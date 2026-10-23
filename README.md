# LAOTIE Ebook KB（laotie-ebook）

把电子书（PDF / EPUB）蒸馏成一个随时可调用的本地知识库：自动提取文本、切块建索引、生成核心摘要，写稿、做研究时直接检索书中的观点、案例和数据，不用自己翻书。

## 功能特性

- **一键提取**：用 PyMuPDF 提取 PDF、ebooklib 解析 EPUB，输出纯文本
- **自动切块**：按段落边界切成约 3000 字的文本块，带重叠上下文，检索不丢语境
- **索引可查**：生成全书 `index.md`（总字数、章节标记、块列表），支持关键词 Grep 定位
- **核心摘要**：抽样阅读后产出 `summary.md`（核心论点、章节框架、关键数据、金句、可用素材点）
- **多书共存**：每本书独立文件夹，互不干扰，可随时增量加书
- **只读原始文件**：只读取电子书，绝不改动原文件

## 环境要求

| 依赖 | 说明 |
|---|---|
| Python 3.10+ | 运行提取与切块脚本 |
| PyMuPDF (`fitz`) | PDF 文本提取：`pip install PyMuPDF` |
| ebooklib | EPUB 解析：`pip install ebooklib` |
| beautifulsoup4 | EPUB 正文清洗：`pip install beautifulsoup4` |

安装依赖：

```bash
pip install PyMuPDF ebooklib beautifulsoup4
```

## 目录结构

```
laotie-ebook/
├── README.md
├── .gitignore
└── ebook-kb/                  # Skill 本体
    ├── SKILL.md               # 触发说明与工作流（供 AI Agent 读取）
    └── scripts/
        ├── extract_book.py    # 提取 PDF/EPUB 文本
        └── build_kb.py        # 切块、建索引
```

## 用法

### 1. 提取电子书文本

```bash
python ebook-kb/scripts/extract_book.py <输入.pdf 或 .epub> <输出.txt>
```

示例：

```bash
python ebook-kb/scripts/extract_book.py "我的书.pdf" "./知识库/我的书/raw_extracted.txt"
```

### 2. 切块建索引

```bash
python ebook-kb/scripts/build_kb.py <提取的.txt> <知识库输出目录>
```

示例：

```bash
python ebook-kb/scripts/build_kb.py "./知识库/我的书/raw_extracted.txt" "./知识库/我的书"
```

产出：

```
知识库/我的书/
├── index.md          # 全书索引：字数、章节标记、文本块列表
├── raw.txt          # 原始全文备份
└── chunks/          # 分块文本，用于关键词检索
    ├── chunk_001.md
    └── ...
```

### 3. 查询

在 `chunks/` 目录用关键词检索，再精读命中的块：

```
Grep "关键词" path="./知识库/我的书/chunks" -C 3
```

命中后 Read 对应 chunk 文件，引用原文作答；搜不到就明确说"书中没有"，不要编造。

## 作为 Agent Skill 使用

把 `ebook-kb/` 整个文件夹放进你的 skills 目录后，Agent 会依据 `SKILL.md` 自动触发：

- **新建**：说"把这本书做成知识库"并给出文件路径，自动跑提取 → 切块 → 摘要
- **查询**：直接问"书里关于 XX 是怎么说的"，自动检索并引用原文

## 说明

- 扫描版 PDF（纯图片、无文字层）提取字数会很少，需要先做 OCR，脚本无法直接处理
- 个人书库数据（提取出的文本、摘要）不入库，`.gitignore` 已忽略
