"""
Convert knowledge.md → interactive index.html for each Group folder.
Uses Tailwind CSS (CDN), Mermaid.js, Dark Mode, collapsible sections.
"""
import re
import html
import sys
from pathlib import Path

WORKSPACE = Path(r"d:\WORK\AI_ML小組新進人員教育訓練簡報")

GROUPS = [
    ("Group1_Weather_Climate_Prediction", "天氣與氣候預報模型開發", "🌦️"),
    ("Group2_Marine_Climate_Tech", "海象與氣候應用技術", "🌊"),
    ("Group3_Warning_Forecasting", "天氣預報與預警應用技術", "⚡"),
    ("Group4_Earthquake_Warning", "地震預警應用技術", "🔔"),
    ("Group5_Weather_Monitoring", "天氣監測與應用技術", "📡"),
    ("Group7_IT_OpenSource", "資訊系統與開源環境", "🖥️"),
    ("Group8_AI_Talent_Cultivation", "AI 人才培育", "🎓"),
]

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-TW" class="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — CWA AI Knowledge Hub</title>
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {{
  darkMode: 'class',
  theme: {{
    extend: {{
      colors: {{
        cwa: {{ 50:'#eef7ff', 100:'#d9edff', 200:'#bce0ff', 300:'#8ecdff', 400:'#53b1ff', 500:'#2b91ff', 600:'#1070f5', 700:'#0a5ae1', 800:'#0f49b6', 900:'#12408f', 950:'#0e2a5e' }}
      }}
    }}
  }}
}}
</script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});</script>
<style>
  body {{ font-family: 'Noto Sans TC', 'Inter', system-ui, sans-serif; }}
  .prose h2 {{ scroll-margin-top: 5rem; }}
  .collapsible-content {{ max-height: 0; overflow: hidden; transition: max-height 0.4s ease-out; }}
  .collapsible-content.open {{ max-height: 8000px; transition: max-height 0.6s ease-in; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #334155; padding: 0.5rem 0.75rem; text-align: left; }}
  th {{ background: #1e293b; font-weight: 600; }}
  tr:nth-child(even) {{ background: rgba(30,41,59,0.3); }}
  blockquote {{ border-left: 4px solid #2b91ff; padding-left: 1rem; color: #94a3b8; font-style: italic; }}
  code {{ background: #1e293b; padding: 0.15rem 0.4rem; border-radius: 4px; font-size: 0.9em; }}
  pre {{ background: #0f172a; padding: 1rem; border-radius: 8px; overflow-x: auto; }}
  pre code {{ background: none; padding: 0; }}
  a {{ color: #53b1ff; text-decoration: underline; }}
  .highlight-box {{ background: linear-gradient(135deg, #0f2a5e 0%, #12408f 100%); border: 1px solid #2b91ff; border-radius: 12px; padding: 1.25rem; margin: 1rem 0; }}
  ::-webkit-scrollbar {{ width: 8px; }}
  ::-webkit-scrollbar-track {{ background: #0f172a; }}
  ::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 4px; }}
</style>
</head>
<body class="bg-slate-950 text-slate-200 min-h-screen">

<!-- Top Nav -->
<nav class="fixed top-0 w-full z-50 bg-slate-900/95 backdrop-blur border-b border-slate-800">
  <div class="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
    <a href="../main.html" class="text-sm text-slate-400 hover:text-white transition">← 返回學習地圖</a>
    <span class="text-lg font-bold text-white">{emoji} {short_title}</span>
    <button onclick="document.documentElement.classList.toggle('dark')" class="text-sm px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 transition">🌓</button>
  </div>
</nav>

<!-- Sidebar TOC (desktop) -->
<aside id="toc" class="hidden lg:block fixed left-0 top-14 w-60 h-[calc(100vh-3.5rem)] overflow-y-auto bg-slate-900/80 border-r border-slate-800 p-4 text-sm">
  <h3 class="text-xs uppercase tracking-wider text-slate-500 mb-3">目錄</h3>
  <div id="toc-links" class="space-y-1"></div>
</aside>

<!-- Main Content -->
<main class="lg:ml-60 pt-20 pb-16 px-4">
  <article class="max-w-4xl mx-auto prose prose-invert">
    {content}
  </article>
</main>

<!-- Back to top -->
<button onclick="window.scrollTo({{top:0,behavior:'smooth'}})" class="fixed bottom-6 right-6 bg-cwa-700 hover:bg-cwa-600 text-white w-10 h-10 rounded-full shadow-lg flex items-center justify-center transition text-lg">↑</button>

<script>
// Build TOC from h2 elements
document.addEventListener('DOMContentLoaded', () => {{
  const tocBox = document.getElementById('toc-links');
  document.querySelectorAll('article h2').forEach((h2, i) => {{
    if (!h2.id) h2.id = 'section-' + i;
    const a = document.createElement('a');
    a.href = '#' + h2.id;
    a.textContent = h2.textContent;
    a.className = 'block py-1 px-2 rounded text-slate-400 hover:text-white hover:bg-slate-800 transition truncate';
    tocBox.appendChild(a);
  }});

  // Collapsible sections
  document.querySelectorAll('.collapsible-toggle').forEach(btn => {{
    btn.addEventListener('click', () => {{
      const target = btn.nextElementSibling;
      target.classList.toggle('open');
      btn.querySelector('.chevron').textContent = target.classList.contains('open') ? '▾' : '▸';
    }});
  }});
}});
</script>
</body>
</html>"""


def md_to_html_content(md_text: str) -> str:
    """Convert markdown to HTML content (lightweight parser)."""
    lines = md_text.split('\n')
    html_parts = []
    in_table = False
    in_code = False
    in_mermaid = False
    in_list = False
    in_blockquote = False
    code_lang = ""
    mermaid_lines = []
    table_rows = []
    list_items = []
    bq_lines = []

    def flush_table():
        nonlocal table_rows, in_table
        if not table_rows:
            return
        out = '<div class="overflow-x-auto my-4"><table>\n'
        for ri, row in enumerate(table_rows):
            cells = [c.strip() for c in row.strip('|').split('|')]
            tag = 'th' if ri == 0 else 'td'
            if ri == 1 and all(set(c.strip()) <= set('-: ') for c in cells):
                continue
            out += '<tr>' + ''.join(f'<{tag}>{inline(c)}</{tag}>' for c in cells) + '</tr>\n'
        out += '</table></div>\n'
        html_parts.append(out)
        table_rows = []
        in_table = False

    def flush_list():
        nonlocal list_items, in_list
        if not list_items:
            return
        html_parts.append('<ul class="list-disc list-inside space-y-1 my-3">\n')
        for li in list_items:
            html_parts.append(f'  <li>{inline(li)}</li>\n')
        html_parts.append('</ul>\n')
        list_items = []
        in_list = False

    def flush_blockquote():
        nonlocal bq_lines, in_blockquote
        if not bq_lines:
            return
        content = '<br>'.join(inline(l) for l in bq_lines)
        html_parts.append(f'<blockquote class="my-4">{content}</blockquote>\n')
        bq_lines = []
        in_blockquote = False

    def inline(text: str) -> str:
        """Handle inline markdown: bold, italic, code, links, KaTeX."""
        t = html.escape(text)
        # bold
        t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
        # italic
        t = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', t)
        # inline code
        t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
        # links
        t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
        # strikethrough
        t = re.sub(r'~~(.+?)~~', r'<del>\1</del>', t)
        return t

    section_counter = 0

    for line in lines:
        stripped = line.strip()

        # Code fence
        if stripped.startswith('```'):
            if not in_code:
                lang = stripped[3:].strip()
                if lang == 'mermaid':
                    in_mermaid = True
                    mermaid_lines = []
                else:
                    in_code = True
                    code_lang = lang
                    html_parts.append(flush_list.__call__() or '')
                    flush_list()
                    flush_table()
                    flush_blockquote()
                    html_parts.append(f'<pre><code class="language-{html.escape(code_lang)}">')
            else:
                if in_mermaid:
                    mermaid_content = '\n'.join(mermaid_lines)
                    html_parts.append(f'<div class="mermaid my-6 bg-slate-900 p-4 rounded-lg overflow-x-auto">\n{mermaid_content}\n</div>\n')
                    in_mermaid = False
                else:
                    html_parts.append('</code></pre>\n')
                    in_code = False
            continue

        if in_code:
            html_parts.append(html.escape(line) + '\n')
            continue
        if in_mermaid:
            mermaid_lines.append(line)
            continue

        # Table
        if '|' in stripped and stripped.startswith('|'):
            if not in_table:
                flush_list()
                flush_blockquote()
                in_table = True
            table_rows.append(stripped)
            continue
        elif in_table:
            flush_table()

        # List
        if re.match(r'^[-*+]\s', stripped) or re.match(r'^\d+\.\s', stripped):
            if not in_list:
                flush_table()
                flush_blockquote()
                in_list = True
            item = re.sub(r'^[-*+\d.]+\s*', '', stripped)
            list_items.append(item)
            continue
        elif in_list and stripped == '':
            flush_list()
            continue
        elif in_list and stripped:
            flush_list()

        # Blockquote
        if stripped.startswith('>'):
            if not in_blockquote:
                flush_table()
                flush_list()
                in_blockquote = True
            bq_lines.append(stripped.lstrip('> '))
            continue
        elif in_blockquote:
            flush_blockquote()

        # Headings
        if stripped.startswith('# ') and not stripped.startswith('## '):
            flush_table(); flush_list(); flush_blockquote()
            text = stripped[2:]
            html_parts.append(f'<h1 class="text-3xl md:text-4xl font-bold text-white mb-6 mt-2">{inline(text)}</h1>\n')
            continue
        if stripped.startswith('## '):
            flush_table(); flush_list(); flush_blockquote()
            text = stripped[3:]
            section_counter += 1
            sid = f"section-{section_counter}"
            html_parts.append(f'''
<div class="mt-12 mb-4">
  <h2 id="{sid}" class="text-2xl font-bold text-cwa-400 border-b border-slate-700 pb-2">{inline(text)}</h2>
</div>\n''')
            continue
        if stripped.startswith('### '):
            flush_table(); flush_list(); flush_blockquote()
            text = stripped[4:]
            html_parts.append(f'<h3 class="text-xl font-semibold text-slate-100 mt-8 mb-3">{inline(text)}</h3>\n')
            continue
        if stripped.startswith('#### '):
            flush_table(); flush_list(); flush_blockquote()
            text = stripped[5:]
            html_parts.append(f'<h4 class="text-lg font-medium text-slate-200 mt-6 mb-2">{inline(text)}</h4>\n')
            continue

        # Horizontal rule
        if stripped in ('---', '***', '___'):
            flush_table(); flush_list(); flush_blockquote()
            html_parts.append('<hr class="border-slate-700 my-8">\n')
            continue

        # Empty line
        if stripped == '':
            continue

        # Paragraph
        html_parts.append(f'<p class="my-3 leading-relaxed">{inline(stripped)}</p>\n')

    # Flush remaining
    flush_table()
    flush_list()
    flush_blockquote()

    return ''.join(html_parts)


def build_html(folder_name: str, title: str, emoji: str):
    md_path = WORKSPACE / folder_name / "knowledge.md"
    if not md_path.exists():
        print(f"  SKIP {folder_name} (no knowledge.md)")
        return False

    md_text = md_path.read_text(encoding='utf-8')
    content = md_to_html_content(md_text)

    short_title = title
    page_html = HTML_TEMPLATE.format(
        title=title,
        short_title=short_title,
        emoji=emoji,
        content=content,
    )

    out_path = WORKSPACE / folder_name / "index.html"
    out_path.write_text(page_html, encoding='utf-8')
    print(f"  ✓ {out_path}")
    return True


def main():
    print("=== Phase 3: knowledge.md → index.html ===")
    count = 0
    for folder, title, emoji in GROUPS:
        if build_html(folder, title, emoji):
            count += 1
    print(f"\nDone: {count} HTML files generated.")


if __name__ == "__main__":
    main()
