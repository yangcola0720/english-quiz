"""
英文搶答計分系統 - Streamlit 版
================================
部署步驟：
  1. 把整個資料夾推上 GitHub
  2. 到 https://share.streamlit.io 連結 GitHub repo
  3. 設定 Main file = app.py，Deploy！

題庫管理：
  - 編輯 questions.json 即可新增/修改題目
  - 格式：[{"q":"題目","opts":["A","B","C","D"],"ans":0,"exp":"解析"}, ...]
  - ans 是正確答案的索引（0=A, 1=B, 2=C, 3=D）
"""

import streamlit as st
import streamlit.components.v1 as components
import json
from pathlib import Path

# ── 頁面設定 ──────────────────────────────────────────────
st.set_page_config(
    page_title="🏆 英文搶答計分系統",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 隱藏 Streamlit 預設 header/footer，讓遊戲全版面顯示
st.markdown("""
<style>
  #MainMenu  { visibility: hidden; }
  header     { visibility: hidden; }
  footer     { visibility: hidden; }
  .block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    max-width: 100% !important;
  }
</style>
""", unsafe_allow_html=True)

# ── 讀取題庫 ──────────────────────────────────────────────
@st.cache_data
def load_questions() -> list:
    path = Path("questions.json")
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            st.warning(f"讀取 questions.json 失敗：{e}，改用內建範例題目。")
    # Fallback（questions.json 不存在時使用）
    return []

questions = load_questions()

if not questions:
    st.error("⚠️ 找不到 questions.json，請確認檔案存在於 repo 根目錄。")
    st.stop()

# ── 讀取遊戲 HTML 並注入題庫 ──────────────────────────────
@st.cache_data
def load_game_html() -> str:
    path = Path("game_streamlit.html")
    if not path.exists():
        st.error("找不到 game_streamlit.html！")
        st.stop()
    return path.read_text(encoding="utf-8")

game_html_raw = load_game_html()

# 把題庫 JSON 注入 HTML（替換佔位符）
questions_json = json.dumps(questions, ensure_ascii=False)
game_html = game_html_raw.replace("__QUESTIONS_JSON__", questions_json)

# ── 渲染遊戲（全版面 iframe）────────────────────────────────
components.html(game_html, height=820, scrolling=False)
