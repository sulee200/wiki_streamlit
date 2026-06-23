#!/usr/bin/env python3
from __future__ import annotations

"""
Build the snow tire knowledge graph from wiki markdown pages.

The graph is deterministic: nodes come from wiki/*.md pages, and typed edges
come from each page's "## Related Concepts" section.
"""

import argparse
import html
import json
import re
import unicodedata
import webbrowser
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any

try:
    import networkx as nx
    from networkx.algorithms import community as nx_community

    HAS_NETWORKX = True
except ImportError:
    nx = None
    nx_community = None
    HAS_NETWORKX = False


REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = REPO_ROOT / "wiki"
GRAPH_DIR = REPO_ROOT / "graph"
GRAPH_JSON = GRAPH_DIR / "graph.json"
GRAPH_HTML = GRAPH_DIR / "graph.html"

ALLOWED_RELATIONS = {
    "positively_affects",
    "negatively_affects",
    "consists_of",
    "part_of",
    "utilizes",
    "causes",
    "contradicts",
    "related_to",
}
ALLOWED_CONFIDENCE = {"EXTRACTED", "INFERRED", "AMBIGUOUS"}
CONFIDENCE_SCORES = {"EXTRACTED": 1.0, "INFERRED": 0.6, "AMBIGUOUS": 0.25}
RELATION_COLORS = {
    "positively_affects": "#59A14F",
    "negatively_affects": "#E15759",
    "consists_of": "#4E79A7",
    "part_of": "#76B7B2",
    "utilizes": "#F28E2B",
    "causes": "#EDC948",
    "contradicts": "#B07AA1",
    "related_to": "#BAB0AC",
}
TYPE_COLORS = {
    "concept": "#F28E2B",
    "source": "#59A14F",
    "synthesis": "#B07AA1",
    "entity": "#4E79A7",
    "unknown": "#BAB0AC",
}
SKIP_PAGE_NAMES = {
    "log.md",
    "lint-report.md",
    "health-report.md",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_frontmatter(markdown: str) -> str:
    return re.sub(r"\A---\s*\n.*?\n---\s*\n?", "", markdown, flags=re.DOTALL)


def parse_frontmatter(markdown: str) -> dict[str, Any]:
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n?", markdown, flags=re.DOTALL)
    if not match:
        return {}

    data: dict[str, Any] = {}
    current_key: str | None = None
    for raw_line in match.group(1).splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")) and current_key:
            item = line.strip()
            if item.startswith("- "):
                data.setdefault(current_key, []).append(clean_scalar(item[2:]))
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        current_key = key.strip()
        value = value.strip()
        if value == "[]":
            data[current_key] = []
        elif value:
            data[current_key] = clean_scalar(value)
        else:
            data[current_key] = []
    return data


def clean_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def wiki_pages() -> list[Path]:
    return sorted(
        p for p in WIKI_DIR.rglob("*.md")
        if p.name not in SKIP_PAGE_NAMES and not p.name.startswith(".")
    )


def normalize_id(label: str) -> str:
    text = unicodedata.normalize("NFKD", label)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "node"


def page_title(path: Path, frontmatter: dict[str, Any], body: str) -> str:
    if frontmatter.get("title"):
        return str(frontmatter["title"]).strip()
    heading = re.search(r"^#\s+(.+?)\s*$", body, flags=re.MULTILINE)
    if heading:
        return heading.group(1).strip()
    return path.stem.replace("-", " ").replace("_", " ").title()


def node_type(frontmatter: dict[str, Any], path: Path) -> str:
    raw = frontmatter.get("node_type") or frontmatter.get("type")
    if raw:
        return str(raw).strip()
    parent = path.parent.name
    if parent == "concepts":
        return "concept"
    if parent == "sources":
        return "source"
    if parent == "syntheses":
        return "synthesis"
    return "unknown"


def concept_type(frontmatter: dict[str, Any]) -> str:
    return str(frontmatter.get("concept_type") or "").strip()


def preview(markdown: str, limit: int = 280) -> str:
    body = strip_frontmatter(markdown)
    lines = [
        re.sub(r"\s+", " ", line.strip(" #-*\t"))
        for line in body.splitlines()
        if line.strip() and not line.lstrip().startswith("```")
    ]
    return " ".join(lines)[:limit]


def make_nodes(pages: list[Path]) -> tuple[list[dict[str, Any]], dict[str, str], list[str]]:
    nodes: list[dict[str, Any]] = []
    lookup: dict[str, str] = {}
    used_ids: dict[str, int] = defaultdict(int)
    warnings: list[str] = []

    for path in pages:
        markdown = read_text(path)
        fm = parse_frontmatter(markdown)
        body = strip_frontmatter(markdown)
        title = page_title(path, fm, body)
        base_id = normalize_id(title)
        used_ids[base_id] += 1
        node_id = base_id if used_ids[base_id] == 1 else f"{base_id}_{used_ids[base_id]}"
        ntype = node_type(fm, path)

        node = {
            "id": node_id,
            "label": title,
            "node_type": ntype,
            "type": ntype,
            "concept_type": concept_type(fm),
            "path": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "source_file": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "preview": preview(markdown),
            "markdown": markdown,
            "color": TYPE_COLORS.get(ntype, TYPE_COLORS["unknown"]),
        }
        nodes.append(node)

        keys = {
            title,
            path.stem,
            path.stem.replace("-", " ").replace("_", " "),
            path.with_suffix("").relative_to(WIKI_DIR).as_posix(),
        }
        for key in keys:
            normalized = normalize_lookup_key(key)
            existing = lookup.get(normalized)
            if existing and existing != node_id:
                warnings.append(f"Ambiguous page lookup '{key}' resolves to both {existing} and {node_id}")
            else:
                lookup[normalized] = node_id

    return nodes, lookup, warnings


def normalize_lookup_key(value: str) -> str:
    value = value.split("|", 1)[0].split("#", 1)[0].strip()
    value = re.sub(r"\.(md|markdown)$", "", value, flags=re.IGNORECASE)
    value = value.replace("\\", "/").split("/")[-1]
    return normalize_id(value)


def related_concepts_section(markdown: str) -> str:
    match = re.search(
        r"^##\s+Related Concepts\s*$([\s\S]*?)(?=^##\s+|\Z)",
        markdown,
        flags=re.MULTILINE | re.IGNORECASE,
    )
    return match.group(1) if match else ""


def extract_related_entries(markdown: str) -> list[dict[str, str]]:
    section = related_concepts_section(markdown)
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for raw_line in section.splitlines():
        target_match = re.match(r"^\s*-\s+\[\[([^\]]+)\]\]\s*$", raw_line)
        if target_match:
            if current:
                entries.append(current)
            current = {"target": target_match.group(1).strip()}
            continue

        if current is None:
            continue

        field_match = re.match(r"^\s*-\s+(relation|confidence|rationale|source evidence|source_evidence):\s*(.*?)\s*$", raw_line, re.IGNORECASE)
        if field_match:
            key = field_match.group(1).lower().replace(" ", "_")
            current[key] = field_match.group(2).strip()
            continue

        if current.get("rationale") and raw_line.startswith(("    ", "\t")) and raw_line.strip():
            current["rationale"] += " " + raw_line.strip()

    if current:
        entries.append(current)
    return entries


def edge_id(source: str, target: str, relation: str) -> str:
    return f"{source}->{target}:{relation}"


def make_edges(pages: list[Path], nodes: list[dict[str, Any]], lookup: dict[str, str]) -> tuple[list[dict[str, Any]], list[str]]:
    title_by_id = {node["id"]: node["label"] for node in nodes}
    path_by_id = {node["id"]: node["path"] for node in nodes}
    source_by_path = {node["path"]: node["id"] for node in nodes}
    edges: list[dict[str, Any]] = []
    problems: list[str] = []
    seen: set[tuple[str, str, str]] = set()

    for path in pages:
        rel_path = str(path.relative_to(REPO_ROOT)).replace("\\", "/")
        source_id = source_by_path.get(rel_path)
        if not source_id:
            continue

        entries = extract_related_entries(read_text(path))
        for entry in entries:
            raw_target = entry.get("target", "")
            target_id = lookup.get(normalize_lookup_key(raw_target))
            relation = entry.get("relation", "").strip()
            confidence = entry.get("confidence", "").strip().upper()
            rationale = entry.get("rationale", "").strip()

            context = f"{rel_path} -> [[{raw_target}]]"
            if not target_id:
                problems.append(f"Broken wikilink: {context}")
                continue
            if target_id == source_id:
                problems.append(f"Self edge skipped: {context}")
                continue
            if relation not in ALLOWED_RELATIONS:
                problems.append(f"Invalid relation '{relation or '<missing>'}': {context}")
                continue
            if confidence not in ALLOWED_CONFIDENCE:
                problems.append(f"Invalid confidence '{confidence or '<missing>'}': {context}")
                continue
            if not rationale:
                problems.append(f"Missing rationale: {context}")
                continue

            key = (source_id, target_id, relation)
            if key in seen:
                problems.append(f"Duplicate edge skipped: {context} ({relation})")
                continue
            seen.add(key)

            score = CONFIDENCE_SCORES[confidence]
            edges.append({
                "id": edge_id(source_id, target_id, relation),
                "source": source_id,
                "target": target_id,
                "from": source_id,
                "to": target_id,
                "relation": relation,
                "confidence": confidence,
                "confidence_score": score,
                "rationale": rationale,
                "source_evidence": entry.get("source_evidence", ""),
                "source_file": rel_path,
                "weight": score,
                "label": relation,
                "title": f"{title_by_id[source_id]} -> {title_by_id[target_id]}: {relation} [{confidence}]",
                "color": RELATION_COLORS.get(relation, "#999999"),
            })

    return edges, problems


def validate_graph(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> list[str]:
    problems: list[str] = []
    node_ids = {node["id"] for node in nodes}
    for node in nodes:
        if not re.fullmatch(r"[a-z0-9_]+", node["id"]):
            problems.append(f"Invalid node id: {node['id']}")
        if related_concepts_section(node.get("markdown", "")) == "" and node.get("node_type") == "concept":
            problems.append(f"Concept page missing Related Concepts section: {node['path']}")
    for edge in edges:
        if edge["source"] not in node_ids or edge["target"] not in node_ids:
            problems.append(f"Invalid edge endpoint: {edge['source']} -> {edge['target']}")
        if edge["relation"] not in ALLOWED_RELATIONS:
            problems.append(f"Invalid relation in edge: {edge['relation']}")
        if edge["confidence"] not in ALLOWED_CONFIDENCE:
            problems.append(f"Invalid confidence in edge: {edge['confidence']}")
        if not edge.get("rationale"):
            problems.append(f"Missing rationale in edge: {edge['source']} -> {edge['target']}")
    return problems


def build_networkx_graph(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> Any:
    if not HAS_NETWORKX:
        return None
    graph = nx.Graph()
    for node in nodes:
        graph.add_node(
            node["id"],
            label=node["label"],
            node_type=node["node_type"],
            concept_type=node.get("concept_type", ""),
            source_file=node["source_file"],
            file_type=node["node_type"],
            preview=node["preview"],
            markdown=node["markdown"],
            path=node["path"],
        )
    for edge in edges:
        graph.add_edge(
            edge["source"],
            edge["target"],
            relation=edge["relation"],
            confidence=edge["confidence"],
            confidence_score=edge["confidence_score"],
            rationale=edge["rationale"],
            source_evidence=edge.get("source_evidence", ""),
            source_file=edge["source_file"],
            weight=edge["weight"],
            _src=edge["source"],
            _tgt=edge["target"],
        )
    return graph


def detect_communities(graph: Any, nodes: list[dict[str, Any]]) -> dict[int, list[str]]:
    if not HAS_NETWORKX or graph is None or graph.number_of_nodes() == 0:
        return {0: [node["id"] for node in nodes]}
    if graph.number_of_edges() == 0:
        return {idx: [node["id"]] for idx, node in enumerate(nodes)}
    try:
        groups = nx_community.louvain_communities(graph, seed=42)
    except Exception:
        groups = nx_community.greedy_modularity_communities(graph)
    return {idx: sorted(group) for idx, group in enumerate(groups)}


def attach_degrees_and_groups(nodes: list[dict[str, Any]], edges: list[dict[str, Any]], communities: dict[int, list[str]]) -> None:
    degree: dict[str, int] = defaultdict(int)
    for edge in edges:
        degree[edge["source"]] += 1
        degree[edge["target"]] += 1

    node_to_group = {
        node_id: cid
        for cid, members in communities.items()
        for node_id in members
    }
    for node in nodes:
        node["degree"] = degree[node["id"]]
        node["value"] = degree[node["id"]] + 1
        node["group"] = node_to_group.get(node["id"], 0)


def write_json(nodes: list[dict[str, Any]], edges: list[dict[str, Any]], validation: list[str]) -> None:
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        "built": date.today().isoformat(),
        "nodes": nodes,
        "edges": edges,
        "validation": {
            "allowed_relations": sorted(ALLOWED_RELATIONS),
            "allowed_confidence": sorted(ALLOWED_CONFIDENCE),
            "problems": validation,
        },
    }
    GRAPH_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def render_graphify_html(graph: Any, communities: dict[int, list[str]]) -> bool:
    if not HAS_NETWORKX or graph is None:
        return False
    try:
        import sys

        if str(REPO_ROOT) not in sys.path:
            sys.path.insert(0, str(REPO_ROOT))
        import graphify_export

        labels = {cid: f"Community {cid}" for cid in communities}
        renderer = getattr(graphify_export, "to_html_v2", graphify_export.to_html)
        renderer(graph, communities, str(GRAPH_HTML), community_labels=labels)
        return True
    except Exception as exc:
        print(f"  warning: graphify_export renderer unavailable ({exc}); using fallback HTML")
        return False


def render_fallback_html(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> None:
    vis_nodes = [
        {
            "id": node["id"],
            "label": node["label"],
            "color": {"background": node["color"], "border": node["color"]},
            "title": html.escape(f"{node['label']} ({node['node_type']})"),
            "size": 10 + min(node.get("degree", 0), 20),
        }
        for node in nodes
    ]
    vis_edges = [
        {
            "from": edge["source"],
            "to": edge["target"],
            "label": edge["relation"],
            "title": html.escape(f"{edge['relation']} [{edge['confidence']}]\n{edge['rationale']}"),
            "arrows": "to",
            "color": {"color": edge["color"]},
        }
        for edge in edges
    ]
    GRAPH_HTML.write_text(
        f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Snow Tire Knowledge Graph</title>
<script src="https://unpkg.com/vis-network@9.1.6/standalone/umd/vis-network.min.js"></script>
<style>
body {{ margin: 0; background: #0f0f1a; color: #e0e0e0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; display: flex; height: 100vh; overflow: hidden; }}
#graph {{ flex: 1; }}
#sidebar {{ width: 280px; background: #1a1a2e; border-left: 1px solid #2a2a4e; padding: 14px; font-size: 13px; }}
#search {{ width: 100%; background: #0f0f1a; border: 1px solid #3a3a5e; color: #e0e0e0; padding: 7px 10px; border-radius: 6px; }}
</style>
</head>
<body>
<div id="graph"></div>
<div id="sidebar">
  <input id="search" placeholder="Search nodes..." autocomplete="off">
  <p>{len(nodes)} nodes &middot; {len(edges)} edges</p>
  <div id="info">Click a node to inspect it.</div>
</div>
<script>
const rawNodes = {json.dumps(vis_nodes, ensure_ascii=False)};
const rawEdges = {json.dumps(vis_edges, ensure_ascii=False)};
const nodes = new vis.DataSet(rawNodes);
const edges = new vis.DataSet(rawEdges);
const network = new vis.Network(document.getElementById("graph"), {{nodes, edges}}, {{
  physics: {{ solver: "forceAtlas2Based", stabilization: {{ iterations: 200 }} }},
  interaction: {{ hover: true, tooltipDelay: 100 }},
  nodes: {{ shape: "dot", font: {{ color: "#ffffff" }} }},
  edges: {{ smooth: {{ type: "continuous" }}, arrows: {{ to: {{ enabled: true, scaleFactor: 0.5 }} }} }},
}});
const nodeMap = new Map(rawNodes.map(n => [n.id, n]));
network.on("click", params => {{
  if (!params.nodes.length) return;
  const node = nodeMap.get(params.nodes[0]);
  document.getElementById("info").innerHTML = `<b>${{node.label}}</b><br><code>${{node.id}}</code>`;
}});
document.getElementById("search").addEventListener("input", event => {{
  const q = event.target.value.toLowerCase();
  const found = rawNodes.find(n => n.label.toLowerCase().includes(q));
  if (found) network.focus(found.id, {{ scale: 1.4, animation: true }});
}});
</script>
</body>
</html>""",
        encoding="utf-8",
    )


def build_graph(open_browser: bool = False, report: bool = False) -> int:
    pages = wiki_pages()
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Building graph from {len(pages)} wiki pages...")
    nodes, lookup, lookup_warnings = make_nodes(pages)
    edges, edge_problems = make_edges(pages, nodes, lookup)
    validation = lookup_warnings + edge_problems + validate_graph(nodes, edges)

    graph = build_networkx_graph(nodes, edges)
    communities = detect_communities(graph, nodes)
    attach_degrees_and_groups(nodes, edges, communities)

    write_json(nodes, edges, validation)
    html_ok = render_graphify_html(graph, communities)
    if not html_ok:
        render_fallback_html(nodes, edges)

    print(f"  saved: {GRAPH_JSON.relative_to(REPO_ROOT)} ({len(nodes)} nodes, {len(edges)} edges)")
    print(f"  saved: {GRAPH_HTML.relative_to(REPO_ROOT)}")
    if validation:
        print(f"  validation: {len(validation)} problem(s)")
        for problem in validation:
            print(f"    - {problem}")
    else:
        print("  validation: ok")

    if report:
        print("\nGraph report")
        print(f"- nodes: {len(nodes)}")
        print(f"- edges: {len(edges)}")
        print(f"- communities: {len(communities)}")
        print(f"- validation problems: {len(validation)}")

    if open_browser:
        webbrowser.open(f"file://{GRAPH_HTML.resolve()}")

    return 0 if not validation else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Build snow tire knowledge graph")
    parser.add_argument("--open", action="store_true", help="Open graph.html in a browser")
    parser.add_argument("--report", action="store_true", help="Print a graph report")
    parser.add_argument("--no-infer", action="store_true", help="Accepted for compatibility; inference is not used")
    parser.add_argument("--clean", action="store_true", help="Accepted for compatibility; no cache is used")
    parser.add_argument("--save", action="store_true", help="Accepted for compatibility")
    args = parser.parse_args()
    return build_graph(open_browser=args.open, report=args.report)


if __name__ == "__main__":
    raise SystemExit(main())
