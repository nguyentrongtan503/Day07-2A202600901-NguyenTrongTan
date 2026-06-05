---
title: Chunking Best Practices for DigitalOcean Knowledge Base Indexing
description: Choose and configure chunking strategies to improve retrieval accuracy, reduce hallucinations, and optimize token usage when indexing knowledge bases.
product: Knowledge Bases
url: https://docs.digitalocean.com/products/knowledge-bases/concepts/data-services-chunking-strategies/
last_updated: "2026-04-15"
---

> **For AI agents:** The documentation index is at [https://docs.digitalocean.com/llms.txt](https://docs.digitalocean.com/llms.txt). Markdown versions of pages use the same URL with `index.html.md` in place of the HTML page (for example, append `index.html.md` to the directory path instead of opening the HTML document).

# Chunking Best Practices for DigitalOcean Knowledge Base Indexing

DigitalOcean Knowledge Bases let you store, index, and retrieve data from private files, websites, Spaces buckets, and other sources to power retrieval-augmented generation with your own content.

Chunking splits your documents into smaller, retrievable units before indexing. The chunking strategy you choose affects retrieval accuracy, indexing cost, and how much context your agent receives during inference. We support several chunking strategies, each configurable per data source.

This guide explains how to choose and tune chunking strategies. For parameter details, model-specific ranges, and recommendations, see the [chunking parameters reference](https://docs.digitalocean.com/products/knowledge-bases/reference/data-services-chunking-strategies/index.html.md) and the [embeddings model catalog](https://docs.digitalocean.com/products/knowledge-bases/details/knowledge-base-models/index.html.md#embeddings-models). For cost details, see [knowledge base pricing](https://docs.digitalocean.com/products/knowledge-bases/details/pricing/index.html.md#knowledge-bases).

## General Best Practices

We recommend the following:

- Start with the default chunking settings, which work well for most documents.
- Configure chunking per data source and mix strategies within the same knowledge base.
- Consider [indexing and storage costs](https://docs.digitalocean.com/products/knowledge-bases/details/pricing/index.html.md#knowledge-bases) when choosing a strategy, as different chunking methods consume tokens differently.

## Choose Chunking Strategy

Chunking strategies can affect indexing and retrieval costs. Semantic chunking may increase indexing cost, while hierarchical chunking may increase retrieval cost because it returns parent and child chunks together. For parameter recommendations, see the [parameters reference](https://docs.digitalocean.com/products/knowledge-bases/reference/data-services-chunking-strategies/index.html.md).

The sections below explain when to use each strategy and how each one behaves during indexing.

### Section-Based Chunking

Uses structural elements such as headings, paragraphs, lists, tables, and callouts as natural boundaries. Adjacent sections are merged or split based on the maximum chunk size (`max_chunk_size`). Section-based chunking produces predictable, readable chunks.

Works best for:

- Product documentation
- Policies and SOPs
- FAQs
- Blogs
- Structured web content
- Markdown files

Choose this strategy if:

- Your document is already structured and has natural boundaries such as headings, paragraphs, lists, or tables.
- You need predictable, readable chunks.
- You want a fast, low-cost option.
- You want a strong baseline for structured content.

For more information, see the [section-based chunking reference](https://docs.digitalocean.com/products/knowledge-bases/reference/data-services-chunking-strategies/index.html.md#section) and the [pricing page](https://docs.digitalocean.com/products/knowledge-bases/details/pricing/index.html.md#knowledge-bases).

### Semantic Chunking

Groups text by meaning using the chosen embeddings model. It performs two embedding passes:

- Detects semantic boundaries (`semantic_threshold`).
- Embeds the final chunks (`max_chunk_size`).

Semantic chunking produces more semantically aligned chunks, especially for documents without strong formatting.

Use when meaning matters more than formatting.

Works best for:

- Academic writing
- Research notes
- Long-form prose
- Dense or inconsistently structured content

Choose this strategy if:

- Your document groups content based on semantic similarity.
- You need to detect topical shifts even when formatting is poor.
- You need more accurate boundaries that reflect shifts in meaning.
- You can accept higher indexing cost; semantic chunking may increase cost by 1.5 to 3 times compared to other strategies.

For more information, see the [semantic chunking reference](https://docs.digitalocean.com/products/knowledge-bases/reference/data-services-chunking-strategies/index.html.md#semantic) and the [pricing page](https://docs.digitalocean.com/products/knowledge-bases/details/pricing/index.html.md#knowledge-bases).

### Hierarchical Chunking

Creates a two-level structure consisting of:

- Parent chunks for broad context (`parent_chunk_size`).
- Child chunks for precise retrieval (`child_chunk_size`).

When a child chunk is retrieved, the system automatically includes its parent chunk to improve grounding.

Use when both broad context and precise retrieval are required.

Works best for:

- API reference documentation
- Legal contracts
- Product manuals
- Highly structured technical content
- Documents requiring long-context reasoning

Choose this strategy if:

- You need both precise retrieval and broader contextual grounding.

Hierarchical chunking has indexing costs similar to section-based strategies, but retrieval costs are higher because parent and child chunks are included together.

For more information, see the [hierarchical chunking reference](https://docs.digitalocean.com/products/knowledge-bases/reference/data-services-chunking-strategies/index.html.md#hierarchical) and the [pricing page](https://docs.digitalocean.com/products/knowledge-bases/details/pricing/index.html.md#knowledge-bases).

### Fixed Length Chunking

Splits text strictly by token count, ignoring formatting or meaning. This produces uniform chunk sizes and predictable indexing behavior.

Use when the document has unreliable formatting or when simplicity is preferred.

Works best for:

- Logs
- IoT telemetry
- OCR text
- Time-series or streaming text
- Machine-generated content
- Code
- Highly structured or repetitive data

Choose this strategy if:

- You want chunking based solely on token count.
- You can ignore document formatting and semantics.
- You need a fast, predictable behavior.
- You are indexing large-scale, unstructured, or repetitive content.

For more information, see the [fixed length chunking reference](https://docs.digitalocean.com/products/knowledge-bases/reference/data-services-chunking-strategies/index.html.md#fixed) and the [pricing page](https://docs.digitalocean.com/products/knowledge-bases/details/pricing/index.html.md#knowledge-bases).

## Improve Chunking Performance

Chunking performance depends heavily on document clarity and formatting. To improve retrieval quality, follow these best practices:

- Start with the default chunking settings before tuning parameters.
- Test retrieval using the [knowledge base retrieval](https://docs.digitalocean.com/products/knowledge-bases/how-to/test-knowledge-bases/index.html.md#retrieve-control).
- Review retrieval quality using metrics such as context relevance, response-context completeness, context adherence, and retrieved chunk usage.
- Adjust the [chunking strategy or parameters](https://docs.digitalocean.com/products/knowledge-bases/how-to/test-knowledge-bases/index.html.md#test-chunk) only when retrieval results show a clear issue.
- [Re-index the data source](https://docs.digitalocean.com/products/knowledge-bases/how-to/index-data-sources/index.html.md#re-index-control) after changing chunking settings.

If you use the knowledge base with an [agent](https://docs.digitalocean.com/products/inference/index.html.md), test it with [agent evaluations](https://docs.digitalocean.com/products/inference/how-to/evaluate-agents/index.html.md) to measure retrieval accuracy. For metric definitions, see the [agent evaluation metrics reference page](https://docs.digitalocean.com/products/inference/reference/agent-evaluation-metrics/index.html.md).

Re-indexing consumes tokens, so make changes intentionally and avoid repeated small adjustments.