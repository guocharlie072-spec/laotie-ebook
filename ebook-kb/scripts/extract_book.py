#!/usr/bin/env python3
"""
电子书文本提取脚本
支持 PDF (PyMuPDF) 和 EPUB (ebooklib) 格式
用法: python extract_book.py <输入文件路径> <输出txt路径>
"""
import sys
import os

def extract_pdf(pdf_path, output_path):
    import fitz  # PyMuPDF
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    full_text = []
    
    for i, page in enumerate(doc):
        text = page.get_text()
        full_text.append(f"\n--- 第{i+1}页 ---\n{text}")
        if (i + 1) % 50 == 0:
            print(f"  已提取 {i+1}/{total_pages} 页")
    
    doc.close()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(full_text))
    
    print(f"✅ PDF提取完成: {total_pages}页 -> {output_path}")
    return total_pages

def extract_epub(epub_path, output_path):
    import ebooklib
    from ebooklib import epub
    from bs4 import BeautifulSoup
    
    book = epub.read_epub(epub_path)
    full_text = []
    chapter_count = 0
    
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        text = soup.get_text(separator='\n', strip=True)
        if len(text) > 100:  # 跳过太短的碎片
            chapter_count += 1
            full_text.append(f"\n--- 章节{chapter_count} ---\n{text}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(full_text))
    
    print(f"✅ EPUB提取完成: {chapter_count}个章节 -> {output_path}")
    return chapter_count

def main():
    if len(sys.argv) < 3:
        print("用法: python extract_book.py <输入文件> <输出txt路径>")
        print("支持: .pdf .epub")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    if not os.path.exists(input_path):
        print(f"❌ 文件不存在: {input_path}")
        sys.exit(1)
    
    ext = os.path.splitext(input_path)[1].lower()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if ext == '.pdf':
        extract_pdf(input_path, output_path)
    elif ext == '.epub':
        extract_epub(input_path, output_path)
    else:
        print(f"❌ 不支持的格式: {ext}，仅支持 .pdf 和 .epub")
        sys.exit(1)

if __name__ == '__main__':
    main()
