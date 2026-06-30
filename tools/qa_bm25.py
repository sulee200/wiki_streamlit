from pathlib import Path
import os
import re
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from rank_bm25 import BM25Okapi


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WIKI_DIR = PROJECT_ROOT / "wiki" / "concepts"


def preprocess(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_]+", text.lower())


def load_pages() -> list[dict]:
    pages = []

    for path in WIKI_DIR.glob("*.md"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        pages.append({
            "name": path.stem,
            "path": path,
            "text": text,
        })

    return pages


def bm25_search(query: str, top_k: int = 3) -> list[dict]:
    pages = load_pages()

    tokenized_pages = [preprocess(page["text"]) for page in pages]
    bm25 = BM25Okapi(tokenized_pages)

    query_tokens = preprocess(query)
    scores = bm25.get_scores(query_tokens)

    ranked = sorted(
        zip(pages, scores),
        key=lambda x: x[1],
        reverse=True,
    )

    results = []
    for page, score in ranked[:top_k]:
        page = dict(page)
        page["score"] = float(score)
        results.append(page)

    return results


# def build_context(pages: list[dict]) -> str:
#     chunks = []

#     for i, page in enumerate(pages, start=1):
#         chunks.append(
#             f"""[Page {i}]
# Name: {page["name"]}
# Path: {page["path"]}
# BM25 Score: {page["score"]:.4f}

# Content:
# {page["text"]}
# """
#         )

#     return "\n\n---\n\n".join(chunks)


def build_context(pages):
    contexts = []

    for i, page in enumerate(pages, start=1):
        
        contexts.append(
f"""
====================================================

[Page {i}]

Title:
{page["name"]}

Concept Type:
{page.get("concept_type","")}

Sources:
{",".join(page.get("sources", []))}

BM25 Score:
{page["score"]:.3f}

Content:

{page["text"]}
"""
)

    return "\n".join(contexts)


def answer_query(query: str) -> tuple[list[dict], str]:
    load_dotenv(PROJECT_ROOT / ".env")

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY was not loaded. Check .env file name and location.")

    client = genai.Client(
            api_key=os.getenv(api_key)
    )

    retrieved_pages = bm25_search(query, top_k=3)

    context = build_context(retrieved_pages)

    prompt = f"""
You are an expert QA assistant for a snow tire knowledge base.

You are given several wiki pages.

Each page begins with

[page name]

Use ONLY these pages.

When using information from a page,
cite it using the page number.

For example:

- According to [page name 1] page, ...
- [page name 2] page states that ...

If the answer cannot be determined from the pages,
say that the retrieved pages are insufficient.

Question

{query}

Retrieved Wiki Pages

{context}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2
        )
    )

    return retrieved_pages, response.text


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python tools/qa_bm25.py "your question"')
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    retrieved_pages, answer = answer_query(query)

    # from dotenv import dotenv_values
    # config = dotenv_values(PROJECT_ROOT / ".env")
    # print(config)

    print("top-3 pages:\n")
    for page in retrieved_pages:
        print(page['name'])

    print("\nAnswer:\n")
    print(answer)