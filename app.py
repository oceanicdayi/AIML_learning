"""
CWA AI Knowledge Hub — Gradio App with ZeroGPU
氣象署 AI 應用學習知識庫 + AI 互動問答
"""

import os
import glob
import gradio as gr
import spaces
from transformers import pipeline

# ---------------------------------------------------------------------------
# 1. Load knowledge base from all Group*/knowledge.md
# ---------------------------------------------------------------------------
KNOWLEDGE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_knowledge_base() -> dict[str, str]:
    """Read all knowledge.md files and return {group_name: content}."""
    kb = {}
    pattern = os.path.join(KNOWLEDGE_DIR, "Group*", "knowledge.md")
    for path in sorted(glob.glob(pattern)):
        group_name = os.path.basename(os.path.dirname(path))
        with open(path, "r", encoding="utf-8") as f:
            kb[group_name] = f.read()
    return kb


KNOWLEDGE_BASE = load_knowledge_base()
FULL_CONTEXT = "\n\n---\n\n".join(
    f"## {name}\n{content}" for name, content in KNOWLEDGE_BASE.items()
)

# Truncate context for model input (keep most relevant ~6000 chars)
MAX_CONTEXT_CHARS = 6000

GROUP_LABELS = {
    "Group1_Weather_Climate_Prediction": "天氣與氣候預報模型開發",
    "Group2_Marine_Climate_Tech": "海象與氣候應用技術",
    "Group3_Warning_Forecasting": "天氣預報與預警應用技術",
    "Group4_Earthquake_Warning": "地震預警應用技術",
    "Group5_Weather_Monitoring": "天氣監測與應用技術",
    "Group7_IT_OpenSource": "資訊系統與開源環境",
    "Group8_AI_Talent_Cultivation": "人工智慧技術人才培育",
    "Group9_Data_Integration_Reconstruction": "資料整集與重建",
}

# ---------------------------------------------------------------------------
# 2. Model — ZeroGPU compatible
# ---------------------------------------------------------------------------
MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"

# Lazy-loaded pipeline (initialized on first GPU call)
_pipe = None


def get_pipe():
    global _pipe
    if _pipe is None:
        _pipe = pipeline(
            "text-generation",
            model=MODEL_ID,
            device_map="auto",
            torch_dtype="auto",
        )
    return _pipe


SYSTEM_PROMPT = """\
你是氣象署 AI 知識庫助手。根據以下課程知識庫內容回答問題。
回答要求：
- 使用繁體中文
- 引用具體技術名稱和模型（如 Pangu-Weather, DGMR, LSTM 等）
- 如果知識庫中沒有相關資訊，誠實說明
- 回答保持簡潔專業

知識庫摘要：
{context}
"""


def build_context_for_query(query: str) -> str:
    """Select most relevant knowledge chunks for the query."""
    query_lower = query.lower()
    scored = []
    for name, content in KNOWLEDGE_BASE.items():
        score = sum(1 for word in query_lower.split() if word in content.lower())
        # Boost by group label match
        label = GROUP_LABELS.get(name, "")
        if any(w in label for w in query):
            score += 3
        scored.append((score, name, content))
    scored.sort(key=lambda x: x[0], reverse=True)

    context_parts = []
    total_len = 0
    for _, name, content in scored:
        label = GROUP_LABELS.get(name, name)
        chunk = f"【{label}】\n{content[:1500]}"
        if total_len + len(chunk) > MAX_CONTEXT_CHARS:
            break
        context_parts.append(chunk)
        total_len += len(chunk)
    return "\n\n".join(context_parts) if context_parts else "（知識庫為空）"


@spaces.GPU(duration=60)
def chat_fn(message: str, history: list[dict]) -> str:
    """Generate AI response using ZeroGPU."""
    if not message.strip():
        return "請輸入您的問題。"

    context = build_context_for_query(message)
    system_msg = SYSTEM_PROMPT.format(context=context)

    messages = [{"role": "system", "content": system_msg}]

    # Add recent history (last 3 turns)
    for turn in history[-6:]:
        messages.append(turn)

    messages.append({"role": "user", "content": message})

    pipe = get_pipe()
    output = pipe(
        messages,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
    )
    return output[0]["generated_text"][-1]["content"]


# ---------------------------------------------------------------------------
# 3. Knowledge browser tab
# ---------------------------------------------------------------------------
def browse_knowledge(group_key: str) -> str:
    """Return knowledge content for selected group."""
    if group_key in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[group_key]
    return "尚無此分組的知識內容。"


def search_knowledge(query: str) -> str:
    """Search across all knowledge files."""
    if not query.strip():
        return "請輸入搜尋關鍵字。"
    results = []
    for name, content in KNOWLEDGE_BASE.items():
        label = GROUP_LABELS.get(name, name)
        lines = content.split("\n")
        matches = [line.strip() for line in lines if query.lower() in line.lower()]
        if matches:
            results.append(f"### {label}\n" + "\n".join(f"- {m}" for m in matches[:5]))
    return "\n\n".join(results) if results else f"找不到與「{query}」相關的內容。"


