import io
import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import helper.file_helper as fh
from typing import List, Dict

def rect_intersects(r1, r2, overlap_threshold=0.1):
    """Returns True if two rectangles overlap significantly."""
    intersection = fitz.Rect(r1).intersect(fitz.Rect(r2))
    if intersection.is_empty:
        return False
    overlap_area = intersection.get_area()
    min_area = min(fitz.Rect(r1).get_area(), fitz.Rect(r2).get_area())
    return (overlap_area / min_area) > overlap_threshold

def extract_spans_from_page(page):
    """Extrai spans individuais do PDF, com coordenadas e texto."""
    text_blocks = []
    page_dict = page.get_text("dict")
    for block in page_dict["blocks"]:
        if block["type"] != 0:  # ignora imagens
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                if span["text"].strip():
                    text_blocks.append({
                        "rect": fitz.Rect(span["bbox"]),
                        "text": span["text"].strip()
                    })
    return text_blocks

def merge_text_blocks(
    text_blocks: List[Dict[str, object]], 
    merge: bool = True
) -> List[str]:
    """
    Une linhas que fazem parte do mesmo parágrafo, evitando bullets e respeitando maiúsculas.
    
    Args:
        text_blocks: Lista de dicionários com 'rect' e 'text'.
        merge: Se False, retorna cada bloco separadamente sem tentar unir.

    Returns:
        Lista de strings representando parágrafos/juntas.
    """
    if not merge:
        return [tb["text"] for tb in sorted(text_blocks, key=lambda b: (b["rect"].y0, b["rect"].x0))]

    merged_blocks: List[str] = []
    current_text: str = ""

    for tb in sorted(text_blocks, key=lambda b: (b["rect"].y0, b["rect"].x0)):
        text: str = tb["text"]

        if current_text:
            # Não junta bullets ou linhas que começam com maiúscula
            if text.startswith(("•", "-")) or text[0].isupper():
                merged_blocks.append(current_text)
                current_text = text
            else:
                # Junta se o bloco anterior não terminou com pontuação final
                if current_text[-1] not in ".!?:;":
                    current_text += " " + text
                else:
                    merged_blocks.append(current_text)
                    current_text = text
        else:
            current_text = text

    if current_text:
        merged_blocks.append(current_text)

    return merged_blocks

# -------------------------
# OCR Helpers
# -------------------------

def extract_text_from_images(page, existing_blocks, lang="por+eng"):
    """Faz OCR apenas nas imagens que não sobrepõem texto vetorial."""
    images = page.get_images(full=True)
    ocr_blocks = []

    for img_index, img in enumerate(images):
        xref = img[0]
        base_image = page.parent.extract_image(xref)
        image_data = base_image["image"]

        img_rect = None
        try:
            img_rects = [obj for obj in page.get_drawings() if "rect" in obj]
            img_rect = img_rects[img_index]["rect"] if len(img_rects) > img_index else None
        except Exception:
            pass

        should_ocr = True
        if img_rect:
            for tb in existing_blocks:
                if rect_intersects(img_rect, tb["rect"]):
                    should_ocr = False
                    break

        if should_ocr:
            img_obj = Image.open(io.BytesIO(image_data))
            ocr_text = pytesseract.image_to_string(img_obj, lang=lang)
            if ocr_text.strip():
                ocr_blocks.append({
                    "rect": img_rect or fitz.Rect(0, 0, 9999, 9999),
                    "text": ocr_text.strip()
                })
    return ocr_blocks

# -------------------------
# Main Function
# -------------------------

def extract_text_inteligente(pdf_path, dpi=300, lang="por+eng"):
    """Extrai texto vetorial + OCR de forma inteligente, paginado."""
    doc = fitz.open(pdf_path)
    all_text = []

    for page_index, page in enumerate(doc):
        # 1️⃣ Extrai spans do PDF
        text_blocks = extract_spans_from_page(page)

        # 2️⃣ Adiciona OCR apenas onde necessário
        ocr_blocks = extract_text_from_images(page, text_blocks, lang)
        text_blocks.extend(ocr_blocks)

        # 3️⃣ Junta linhas em parágrafos
        merged_blocks = merge_text_blocks(text_blocks)

        # 4️⃣ Adiciona número da página
        page_text = "\n".join(merged_blocks)
        all_text.append(f"PÁGINA: {page_index + 1}\n\n{page_text}")

    doc.close()
    return "\n\n".join(all_text)


def process_pdfs_in_dir(dir_path, lang="por+eng"):
    """Processes all PDF files in a directory using intelligent extraction."""
    pdf_files = [f for f in os.listdir(dir_path) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("⚠️ Nenhum PDF encontrado no diretório.")
        return

    for pdf_file in pdf_files:
        pdf_path = os.path.join(dir_path, pdf_file)
        print(f"\n🚀 Iniciando extração: {pdf_file}")
        text = extract_text_inteligente(pdf_path, lang=lang)
        output_path = os.path.splitext(pdf_path)[0] + "_texto.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"✅ Texto salvo em: {output_path}\n")


if __name__ == "__main__":
    # Get directory path and language from command-line arguments
    dir_path, lang = fh.get_cli_args()

    print(f"📂 Diretório: {dir_path}")
    print(f"🌐 Idioma OCR: {lang}\n")

    process_pdfs_in_dir(dir_path, lang)
