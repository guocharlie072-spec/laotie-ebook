#!/usr/bin/env python3
"""
知识库构建脚本：把提取后的长文本切块、分文件、生成索引
用法: python build_kb.py <输入txt路径> <输出知识库目录>
输出结构:
  <输出目录>/
    ├── index.md          # 全书索引和概览
    ├── chunks/           # 分块文本
    │   ├── chunk_001.md
    │   ├── chunk_002.md
    │   └── ...
    └── raw.txt           # 原始全文（备份）
"""
import sys
import os
import re

def split_into_chunks(text, max_chars=3000, overlap=200):
    """按段落优先切块，尽量在段落边界切分"""
    paragraphs = re.split(r'\n\s*\n', text)
    chunks = []
    current_chunk = []
    current_len = 0
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        para_len = len(para)
        
        if current_len + para_len > max_chars and current_chunk:
            # 保存当前块
            chunks.append('\n\n'.join(current_chunk))
            # 保留重叠部分
            overlap_text = current_chunk[-1] if current_chunk else ''
            current_chunk = [overlap_text] if overlap_text else []
            current_len = len(overlap_text)
        
        current_chunk.append(para)
        current_len += para_len
    
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks

def detect_chapter_titles(text):
    """尝试识别章节标题（简单规则：短行 + 章节/第X章/Chapter等关键词）"""
    lines = text.split('\n')
    chapters = []
    for i, line in enumerate(lines):
        line = line.strip()
        if 3 < len(line) < 50:
            if re.match(r'^(第[一二三四五六七八九十百千\d]+[章节回卷部]|Chapter\s+\d+|序章|前言|序言|引言|结语|后记|附录|附录|楔子|尾声)', line, re.IGNORECASE):
                chapters.append((i, line))
    return chapters

def main():
    if len(sys.argv) < 3:
        print("用法: python build_kb.py <输入txt路径> <输出知识库目录>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    kb_dir = sys.argv[2]
    
    if not os.path.exists(input_path):
        print(f"❌ 文件不存在: {input_path}")
        sys.exit(1)
    
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    total_chars = len(text)
    print(f"📖 全书字数: {total_chars:,}")
    
    # 检测章节
    chapters = detect_chapter_titles(text)
    print(f"📑 识别到章节标记: {len(chapters)} 个")
    
    # 切块
    chunks = split_into_chunks(text)
    print(f"✂️  切分为 {len(chunks)} 个文本块")
    
    # 创建输出目录
    chunks_dir = os.path.join(kb_dir, 'chunks')
    os.makedirs(chunks_dir, exist_ok=True)
    
    # 保存原始全文
    raw_path = os.path.join(kb_dir, 'raw.txt')
    with open(raw_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    # 保存每个chunk
    chunk_files = []
    for i, chunk in enumerate(chunks):
        chunk_file = f"chunk_{i+1:03d}.md"
        chunk_path = os.path.join(chunks_dir, chunk_file)
        with open(chunk_path, 'w', encoding='utf-8') as f:
            f.write(chunk)
        chunk_files.append((i+1, chunk_file, len(chunk)))
    
    # 生成索引文件
    book_name = os.path.basename(input_path).replace('.txt', '')
    index_path = os.path.join(kb_dir, 'index.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(f"# 《{book_name}》知识库索引\n\n")
        f.write(f"- 总字数: {total_chars:,}\n")
        f.write(f"- 文本块数: {len(chunks)}\n")
        f.write(f"- 识别章节数: {len(chapters)}\n\n")
        
        f.write("## 章节标记\n\n")
        for idx, title in chapters[:30]:
            f.write(f"- {title}\n")
        if len(chapters) > 30:
            f.write(f"- ... (共{len(chapters)}个)\n")
        
        f.write("\n## 文本块列表\n\n")
        f.write("| 块号 | 文件 | 字数 |\n")
        f.write("|------|------|------|\n")
        for num, fname, size in chunk_files:
            f.write(f"| {num} | {fname} | {size:,} |\n")
    
    print(f"✅ 知识库构建完成: {kb_dir}")
    print(f"   - 索引: {index_path}")
    print(f"   - 文本块目录: {chunks_dir}")

if __name__ == '__main__':
    main()