# ---------------------------------------------------------------------------
# 4. Build Gradio UI
# ---------------------------------------------------------------------------
CSS = """
.main-header { text-align: center; margin-bottom: 1rem; }
.main-header h1 { font-size: 2rem; margin-bottom: 0.25rem; }
.main-header p { color: #888; }
footer { display: none !important; }
"""

HEADER_MD = """
# 🌏 CWA AI Knowledge Hub
### 中央氣象署 AI 技術應用 — 新進人員教育訓練互動知識庫
115 年 4 月 20–21 日 ｜ 8 個任務型分組 ｜ AI 互動問答
"""

GROUP_CHOICES = [(f"{v} ({k})", k) for k, v in GROUP_LABELS.items()]

EXAMPLE_QUESTIONS = [
    "氣象署使用了哪些 AI 天氣預報模型？",
    "DGMR 是什麼？在氣象署如何應用？",
    "地震預警系統使用了什麼 AI 技術？",
    "Pangu-Weather 和 GraphCast 的差異是什麼？",
    "氣象署的 HPC 基礎設施規格為何？",
    "異常波浪監測使用哪些模型？",
]

with gr.Blocks(css=CSS, title="CWA AI Knowledge Hub", theme=gr.themes.Soft()) as demo:

    gr.Markdown(HEADER_MD, elem_classes=["main-header"])

    with gr.Tabs():
        # --- Tab 1: AI Chat ---
        with gr.Tab("🤖 AI 互動問答"):
            gr.Markdown(
                "向 AI 助手提問課程相關問題，模型會根據知識庫內容回答。"
                f"\n\n> 使用模型：`{MODEL_ID}` ｜ ZeroGPU 加速"
            )
            chatbot = gr.ChatInterface(
                fn=chat_fn,
                type="messages",
                examples=EXAMPLE_QUESTIONS,
                cache_examples=False,
            )

        # --- Tab 2: Knowledge Browser ---
        with gr.Tab("📚 知識庫瀏覽"):
            with gr.Row():
                group_dropdown = gr.Dropdown(
                    choices=GROUP_CHOICES,
                    label="選擇分組",
                    value="Group1_Weather_Climate_Prediction",
                )
            knowledge_display = gr.Markdown(
                value=browse_knowledge("Group1_Weather_Climate_Prediction"),
                label="知識內容",
            )
            group_dropdown.change(
                fn=browse_knowledge,
                inputs=group_dropdown,
                outputs=knowledge_display,
            )

        # --- Tab 3: Search ---
        with gr.Tab("🔍 全文搜尋"):
            search_input = gr.Textbox(
                placeholder="輸入關鍵字（如：Transformer、降水、LSTM…）",
                label="搜尋關鍵字",
            )
            search_output = gr.Markdown(label="搜尋結果")
            search_input.submit(
                fn=search_knowledge,
                inputs=search_input,
                outputs=search_output,
            )
            search_btn = gr.Button("搜尋", variant="primary")
            search_btn.click(
                fn=search_knowledge,
                inputs=search_input,
                outputs=search_output,
            )

        # --- Tab 4: Course Map ---
        with gr.Tab("🗺️ 課程地圖"):
            map_md = "## 課程時程\n\n"
            map_md += "### 📅 Day 1 — 4 月 20 日\n\n"
            map_md += "| 時段 | 分組 | 主題 |\n|------|------|------|\n"
            map_md += "| 上午 | Group 1 | 天氣與氣候預報模型開發 |\n"
            map_md += "| 上午 | Group 2 | 海象與氣候應用技術 |\n"
            map_md += "| 下午 | Group 3 | 天氣預報與預警應用技術 |\n"
            map_md += "| 下午 | Group 4 | 地震預警應用技術 |\n\n"
            map_md += "### 📅 Day 2 — 4 月 21 日\n\n"
            map_md += "| 時段 | 分組 | 主題 |\n|------|------|------|\n"
            map_md += "| 上午 | Group 5 | 天氣監測與應用技術 |\n"
            map_md += "| 上午 | Group 7 | 資訊系統與開源環境 |\n"
            map_md += "| 下午 | Group 8 | 人工智慧技術人才培育 |\n"
            map_md += "| 下午 | Group 9 | 資料整集與重建 |\n"
            gr.Markdown(map_md)

    gr.Markdown(
        "<center style='color:#666;font-size:0.8rem;margin-top:1rem;'>"
        "CWA AI Knowledge Hub © 2025 中央氣象署"
        "</center>"
    )

if __name__ == "__main__":
    demo.launch()
