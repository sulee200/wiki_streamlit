from __future__ import annotations

from pathlib import Path
import json
import os
import re
import sys

from dotenv import load_dotenv
from rank_bm25 import BM25Okapi
from google import genai
from google.genai import types
from openai import OpenAI


LLM_MODEL = "Llama" # or "GEMINI"


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WIKI_DIR = PROJECT_ROOT / "wiki" / "concepts"
GRAPH_PATH = PROJECT_ROOT / "graph" / "graph.json"


def label_to_id(label: str) -> str:
    return (
        label.lower()
             .replace(" ", "_")
    )


def preprocess(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_]+", text.lower())


def load_pages() -> list[dict]:
    pages = []

    for path in WIKI_DIR.glob("*.md"):
        text = path.read_text(encoding="utf-8", errors="ignore")

        pages.append({
            "name": path.stem,
            "path": str(path),
            "text": text,
        })

    return pages


def bm25_search(query: str, top_k: int = 3) -> list[dict]:
    pages = load_pages()

    if not pages:
        raise ValueError(f"No wiki pages found in {WIKI_DIR}")

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
        item = dict(page)
        item["score"] = float(score)
        results.append(item)

    return results


def load_graph() -> dict:
    if not GRAPH_PATH.exists():
        raise FileNotFoundError(f"graph.json not found: {GRAPH_PATH}")

    return json.loads(GRAPH_PATH.read_text(encoding="utf-8"))


def normalize_node_id(name: str) -> str:
    return name.lower().replace(" ", "_").replace("-", "_")



def get_graph_nodes_edges(graph: dict) -> tuple[list[dict], list[dict]]:
    return graph["nodes"], graph["edges"]


def get_node_id(node: dict) -> str:
    return node["id"]


def get_edge_source(edge: dict) -> str:
    return edge["source"]


def get_edge_target(edge: dict) -> str:
    return edge["target"]




# def find_matching_node_id(page_name: str, graph: dict) -> str | None:

#     nodes, _ = get_graph_nodes_edges(graph)

#     target = page_name.lower().strip()

#     for node in nodes:

#         label = node["label"].lower().strip()

#         if label == target:
#             return node["id"]

#     return None


def extract_subgraph(seed_node_id: str, graph: dict, hops: int = 1) -> dict:
    nodes, edges = get_graph_nodes_edges(graph)

    node_map = {get_node_id(node): node for node in nodes}
    adjacency: dict[str, list[tuple[str, dict]]] = {} # {"A": [("B", {"type": "related_to", ...}), ("C", {"type": "related_to", ...})]}

    for edge in edges:
        src = get_edge_source(edge)
        tgt = get_edge_target(edge)

        adjacency.setdefault(src, []).append((tgt, edge)) # ("A", ("B", {edge}))
        adjacency.setdefault(tgt, []).append((src, edge)) # ("B", ("A", {edge}))

    visited = {seed_node_id}
    frontier = {seed_node_id}
    sub_edges = []

    for _ in range(hops):
        next_frontier = set()

        for node_id in frontier:
            for neighbor, edge in adjacency.get(node_id, []):
                sub_edges.append(edge)

                if neighbor not in visited:
                    visited.add(neighbor)
                    next_frontier.add(neighbor)

        frontier = next_frontier

    sub_nodes = [
        node_map[node_id]
        for node_id in visited
        if node_id in node_map
    ]

    return {
        "seed": seed_node_id,
        "nodes": sub_nodes,
        "edges": sub_edges,
    }


def collect_subgraphs(seed_pages: list[dict], hops: int = 1) -> list[dict]:
    graph = load_graph()
    nodes, _ = get_graph_nodes_edges(graph)
    valid_node_ids = {node["id"] for node in nodes}

    subgraphs = []

    for page in seed_pages:
        node_id = label_to_id(page["name"])

        if node_id not in valid_node_ids:
            continue

        subgraph = extract_subgraph(node_id, graph, hops=hops)
        subgraph["seed_page"] = page["name"]
        subgraph["bm25_score"] = page["score"]

        subgraphs.append(subgraph)

    return subgraphs



def format_subgraphs_for_llm(subgraphs: list[dict]) -> str:
    blocks = []

    for i, sg in enumerate(subgraphs, start=1):
        node_lines = []

        for node in sg["nodes"]:
            node_id = get_node_id(node)
            title = node.get("label") or node.get("title") or node_id
            concept_type = node.get("concept_type") or node.get("type") or node.get("node_type", "")

            node_lines.append(
                f"- node_id: {node_id}, title: {title}, concept_type: {concept_type}"
            )

        edge_lines = []

        for edge in sg["edges"]:
            src = get_edge_source(edge)
            tgt = get_edge_target(edge)
            relation = edge.get("relation") or edge.get("type") or edge.get("label") or "related_to"
            confidence = edge.get("confidence", "")

            edge_lines.append(
                f"- {src} --[{relation}, confidence={confidence}]--> {tgt}"
            )

        blocks.append(
            f"""
[Subgraph {i}]
Seed page: {sg["seed_page"]}
Seed node: {sg["seed"]}
BM25 score: {sg["bm25_score"]:.3f}

Nodes:
{chr(10).join(node_lines)}

Edges:
{chr(10).join(edge_lines)}
"""
        )

    return "\n\n".join(blocks)


