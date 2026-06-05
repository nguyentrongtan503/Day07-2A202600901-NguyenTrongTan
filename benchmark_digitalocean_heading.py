from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Callable

from src import Document, EmbeddingStore, MarkdownHeadingChunker


DATASET = [
    {
        "path": "data/do_retrieval_best_practices.md",
        "doc_id": "do_retrieval_best_practices",
        "url": "https://docs.digitalocean.com/products/knowledge-bases/concepts/data-services-retrieval/",
        "category": "retrieval",
        "doc_type": "concept",
        "audience": "developer",
    },
    {
        "path": "data/do_chunking_best_practices.md",
        "doc_id": "do_chunking_best_practices",
        "url": "https://docs.digitalocean.com/products/knowledge-bases/concepts/data-services-chunking-strategies/",
        "category": "chunking",
        "doc_type": "concept",
        "audience": "developer",
    },
    {
        "path": "data/do_system_instructions_best_practices.md",
        "doc_id": "do_system_instructions_best_practices",
        "url": "https://docs.digitalocean.com/products/knowledge-bases/concepts/data-services-system-instructions/",
        "category": "prompting",
        "doc_type": "concept",
        "audience": "developer",
    },
    {
        "path": "data/do_create_knowledge_bases.md",
        "doc_id": "do_create_knowledge_bases",
        "url": "https://docs.digitalocean.com/products/knowledge-bases/how-to/create/",
        "category": "setup",
        "doc_type": "how_to",
        "audience": "operator",
    },
    {
        "path": "data/do_test_knowledge_bases.md",
        "doc_id": "do_test_knowledge_bases",
        "url": "https://docs.digitalocean.com/products/knowledge-bases/how-to/test-knowledge-bases/",
        "category": "evaluation",
        "doc_type": "how_to",
        "audience": "operator",
    },
]


BENCHMARKS = [
    {
        "query": "What are DigitalOcean's recommended best practices for a strong retrieval setup?",
        "filter": {"category": "retrieval"},
        "expected_categories": {"retrieval"},
    },
    {
        "query": "Why can chunks that are too small or too large hurt retrieval quality?",
        "filter": {"category": "chunking"},
        "expected_categories": {"chunking", "retrieval"},
    },
    {
        "query": "When should filters be used in knowledge base retrieval?",
        "filter": {"category": "retrieval"},
        "expected_categories": {"retrieval"},
    },
    {
        "query": "What is the difference between chunking, retrieval, and reranking in a RAG system?",
        "filter": None,
        "expected_categories": {"retrieval", "chunking"},
    },
    {
        "query": "How should a team test whether a knowledge base returns useful answers?",
        "filter": {"category": "evaluation"},
        "expected_categories": {"evaluation"},
    },
]


VOCABULARY = [
    "retrieval",
    "retrieve",
    "chunk",
    "chunking",
    "reranking",
    "rerank",
    "filter",
    "filters",
    "metadata",
    "semantic",
    "keyword",
    "hybrid",
    "test",
    "testing",
    "knowledge",
    "base",
    "agent",
    "context",
    "answer",
    "source",
    "document",
    "files",
    "search",
    "query",
    "quality",
    "small",
    "large",
]


class SimpleKeywordEmbedder:
    """Small classroom embedder for transparent benchmark runs."""

    def __init__(self, vocabulary: list[str]) -> None:
        self.vocabulary = vocabulary
        self._backend_name = "simple keyword embedder"

    def __call__(self, text: str) -> list[float]:
        tokens = re.findall(r"[a-z0-9]+", text.lower())
        counts = {term: 0 for term in self.vocabulary}
        for token in tokens:
            if token in counts:
                counts[token] += 1
        vector = [float(counts[term]) for term in self.vocabulary]
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]


def summarize(text: str, max_len: int = 120) -> str:
    compact = " ".join(text.split())
    return compact if len(compact) <= max_len else compact[: max_len - 3] + "..."


def extract_heading(chunk: str) -> str:
    for line in chunk.splitlines():
        if re.match(r"^#{1,3}\s+", line):
            return line.lstrip("#").strip()
    return "No heading"


def build_chunk_documents() -> list[Document]:
    chunker = MarkdownHeadingChunker(max_chunk_size=900, fallback_chunk_size=700)
    documents: list[Document] = []

    for item in DATASET:
        path = Path(item["path"])
        content = path.read_text(encoding="utf-8")
        chunks = chunker.chunk(content)

        for index, chunk in enumerate(chunks, start=1):
            metadata = {
                "doc_id": item["doc_id"],
                "source": "DigitalOcean Docs",
                "url": item["url"],
                "category": item["category"],
                "doc_type": item["doc_type"],
                "language": "en",
                "audience": item["audience"],
                "chunk_strategy": "markdown_heading",
                "chunk_index": index,
                "heading": extract_heading(chunk),
            }
            documents.append(
                Document(
                    id=f"{item['doc_id']}_chunk_{index}",
                    content=chunk,
                    metadata=metadata,
                )
            )

    return documents


def run_benchmark(print_fn: Callable[[str], None] = print) -> None:
    documents = build_chunk_documents()
    store = EmbeddingStore(
        collection_name="digitalocean_heading_benchmark",
        embedding_fn=SimpleKeywordEmbedder(VOCABULARY),
    )
    store.add_documents(documents)

    print_fn("=== Document Inventory ===")
    for item in DATASET:
        path = Path(item["path"])
        chars = len(path.read_text(encoding="utf-8"))
        count = sum(1 for doc in documents if doc.metadata["doc_id"] == item["doc_id"])
        print_fn(f"{item['doc_id']}: chars={chars}, heading_chunks={count}, category={item['category']}")

    print_fn("\n=== Benchmark Results: Markdown Heading Chunker ===")
    relevant_top3 = 0
    for index, benchmark in enumerate(BENCHMARKS, start=1):
        if benchmark["filter"]:
            results = store.search_with_filter(
                benchmark["query"],
                top_k=3,
                metadata_filter=benchmark["filter"],
            )
        else:
            results = store.search(benchmark["query"], top_k=3)

        has_relevant = any(
            result["metadata"]["category"] in benchmark["expected_categories"]
            for result in results
        )
        relevant_top3 += int(has_relevant)

        print_fn(f"\nQ{index}: {benchmark['query']}")
        print_fn(f"Filter: {benchmark['filter'] or 'none'}")
        for rank, result in enumerate(results, start=1):
            metadata = result["metadata"]
            relevant = metadata["category"] in benchmark["expected_categories"]
            print_fn(
                f"  {rank}. score={result['score']:.3f}, relevant={relevant}, "
                f"category={metadata['category']}, heading={metadata['heading']}"
            )
            print_fn(f"     {summarize(result['content'])}")

    print_fn(f"\nRelevant in top-3: {relevant_top3} / {len(BENCHMARKS)}")


if __name__ == "__main__":
    run_benchmark()
