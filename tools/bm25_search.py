from pathlib import Path
import re
import sys

from rank_bm25 import BM25Okapi


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WIKI_DIR = PROJECT_ROOT / "wiki" / "concepts"


def preprocess(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_]+", text.lower()) # 알파벳, 숫자, _만 단어별로 띄어서 리스트 만들기


def load_pages():
    pages = []

    for path in WIKI_DIR.glob("*.md"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        pages.append({
            "name": path.stem,
            "path": path,
            "text": text,
        })

    return pages


def search(query: str, top_k: int = 3):
    pages = load_pages()

    if not pages:
        print(f"No markdown pages found in {WIKI_DIR}")
        return

    tokenized_pages = [preprocess(page["text"]) for page in pages]
    bm25 = BM25Okapi(tokenized_pages)

    query_tokens = preprocess(query)
    scores = bm25.get_scores(query_tokens)

    ranked = sorted(
        zip(pages, scores),
        key=lambda x: x[1],
        reverse=True, # bm25 score가 높을수록 query와 연관된 문서
    )

    for page, score in ranked[:top_k]:
        print(f"{page['name']}  score={score:.4f}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python tools/bm25_search.py "your query"')
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    search(query, top_k=3)