def get_gemini_client():
    load_dotenv(PROJECT_ROOT / ".env")

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY was not loaded. Check .env file.")

    return genai.Client(api_key=api_key)

def get_llama_client():
    load_dotenv(PROJECT_ROOT / ".env")

    api_key = os.getenv("Llama_API_KEY")

    if not api_key:
        raise ValueError("Llama_API_KEY was not loaded. Check .env file")
    
    return OpenAI(base_url = "https://integrate.api.nvidia.com/v1", api_key = api_key)


def choose_pages_with_llm(query: str, subgraphs: list[dict]) -> list[str]:
    subgraph_text = format_subgraphs_for_llm(subgraphs)

    prompt = f"""
        Return ONLY the final JSON list.
        Do not reason.
        Do not analyze.
        Do not write explanations.
        Do not include markdown.

        You are selecting wiki pages for a snow tire QA system.

        Return format example:
        ["Snow Traction", "Tire Tread Pattern"]

        User query:
        {query}

        Subgraphs:
        {subgraph_text}
    """

    if LLM_MODEL == "GEMINI":

        client = get_gemini_client()

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.0,
            ),
        )

        text = response.text

    elif LLM_MODEL == "Llama":

        client = get_llama_client()

        response = client.chat.completions.create(

            model="nvidia/llama-3.3-nemotron-super-49b-v1.5",
            messages=[
                {"role": "system", "content": "You must return only valid JSON. No reasoning, no explanation, no markdown."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            top_p=0.95,
            max_tokens=4096,
            frequency_penalty=0,
            presence_penalty=0,
            stream=False
        )

        text = response.choices[0].message.content

    else:
        raise ValueError(f"Set an appropriate LLM model")
    

    if text is None:
        raise ValueError(f"LLM returned no content:\n{response.model_dump()}")
    
    text = text.strip()

    try:
        pages = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\[.*\]", text, flags=re.DOTALL)
        if not match:
            raise ValueError(f"LLM did not return a JSON list:\n{text}")
        pages = json.loads(match.group(0))

    return [str(p) for p in pages]


def load_selected_pages(page_names: list[str]) -> list[dict]:

    all_pages = load_pages()

    page_map = {
        label_to_id(page["name"]): page
        for page in all_pages
    }

    pages = []

    for name in page_names:

        page = page_map.get(label_to_id(name))

        if page:
            pages.append(page)

    return pages


def build_page_context(pages: list[dict]) -> str:
    contexts = []

    for i, page in enumerate(pages, start=1):
        contexts.append(
            f"""
==================================================
[Page {page["name"]}]

Title:
{page["name"]}

Path:
{page["path"]}

Content:
{page["text"]}
"""
        )

    return "\n".join(contexts)


def generate_final_answer(query: str, pages: list[dict]) -> str:
    context = build_page_context(pages)

    prompt = f"""
        You are an expert QA assistant for a snow tire knowledge base.

        Answer the user's question using ONLY the wiki pages below.
        Cite evidence using the exact wiki page title, for example [Snow Traction] or [Slip Ratio].
        At the end, include a Sources section listing only the exact page titles used.
        Do not cite pages as [Page 1], [Page 2], or similar numbered labels.
        If the pages are insufficient, say that the retrieved pages are insufficient.

        User question:
        {query}

        Retrieved wiki pages:
        {context}
    """ 
    
    if LLM_MODEL == "GEMINI":

        client = get_gemini_client()

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.0,
            ),
        )

        text = response.text

    elif LLM_MODEL == "Llama":

        client = get_llama_client()

        response = client.chat.completions.create(

            model="nvidia/llama-3.3-nemotron-super-49b-v1.5",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            top_p=0.95,
            max_tokens=4096,
            frequency_penalty=0,
            presence_penalty=0,
            stream=False
        )

        text = response.choices[0].message.content

    return text.strip()


def answer_query(query: str) -> tuple[str, dict]:
    seed_pages = bm25_search(query, top_k=3)
    subgraphs = collect_subgraphs(seed_pages, hops=1)

    selected_page_names = choose_pages_with_llm(query, subgraphs)

    # fallback: if LLM selected nothing, use BM25 top-3 directly
    selected_pages = load_selected_pages(selected_page_names)

    if not selected_pages:
        selected_pages = seed_pages

    answer = generate_final_answer(query, selected_pages)

    debug_info = {
        "bm25_seed_pages": [
            {"name": p["name"], "score": p["score"]}
            for p in seed_pages
        ],
        "selected_page_names": selected_page_names,
        "loaded_pages": [
            p["name"]
            for p in selected_pages
        ],
    }

    return answer, debug_info


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python tools/qa_graph.py "your question"')
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    answer, debug = answer_query(query)

    print("\n=== BM25 Seed Pages ===")
    for item in debug["bm25_seed_pages"]:
        print(f'- {item["name"]}  score={item["score"]:.3f}')

    print("\n=== LLM Selected Pages ===")
    for name in debug["selected_page_names"]:
        print(f"- {name}")

    print("\n=== Loaded Pages ===")
    for name in debug["loaded_pages"]:
        print(f"- {name}")

    print("\n=== Answer ===")
    print(answer)