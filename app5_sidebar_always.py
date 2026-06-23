from pathlib import Path
from urllib.parse import quote, unquote
import re

import streamlit as st
import streamlit.components.v1 as components


# app4.py의 큰 틀은 유지한 채 <Graph&Chat> or <Wiki>를 선택하는 것을 selected view 대신 sidebar로 옮김

st.set_page_config(page_title="Snow Tire Knowledge Assistant", layout="wide")

ROOT = Path(".")
WIKI_DIR = ROOT / "wiki"
GRAPH_HTML = ROOT / "graph" / "graph_v2.html"
INDEX_MD = WIKI_DIR / "index.md"


def read_markdown(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"파일을 찾을 수 없습니다: {path}"


def extract_index_links(index_text: str):
    pattern = r"\[([^\]]+)\]\(([^)]+\.md)\)"
    return re.findall(pattern, index_text)


def convert_wikilinks_to_html(text: str, page_map: dict) -> str:
    pattern = r"\[\[([^\]]+)\]\]"

    def replace(match):
        page_name = match.group(1).strip()

        if page_name in page_map:
            encoded_page = quote(page_name)
            return (
                f'<a href="?view=wiki&wiki_page={encoded_page}" '
                f'style="color:#1f77ff; text-decoration:none; font-weight:500;">'
                f'{page_name}</a>'
            )

        return f"<code>[[{page_name}]]</code>"

    return re.sub(pattern, replace, text)


def inject_link_fix_script():
    components.html(
        """
        <script>
        function fixWikiLinks() {
            const links = window.parent.document.querySelectorAll('a[href*="wiki_page"]');
            links.forEach(function(link) {
                link.setAttribute('target', '_self');
                link.removeAttribute('rel');
            });
        }
        fixWikiLinks();
        setTimeout(fixWikiLinks, 300);
        setTimeout(fixWikiLinks, 1000);
        </script>
        """,
        height=0,
        width=0,
    )


st.title("Snow Tire Knowledge Assistant")

# -------------------------
# Build wiki page map
# -------------------------
index_text = read_markdown(INDEX_MD)
wiki_links = extract_index_links(index_text)

page_map = {
    title.strip(): WIKI_DIR / rel_path
    for title, rel_path in wiki_links
}

# -------------------------
# View selector in sidebar
# -------------------------

st.sidebar.markdown("## Navigation")

query_view = st.query_params.get("view", "graph")

selected_view = (
    "Wiki"
    if query_view == "wiki"
    else "Graph & Chat"
)

if st.sidebar.button("Graph & Chat",
                     type="primary" if selected_view=="Graph & Chat" else "secondary", use_container_width=True):
    st.query_params["view"] = "graph"
    st.rerun()

if st.sidebar.button("Wiki",
                     type="primary" if selected_view=="Wiki" else "secondary", use_container_width=True):
    st.query_params["view"] = "wiki"
    st.rerun()

# -------------------------
# Graph & Chat View
# -------------------------
if selected_view == "Graph & Chat":

    st.subheader("Knowledge Graph")

    if GRAPH_HTML.exists():
        graph_html = GRAPH_HTML.read_text(encoding="utf-8")
        components.html(graph_html, height=800, scrolling=True)
    else:
        st.warning("graph/graph_v2.html 파일을 찾을 수 없습니다.")

    st.divider()

    st.subheader("Ask Questions")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_question = st.chat_input("Ask about the wiki or graph...")

    if user_question:
        st.session_state.messages.append(
            {"role": "user", "content": user_question}
        )

        with st.chat_message("user"):
            st.markdown(user_question)

        answer = "아직 LLM QA 기능은 연결되지 않았습니다."

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

# -------------------------
# Wiki View
# -------------------------
if selected_view == "Wiki":

    st.subheader("Wiki")

    if not page_map:
        st.warning("wiki/index.md에서 wiki page 링크를 찾지 못했습니다.")
        st.markdown(index_text)

    else:
        query_page = st.query_params.get("wiki_page")

        if query_page:
            current_page = unquote(query_page).strip()
        elif "current_page" in st.session_state:
            current_page = st.session_state.current_page
        elif "Overview" in page_map:
            current_page = "Overview"
        else:
            current_page = next(iter(page_map))

        if current_page not in page_map:
            current_page = "Overview" if "Overview" in page_map else next(iter(page_map))

        st.session_state.current_page = current_page

        page_names = list(page_map.keys())

    # Sidebar navigation
    st.sidebar.markdown("## Wiki Pages")

    sidebar_links = []

    for page_name in page_names:
        encoded_page = quote(page_name)

        if page_name == current_page:
            sidebar_links.append(
                f"""
                <div style="padding:6px 10px; font-weight:700;">
                    ▶ {page_name}
                </div>
                """
            )
        else:
            sidebar_links.append(
                f"""
                <a href="?view=wiki&wiki_page={encoded_page}"
                target="_self"
                style="display:block; padding:6px 10px; color:inherit; text-decoration:none;">
                    {page_name}
                </a>
                """
            )

    st.sidebar.markdown("\n".join(sidebar_links), unsafe_allow_html=True)

    # Render selected page
    page_path = page_map[current_page]
    page_text = read_markdown(page_path)

    html_text = convert_wikilinks_to_html(page_text, page_map)

    st.markdown(html_text, unsafe_allow_html=True)
    inject_link_fix_script()
