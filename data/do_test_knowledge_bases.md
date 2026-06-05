---
title: How to Test DigitalOcean Knowledge Bases
description: Test retrieval results, update chunking strategy, and use the Knowledge Base API to query knowledge base data.
product: Knowledge Bases
url: https://docs.digitalocean.com/products/knowledge-bases/how-to/test-knowledge-bases/
last_updated: "2026-04-15"
---

> **For AI agents:** The documentation index is at [https://docs.digitalocean.com/llms.txt](https://docs.digitalocean.com/llms.txt). Markdown versions of pages use the same URL with `index.html.md` in place of the HTML page (for example, append `index.html.md` to the directory path instead of opening the HTML document).

# How to Test DigitalOcean Knowledge Bases

DigitalOcean Knowledge Bases let you store, index, and retrieve data from private files, websites, Spaces buckets, and other sources to power retrieval-augmented generation with your own content.

## Test Chunking Strategy

Chunking quality depends on document structure and formatting. To improve chunking, test retrieval results by [running retrieval queries](https://docs.digitalocean.com/products/knowledge-bases/how-to/test-knowledge-bases/index.html.md#retrieve-control) or, if the knowledge base is attached to an AI agent, by running [agent evaluations](https://docs.digitalocean.com/products/inference/how-to/evaluate-agents/index.html.md).

To change chunking settings, [delete the data source](https://docs.digitalocean.com/products/knowledge-bases/how-to/manage-data-sources/index.html.md#remove-data-control), and then [add it again with the new chunking configuration](https://docs.digitalocean.com/products/knowledge-bases/how-to/manage-data-sources/index.html.md#add-data-control).

Since each indexing job consumes tokens, choose chunking settings carefully. For reference, semantic and hierarchical chunking can increase token usage, while section-based and fixed length chunking offer more predictable costs. For details on chunking costs, see [knowledge base pricing](https://docs.digitalocean.com/products/knowledge-bases/details/pricing/index.html.md#knowledge-bases).

## Test Reranking

Reranking can improve retrieval relevance by reordering results after the initial search so the most relevant chunks are more likely to appear first. To evaluate its impact, test retrieval results in the Control Panel, compare outputs with and without reranking enabled, and adjust the setting based on answer quality and cost.

To check and enable reranking, [go to the knowledge base’s **Settings** tab](https://docs.digitalocean.com/products/knowledge-bases/how-to/edit-knowledge-bases/index.html.md#edit-reranking).

Once reranking is enabled, reranking tokens are billed separately from vectorizing retrieval queries. For more information, see [knowledge base pricing](https://docs.digitalocean.com/products/knowledge-bases/details/pricing/index.html.md#knowledge-bases).

To test your reranking model, you can [send queries to your knowledge base in the Control Panel](https://docs.digitalocean.com/products/knowledge-bases/how-to/test-knowledge-bases/index.html.md#retrieve-control), [use the DigitalOcean API](https://docs.digitalocean.com/products/knowledge-bases/how-to/test-knowledge-bases/index.html.md#retrieve-api), or [test retrieval and responses in RAG Playground](https://docs.digitalocean.com/products/knowledge-bases/how-to/test-knowledge-base-retrieval/index.html.md).

## Retrieve Data from a Knowledge Base Using the Control Panel

Retrieve data from a knowledge base to test how well it returns relevant content for semantic, keyword, or hybrid searches. Results are returned as chunks, which are smaller sections of your source content along with any metadata attached during ingestion, such as category, product, source, or page information.

To retrieve data from a knowledge base, go to the [Control Panel](https://cloud.digitalocean.com), in the left menu, click **DATA SERVICES**, and then click the **Knowledge Bases** tab.

Then, click the knowledge base you want to query, and then click its **Retrieve** tab.

To enable reranking, [go to the knowledge base’s **Settings** tab](https://docs.digitalocean.com/products/knowledge-bases/how-to/test-knowledge-bases/index.html.md#test-reranking). This means retrieved results are reordered by the reranking model to improve relevance.

If you want to disable reranking for one query, [go to the knowledge base’s **Settings** tab](https://docs.digitalocean.com/products/knowledge-bases/how-to/edit-knowledge-bases/index.html.md#edit-reranking), and click **Disable reranking**.

In the **Search query** field, type the text you want to search for.

In the **num_results** field, set how many results to return.

You can run one of the following search types against your knowledge base using the **alpha** field:

- **Semantic search**: Finds results by meaning, even when the exact words do not match. Best for conversational or open-ended queries. Set `alpha: 1`.
- **Keyword search**: Finds results by exact word matches. Best for precise terms such as names, dates, IDs, or product codes. Set `alpha: 0`.
- **Hybrid search**: Combines semantic and keyword search in one result set. Best as the default for most queries. Start with `alpha: 0.5`, and then tune lower for more exact matching or higher for more meaning-based matching.

An **alpha** value of `0` uses keyword retrieval, a value of `1` uses semantic retrieval, and values in between use hybrid retrieval.

Under the **Filters (optional)** tab, you can combine filters with **and_all**, which returns only chunks that match every condition, or **or_all**, which returns chunks that match at least one condition.

You can filter results by first clicking the **Category** dropdown list and choosing one of the following chunk metadata fields:

- **item_name**: The source item name, such as a file name or URL path. For example, `https://docs.digitalocean.com/products/inference/`.
- **ingested_timestamp**: The date and time when the chunk was ingested into the knowledge base. For example, `2025-12-01T00:00:00Z`.
- **page_number**: The page number of the source document, when available. For example, `3`.
- **chunk_category**: The category assigned to the chunk during processing, such as the extracted content type.

Then, click the condition dropdown to choose one of the following:

- **equals**: Returns chunks where the field exactly matches the value. We recommend using this with **item_name** to target a specific file or URL, or with **chunk_category** when you want only one specific chunk type.
- **not_equals**: Excludes chunks where the field exactly matches the value.
- **greater_than**: Returns chunks where the field value is greater than the value you enter. We recommend using this with **ingested_timestamp** or **page_number** to filter by date or page range.
- **greater_than_or_equals**: Returns chunks where the field value is greater than or equal to the value you enter. We recommend using this with **ingested_timestamp** or **page_number** to filter by date or page range.
- **less_than**: Returns chunks where the field value is less than the value you enter. We recommend using this with **ingested_timestamp** or **page_number** to filter by date or page range.

Then, in the **Value** field, enter the value for the filter.

To add a filter, click the **+ Add condition**. If you want to delete a filter, on the right of the filter condition, click **x**.

After setting up your search query, click **Retrieve**.

The **Results** section shows the total number of results retrieved, the query time in milliseconds (ms), the **alpha** value, and each retrieved chunk with its source file, page number when available, category metadata, and relevance score when available. Higher-relevance chunks are visually emphasized to help you spot the strongest matches more quickly.

If needed, you can also compare how different models answer questions using retrieved knowledge base content in the [RAG Playground](https://docs.digitalocean.com/products/knowledge-bases/how-to/test-knowledge-base-retrieval/index.html.md).

### Use Code Snippets to Retrieve Data

Use the code snippets to turn your current retrieval settings into working API requests for testing, automation, or application development. This lets you reuse the same query, filters, and retrieval settings outside the Control Panel without writing the request from scratch.

To use the live auto-generated code snippets for the Gradient SDK (Python) or cURL based on your current query settings, click the **Retrieve Endpoint** tab, select the snippet you want from the code snippet dropdown list, and then click **Copy** to paste it where you need it or **Download** to save it.

## Retrieve Data from a Knowledge Base Using the Knowledge Base API

You can query a knowledge base to retrieve the most relevant chunks, along with metadata, scores, and any hierarchical context. The knowledge base retrieve API is available at `https://kbaas.do-ai.run` and has the following endpoint:

| Endpoint | Verb | Description |
|---|---|---|
| `/v1/<knowledge-base-uuid>/retrieve` | POST | Retrieves the most relevant chunks from a knowledge base using hybrid retrieval, combining keyword-based lexical retrieval with embedding-based semantic retrieval (and optional metadata filters). |

Data retrieval depends on how the knowledge base was configured and how the request is sent:

- **Chunking** affects how content is split during indexing, which can affect retrieval results. Chunking is configured when you [create or update a knowledge base data source](https://docs.digitalocean.com/products/knowledge-bases/how-to/test-knowledge-bases/index.html.md#test-chunk), not during retrieval.
- **Reranking** optionally improves the ordering of retrieved results. If reranking is enabled for the knowledge base, you can disable it for an individual retrieval request.

You can also call the retrieve endpoint using the [Gradient SDK](https://gradient-sdk.digitalocean.com/api/python/resources/retrieve/methods/documents).

To retrieve chunks from a knowledge base, send a POST request to `/v1/<knowledge-base-uuid>/retrieve` using your DigitalOcean API token. Requests to the retrieve API require a DigitalOcean API token created from the [**Settings** page](https://cloud.digitalocean.com/account/api/tokens) with the `GenAI:read` scope enabled.

You can include the following fields in the request body:

- `query`: Specifies the search query string.
- `num_results`: Defines the number between 0 and 100 of results to return.
- `alpha`: Controls the balance between lexical and semantic retrieval. Values range from `0` (lexical only) to `1` (semantic only). We recommend setting lower values for structured or technical queries, higher values for conversational or exploratory queries, and mid-range values for balanced precision and recall.
- `reranking`: Optionally controls reranking behavior for the request. Use this to disable reranking for an individual retrieval request.
- `filters`: Optionally narrows results by matching chunk metadata, such as:

  - `item_name`: The source item name, such as a file name or URL path.
  - `ingested_timestamp`: The date and time when the chunk was ingested into the knowledge base.
  - `page_number`: The page number of the source document, when available.
  - `chunk_category`: The category assigned to the chunk during processing.

  Supported operations include:

  - `equals`: Matches values exactly. We recommend using this with `item_name` to target a specific file or URL, or with `chunk_category` to return one specific chunk type.
  - `not_equals`: Excludes exact matches.
  - `greater_than`: Matches values greater than the input. We recommend using this with `ingested_timestamp` or `page_number` to filter by date or page range.
  - `greater_than_or_equals`: Matches values greater than or equal to the input. We recommend using this with `ingested_timestamp` or `page_number` to filter by date or page range.
  - `less_than`: Matches values less than the input. We recommend using this with `ingested_timestamp` or `page_number` to filter by date or page range.
  - `less_than_or_equals`: Matches values less than or equal to the input. We recommend using this with `ingested_timestamp` or `page_number` to filter by date or page range.
  - `starts_with`: Matches text values that begin with the input. We recommend using this with `item_name` to restrict results to a specific file, URL, or path prefix.

  Combine filters with `and_all` to match all conditions or `or_all` to match any condition. You can also nest groups for more complex logic.

The following example shows a hybrid retrieval request with no filters:

```bash
curl --location 'https://kbaas.do-ai.run/v1/<knowledge-base-uuid>/retrieve' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer $DO_API_TOKEN' \
--data '{
    "query": "How do I build an agent on DigitalOcean?",
    "num_results": 5,
    "alpha": 0.5
}'
```

When using `filters`, the `key` must reference a metadata field in the dataset, and the `value` must match the field type, such as string, number, or boolean. Use operators compatible with the field type. For example, avoid `greater_than` on string fields unless they use a supported date or version format.

The following example uses `or_all` filter to return chunks where the source path starts with a specific documentation URL or the chunk was ingested on or after a specified date:

```bash
curl --location 'https://kbaas.do-ai.run/v1/<knowledge-base-uuid>/retrieve' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer $DO_API_TOKEN' \
--data '{
    "query": "How do I build an agent on DigitalOcean",
    "num_results": 5,
    "filters": {
        "or_all": [
            {
                "starts_with": {
                    "key": "item_name",
                    "value": "https://docs.digitalocean.com/products/inference/"
                },
                "greater_than_or_equals": {
                    "key": "ingested_timestamp",
                    "value": "2025-12-01"
                }
            }
        ]
    },
    "alpha": 0.5
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
                "item_name": "https://docs.digitalocean.com/products/inference/how-to/create-agents/",
            },
            "text_content": "Chunk 1 Content"
        },
        {
            "metadata": {
                "chunk_category": "CompositeElement",
                "ingested_timestamp": "2025-12-15T15:23:19.191428+00:00",
                "item_name": "https://docs.digitalocean.com/products/inference/how-to/use-serverless-inference/",
            },
            "text_content": "Chunk2 content"
        },
        ...
    ],
    "total_results": 5
}
```

Enable reranking for the request by setting the `enabled` parameter in `reranking` to `true` (or `false`).

The following example enables reranking for a hybrid retrieval request:

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

The following example shows a reranked response returned by the knowledge base API endpoint:

```json
{
    "results": [
        {
            "metadata": {
                "chunk_category": "CompositeElement",
                "ingested_timestamp": "2025-12-15T15:23:19.191428+00:00",
                "item_name": "https://docs.digitalocean.com/products/inference/how-to/create-agents/"
            },
            "text_content": "Chunk 1 content"
        },
        {
            "metadata": {
                "chunk_category": "CompositeElement",
                "ingested_timestamp": "2025-12-15T15:23:19.191428+00:00",
                "item_name": "https://docs.digitalocean.com/products/inference/how-to/use-serverless-inference/"
            },
            "text_content": "Chunk 2 content"
        }
    ],
    "total_results": 5
    ...
}
```