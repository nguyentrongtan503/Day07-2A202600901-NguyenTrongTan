---
title: DigitalOcean Knowledge Base Retrieval Best Practices
description: Guidance for improving knowledge base retrieval with hybrid search, chunking, filters, and reranking.
product: Knowledge Bases
url: https://docs.digitalocean.com/products/knowledge-bases/concepts/data-services-retrieval/
last_updated: "2026-04-23"
---

> **For AI agents:** The documentation index is at [https://docs.digitalocean.com/llms.txt](https://docs.digitalocean.com/llms.txt). Markdown versions of pages use the same URL with `index.html.md` in place of the HTML page (for example, append `index.html.md` to the directory path instead of opening the HTML document).

# DigitalOcean Knowledge Base Retrieval Best Practices

DigitalOcean Knowledge Bases let you store, index, and retrieve data from private files, websites, Spaces buckets, and other sources to power retrieval-augmented generation with your own content.

[Knowledge base retrieval](https://docs.digitalocean.com/products/knowledge-bases/how-to/test-knowledge-bases/index.html.md#retrieve-control) returns the closest matching chunks as context for an LLM. It does not determine whether the retrieved content fully answers the question, so pass the results to an LLM with clear instructions for final response generation. For system instructions best practices, see [System Instructions Best Practices](https://docs.digitalocean.com/products/knowledge-bases/concepts/data-services-system-instructions/index.html.md).

We recommend the following best practices for a strong retrieval setup:

- Balance semantic and keyword search for your query type.
- Use filters to narrow retrieval to specific files, documents, or URL paths.
- Test chunking if results are incomplete, fragmented, or noisy.
- Enable reranking when relevant chunks exist but need better ordering.

Treat chunking, retrieval, and reranking as separate layers of the same system: chunking shapes the indexed data, retrieval selects candidate chunks, and reranking improves their final order before the results are passed to an LLM.

## Use Hybrid Retrieval

Retrieval quality depends on how your data was chunked during indexing. If chunks are too small, results may be fragmented. If chunks are too large, results may include unrelated content.

We recommend using hybrid retrieval as the default for both the Control Panel and retrieve API. Pure semantic search (`alpha=1`) can drift too far from the exact query, while pure keyword search (`alpha=0`) can miss relevant content when users use synonyms. Set `alpha` values around `0.5` to `0.7` for balanced precision and recall.

For more guidance on using chunking strategies to improve knowledge base retrieval, see [Chunking Strategy Best Practices](https://docs.digitalocean.com/products/knowledge-bases/concepts/data-services-chunking-strategies/index.html.md).

## Use Filters

Use filters to limit retrieval to specific documents, files, metadata, or URL paths. We recommend using filter logic such as `must`, `must_not`, and `should`:

- Use `starts_with` to restrict results to a certain section in your content or URL path rather than searching the entire knowledge base when you only need one document or section.
- Use `equals` to target a specific file or source instead of relying on broad queries to find precise content.
- Combine filters to narrow results to relevant metadata to avoid retrieving irrelevant sources.

Below is an example of a retrieval request scoped to a specific documentation path using the `starts_with` filter:

```bash
curl --location 'https://kbaas.do-ai.run/v1/<knowledge-base-uuid>/retrieve' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer $DO_API_TOKEN' \
--data '{
  "query": "How do I build an agent on DigitalOcean?",
  "num_results": 5,
  "alpha": 0.5,
  "filters": {
    "starts_with": {
      "key": "item_name",
      "value": "https://docs.digitalocean.com/products/inference/"
    }
  }
}'
```

For more information on using filters with your retrieval queries, see [Retrieve data from a knowledge base](https://docs.digitalocean.com/products/knowledge-bases/how-to/test-knowledge-bases/index.html.md#retrieve-control).

## Enable Reranking

Enable reranking when relevant chunks are present but not ordered well:

- Enable reranking when multiple relevant chunks exist and ranking quality matters.
- Compare results with and without reranking to confirm it improves relevance. This validates your retrieval’s quality, latency, or cost impact.
- Use reranking after retrieval is already returning the right candidate set.

Below is an example of a retrieval request with reranking enabled:

```bash
curl --location 'https://kbaas.do-ai.run/v1/<knowledge-base-uuid>/retrieve' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer $DO_API_TOKEN' \
--data '{
  "query": "How do I build an agent on DigitalOcean?",
  "num_results": 5,
  "alpha": 0.5,
  "reranking": {
    "enabled": true
  }
}'
```

For more information on enabling and using reranking in your retrieval queries, see [Test reranking](https://docs.digitalocean.com/products/knowledge-bases/how-to/test-knowledge-bases/index.html.md#test-reranking).

## Retrieval Example

The following example shows a balanced retrieval request that uses hybrid search, scopes results to a docs path, and enables reranking:

```bash
curl --location 'https://kbaas.do-ai.run/v1/<knowledge-base-uuid>/retrieve' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer $DO_API_TOKEN' \
--data '{
  "query": "How do I build an agent on DigitalOcean?",
  "num_results": 5,
  "alpha": 0.5,
  "filters": {
    "starts_with": {
      "key": "item_name",
      "value": "https://docs.digitalocean.com/products/inference/"
    }
  },
  "reranking": {
    "enabled": true
  }
}'
```

The following example shows a response returned by the knowledge base API endpoint:

```json
{
  "results": [
    {
      "metadata": {
        "chunk_category": "CompositeElement",
        "ingested_timestamp": "2025-12-15T15:23:19.191428+00:00",
        "item_name": "https://docs.digitalocean.com/products/inference/how-to/create-agents/"
      },
      "text_content": "To create an agent from the DigitalOcean Control Panel, in the left menu, click Agent Platform to go to the Agent Workspaces tab."
    },
    {
      "metadata": {
        "chunk_category": "CompositeElement",
        "ingested_timestamp": "2025-12-15T15:23:19.191428+00:00",
        "item_name": "https://docs.digitalocean.com/products/inference/how-to/attach-agent-knowledge-bases/"
      },
      "text_content": "You can attach knowledge bases to give agents access to additional custom data, or detach them if the information is no longer needed."
    }
  ],
  "total_results": 2
}
```