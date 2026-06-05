---
title: How to Create DigitalOcean Knowledge Bases
description: Create a knowledge base by choosing an embeddings model, adding data sources, configuring chunking, and selecting an OpenSearch database.
product: Knowledge Bases
url: https://docs.digitalocean.com/products/knowledge-bases/how-to/create/
last_updated: "2026-04-15"
---

> **For AI agents:** The documentation index is at [https://docs.digitalocean.com/llms.txt](https://docs.digitalocean.com/llms.txt). Markdown versions of pages use the same URL with `index.html.md` in place of the HTML page (for example, append `index.html.md` to the directory path instead of opening the HTML document).

# How to Create DigitalOcean Knowledge Bases

DigitalOcean Knowledge Bases let you store, index, and retrieve data from private files, websites, Spaces buckets, and other sources to power retrieval-augmented generation with your own content.

A knowledge base stores data sources (such as local file uploads, [DigitalOcean Spaces buckets or folders](https://docs.digitalocean.com/products/spaces/index.html.md), public seed or sitemap URLs, [Dropbox](https://www.dropbox.com) folders, and [Amazon S3 buckets](https://aws.amazon.com/s3/)), that AI agents can use to answer questions with retrieval-augmented generation (RAG). RAG helps agents provide more accurate, current, and domain-specific responses.

When you create a knowledge base, your data is immediately indexed by converting the content into vector embeddings using an embeddings model. These embeddings capture the meaning of your content and are stored in a [Managed OpenSearch database](https://docs.digitalocean.com/products/databases/opensearch/index.html.md), which you can [scale to improve performance](https://docs.digitalocean.com/products/databases/opensearch/how-to/resize/index.html.md). The embeddings model determines token limits, chunk size ranges, and whether size estimates are available when you [download the CSV for the indexing job](https://docs.digitalocean.com/products/knowledge-bases/how-to/view-indexing-jobs/index.html.md).

**Note**: Size estimates in the CSV are based on total data size, not extractable text, and are available only for local uploads and Spaces buckets. Other sources show `estimate unavailable`.

Each knowledge base requires at least one data source, and [you can add or remove sources after creation](https://docs.digitalocean.com/products/knowledge-bases/how-to/manage-data-sources/index.html.md#add-data-control).

## Create a Knowledge Base Using the Control Panel

To create a knowledge base, go to the [DigitalOcean Control Panel](https://cloud.digitalocean.com/), in the left menu, click **DATA SERVICES**, and then click **Knowledge Bases**.

Then, in the top-right, click **Create Knowledge Base** to open the **Create a knowledge base** page.

### Choose Your Embeddings Model

Under the **Add data** step, click the **Choose your embeddings model** dropdown list, and choose an embeddings model. You can’t change the model after creating your knowledge base.

An embeddings model converts your data into vector embeddings which are stored in an [OpenSearch database](https://docs.digitalocean.com/products/databases/opensearch/index.html.md). We offer [multiple embeddings models](https://docs.digitalocean.com/products/knowledge-bases/details/knowledge-base-models/index.html.md#embeddings-models) for different use cases. The [indexing costs](https://docs.digitalocean.com/products/knowledge-bases/details/pricing/index.html.md#knowledge-bases) depend on the selected model and the size of your data.

To understand your indexing costs, click **How much will I pay for an indexing job?**. This opens the **Estimating index job costs** window, which shows estimated indexing costs by embeddings model token rate and dataset size. Larger datasets cost more to index, and you only pay for successfully indexed data. Final costs may vary. For details, see [embeddings model pricing](https://docs.digitalocean.com/products/knowledge-bases/details/pricing/index.html.md#knowledge-bases).

### Configure Reranking

You can optionally enable reranking for retrieval results when you create the knowledge base. Reranking reorders results after the initial search so the most relevant chunks are more likely to appear first and be used in generated responses.

If reranking is enabled, reranking tokens are billed separately from vectorizing retrieval queries. For more information, see [knowledge base pricing](https://docs.digitalocean.com/products/knowledge-bases/details/pricing/index.html.md#knowledge-bases).

Under the **Choose your reranking model** section, click the **Reranking model (optional)** dropdown list, and then select a reranking model. Choose a reranking model based on the relevance quality you need, your latency requirements, and [your cost considerations](https://docs.digitalocean.com/products/knowledge-bases/details/pricing/index.html.md#knowledge-bases). You can’t change the reranking model after enabling reranking. To see the reranking models, see our [available reranking models](https://docs.digitalocean.com/products/knowledge-bases/details/knowledge-base-models/index.html.md#reranking-models).

If reranking is enabled, retrieval results show that reranking is active, along with the model name and per-token pricing. Reranking applies to all retrieval requests and incurs charges on each request.

### Add Data Sources

You can add multiple types of data sources and include as many as needed. To save processing time and cost, organize your files in dedicated [Spaces buckets](https://docs.digitalocean.com/products/spaces/index.html.md), specific folders, or local storage containing only relevant files.

To avoid delays, we recommend uploading fewer than 100 files at a time, each under 2 GB. For larger uploads, use the [DigitalOcean API](https://docs.digitalocean.com/products/spaces/reference/index.html.md). If uploads continue to stall, [contact support](https://cloudsupport.digitalocean.com).

In the **Add data sources** section, under the **Select data sources to index** sub-section, select the type of data you want to add.

Knowledge bases support the following text-based file formats: `.csv`, `.eml`, `.epub`, `.xls`, `.xlsx`, `.html`, `.md`, `.odt`, `.pdf`, `.txt`, `.rst`, `.rtf`, `.tsv`, `.doc`, `.docx`, `.xml`, `.json`, and `.jsonl`. When supported files contain embedded media, such as images or SVGs, we also attempt to index that content.

You can add any of the following data sources:

### File Upload

To upload files, click **Upload a file** to open the **Select files to upload** window.

For performance and reliability, we recommend uploading files no larger than 2 GB and uploading fewer than 100 files at a time.

Under the **Choose Files** section, either click **Upload**, or drag-and-drop at least one file.

If you want to add more files, on the bottom right, click **Upload more files**.

If you want to remove a file, on the right of it, click the trash icon.

### Spaces Bucket or Folder

To add a [Spaces bucket or folder](https://docs.digitalocean.com/products/spaces/index.html.md), click **Pull from a Spaces bucket or folder** to open the **Select Spaces bucket or folder** window.

We can index all supported file formats in selected buckets and folders, regardless of privacy settings.

Then, either choose at least one bucket or folder you want to index, or on the left of a bucket, click **+** to expand its contents, and then select specific folders. For optimal performance and indexing quality, we recommend using five or fewer buckets and uploading only indexing data to your buckets.

### Web or Site Map URL

**Note**:

  When you specify a website URL as a data source for your knowledge base, DigitalOcean uses a custom agent named `DigitalOceanGradientAICrawler/1.0` to index the website content. The crawler indexes up to 5,500 pages and skips inaccessible or disallowed links to prevent excessively large indexing jobs.

  Depending on the behavior you select, the crawler follows HTML links on the site, indexes text and certain image types, and ignores videos and navigation links. It respects the website’s `robots.txt` rules, including any `Disallow` directives or the wildcard `*`.

To add a URL for web crawling, click **Add a web or site map URL**. You can then choose to specify a [**Seed URL**](#seed-url) or a [**Site map URL**](#site-map-url).

### Specify Seed URL

Specifying a seed URL crawls only the seed URL and linked pages within the same path, domain, or subdomains.

To specify a seed URL, click **Seed URL**, and then in the **Seed URL** field, enter the public URL you want to crawl.

Under the **Crawling rules** section, select the crawl scope (from most narrow to most broad):

- **Scoped** crawls only the seed URL.
- **URL and all linked pages in path** crawls the seed URL and all pages within the same path.
- **URL and all linked pages in domain** crawls all pages in the same domain.
- **Subdomains** crawls the domain and all its subdomains.

Click the **Index embedded media** option to index supported images and other media encountered during the crawl.

Click the **Include headers and footers navigation links** option to include each page’s header and footer content, such as links in them.

### Specify Site Map URL

Specifying the site map URL crawls only URLs listed in the site map.

To crawl other URLs, use the [**Seed URL**](#specify-seed-url) option, or add another web crawling data source.

To specify a site map URL, click **Sitemap URL**, and then in the **Sitemap URL** field, enter the URL you want to crawl. For example, `docs.digitalocean.com/sitemap.xml`.

The site map URL must be in `.xml` format where you can identify a specific list of URLs to crawl. You can use a site map URL to add scoped URLs all at once instead of adding them individually, or choosing a crawling rule for a seed URL.

Click the **Index embedded media** option to index supported images and other media encountered during the crawl.

Click the **Include headers and footers navigation links** option to include each page’s header and footer content, such as links in them.

### Dropbox Folder

If you haven’t connected your Dropbox account, on the right of the **Pull from a Dropbox folder** option, click **Connect account** to first log in to your Dropbox account and authorize the connection.

To add a [Dropbox](https://www.dropbox.com) folder, click **Pull from a Dropbox folder**, and then choose at least one folder you want to index, or on the left of a folder, click **+** to expand its contents and select specific folders.

### Amazon S3 Bucket or Folder

To add an Amazon S3 bucket or folder, click **Pull from an AWS S3 bucket folder**.

In the [**Access Key ID**](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) field, enter the IAM access key ID for your S3 bucket or folder.

In the **Secret Key** field, enter the secret key associated with your access key ID.

In the **Bucket Name** field, enter the name of the S3 bucket to index.

In the **Region** field, enter the AWS region where your S3 bucket folder is located, such as `us-east-1` or `eu-west-1`.

On the right of the **Region** field, click **+** to add the S3 bucket.

If you want to control how the data source is split into chunks during indexing, click **Advanced Options** to [configure its chunking strategy](https://docs.digitalocean.com/products/knowledge-bases/how-to/create/index.html.md#config-chunk). By default, all data sources use section-based chunking. For more information about chunking strategies, see our [chunking strategy best practices](https://docs.digitalocean.com/products/knowledge-bases/concepts/data-services-chunking-strategies/index.html.md).

Then, click **Add selected data source**.

After adding your data source, [add another data source if you want](#add-control), and then in the top-right, review the data sources you’ve added with their data source type, estimated size, and configuration (such as, chunking configuration).

**Note**: Size estimates are available only for sources with known values, such as Spaces buckets and uploaded files. For other sources, the size appears after the initial indexing job completes.

If one of your data sources fails to be added, click the data source method you chose for that data source, and then on the right of the failed file, bucket, folder or URL, click the trash icon, and then [try again](#add-data-control). If it fails again, [contact support](https://cloudsupport.digitalocean.com).

After adding all your data sources and reviewing them, click **Next step: Configure database**, or [configure chunking strategies for your data sources](#config-chunk)

### Configure Chunking Strategy

Chunking controls how each data source is split before embedding and indexing the source into your knowledge base. Data sources use section-based chunking by default, and you can use different strategies in the same knowledge base by adding content as separate data sources.

Chunking strategies depend on the [selected embeddings model](https://docs.digitalocean.com/products/inference/details/models/index.html.md#embeddings-model). Chunk sizes must stay within the model’s token window and be at least approximately 100 tokens. For insights on which strategy to choose and configuration setup, see our [chunking best practices](https://docs.digitalocean.com/products/knowledge-bases/concepts/data-services-chunking-strategies/index.html.md) and the [chunking parameters reference](https://docs.digitalocean.com/products/knowledge-bases/reference/data-services-chunking-strategies/index.html.md).

To configure chunking after selecting your data source, at the bottom of the data source’s selection window, click **Advanced Options** to open the **Chunking strategy** section.

Under the **Select a chunking strategy for this data source** sub-section, click the strategy you want to use, and then configure its parameters.

You can choose one of the following strategies:

| Chunking strategy | How it works | Best For | Configuration |
|---|---|---|---|
| **Section-based chunking (default)** | Splits content using structural elements such as headings, paragraphs, tables, and lists. | Structured documents where preserving document layout matters. This strategy is fast and low cost. | Use the **Maximum chunk size** slider to set the maximum number of tokens per chunk. The value must stay within the embeddings model’s limits. |
| **Semantic chunking** | Groups text by meaning using embeddings. | Content where related ideas should stay together even when structure is limited. This strategy is slower and higher cost because it uses embeddings for both chunk detection and final embedding. | Use the **Similarity threshold** field to set how similar sentences must be to group together. Lower values create larger sentence groups. Use the **Maximum chunk size** slider to set the maximum number of tokens per chunk. |
| **Hierarchical chunking** | Creates parent chunks for broader context and child chunks for retrieval. Retrieval returns the child chunk first, then includes the parent chunk for additional context. | Documents where smaller passages need surrounding context. | Use the **Maximum parent chunk size** slider to set the maximum number of tokens in each parent chunk. Use the **Maximum child chunk size** slider to set the maximum number of tokens in each child chunk. Child chunks must be smaller than parent chunks. |
| **Fixed-length chunking** | Splits text by token count and ignores formatting or structure. | Unstructured data such as logs, telemetry, or Optical Character Recognition (OCR). | Use the **Maximum chunk size** slider to set the maximum number of tokens per chunk. The value must stay within the embeddings model’s limits. |

If you decide to [change chunking strategies after creating your knowledge base](https://docs.digitalocean.com/products/knowledge-bases/how-to/test-knowledge-bases/index.html.md#test-chunk), this requires re-indexing, which consumes additional tokens.

After setting up your chunking configuration your data source, click **Add selected data source**, and [repeat for another data source](#chunk), if necessary. Then, click **Next step: Configure database**.

### Choose Knowledge Base Name

In the **Configure database** step, either keep the autogenerated name or choose a unique name using 3 to 63 characters, including only letters, numbers, dashes, and periods.

### Choose Your OpenSearch Database

Knowledge bases require an [OpenSearch database](https://docs.digitalocean.com/products/databases/opensearch/index.html.md) to store vector embeddings. On the top-right of the page, use the estimated sizes in your added data sources list to choose a database size. We recommend allocating at least twice the total estimated data size. Database size is based on [OpenSearch pricing](https://docs.digitalocean.com/products/databases/opensearch/details/pricing/index.html.md).

If you want to remove a data source, click **Edit data sources**, which takes you back to the **Add data** step, and then under the **Add data sources** section, select the data source method with the data you want to remove, and then click the trash icon next to the data.

In the **Where should your knowledge base live?** section, under the **OpenSearch database options** sub-section, select either **Use existing** to connect to an existing OpenSearch database or **Create new** to provision a new one.

### Use Existing OpenSearch Database

If you choose **Use existing**, click the **Select an OpenSearch database** dropdown list, and then select the database you want to use. If it already contains data, it may limit how much new data you can index. You only pay for successfully indexed data.

### Create a New OpenSearch Database

Creating a new database automatically sets the smallest size that fits your data. We recommend allocating about twice the size of your total estimated data source size to efficiently store embeddings.

If you choose **Create new**, under the **Choose a datacenter region** section, either keep the default datacenter region, or click the **Additional datacenter regions** dropdown list to choose a different one.

If you want to attach the knowledge base to [agents](https://docs.digitalocean.com/products/inference/index.html.md), choose the same region as your agents to reduce latency. Most Agent Platform infrastructure is in TOR1, so we recommend the default region.

Under the **VPC Network** section, choose the VPC where your OpenSearch database is created.

Your VPC network determines which resources (such as agents or other applications) can access it. We recommend selecting the same VPC as those resources, so they can connect securely over a private network.

Afterwards, click **Next step: Review and create**.

### Finalize Details

In the **Review** step, under the **Final Details** section, click the **Select a project** dropdown list to choose the project you want your knowledge base stored in.

In the **Tags** field, add tags to help organize and filter your knowledge base. Tags can include letters, numbers, colons, dashes, and underscores. Choose a tag name, then press `ENTER` or `SPACEBAR` to add it. Use the arrow keys to navigate and the `BACKSPACE` key to remove tags.

Under the **Review** section, use the configuration sub-sections to confirm your embeddings model and token cost, selected data sources and estimated total size, and OpenSearch database specs and price. Existing databases don’t add new database charges.

To change a configuration, click **Edit** next to the sub-section you want to update, and then make your changes in its respective step.

After finalizing and reviewing your knowledge base setup, click **Create knowledge base** (or **Create Knowledge Base and database**).

### Provisioning Your Knowledge Base

After creating your knowledge base, it appears in the [**Knowledge bases** page](https://cloud.digitalocean.com/knowledge-bases) and immediately begins provisioning. Provisioning typically takes five minutes or longer as the process embeds and indexes your data sources.

After provisioning completes, click your knowledge base to view its **Overview** section. Under the **LATEST INDEXING DETAILS** sub-section view a summary of the indexing results, including final costs. You can download a CSV file of this index job in the knowledge base’s [**Activity** tab](https://docs.digitalocean.com/products/knowledge-bases/how-to/view-indexing-jobs/index.html.md).

If indexing takes longer than expected, let the indexing job continue running until it either completes or fails. If it fails, [check the **Activity** tab for detailed logs to understand what went wrong](https://docs.digitalocean.com/products/knowledge-bases/how-to/view-indexing-jobs/index.html.md) (for example, failed or skipped files).

After reviewing the indexing job logs and fixing any issues, on the right of the log, click **Re-run** to restart indexing. If problems persist, [contact support](https://cloudsupport.digitalocean.com).

If you added a seed or site map URL as a data source, verify web crawling is indexed successfully by re-adding the [same seed](#seed-url) or [sitemap URL](#site-map-url) as a new data source. If the [indexing job results](https://docs.digitalocean.com/products/knowledge-bases/how-to/view-indexing-jobs/index.html.md) of the duplicated data source shows zero tokens, the original crawl indexed all content, and you can [delete the duplicate](https://docs.digitalocean.com/products/knowledge-bases/how-to/manage-data-sources/index.html.md#delete-data-control).

To keep your data sources up to date automatically without manual re-ingest, we recommend also [setting up scheduled indexing](https://docs.digitalocean.com/products/knowledge-bases/how-to/index-data-sources/index.html.md#schedule-control).

## Create a Knowledge Base via the API

To create a knowledge base via the DigitalOcean API, provide a name, an [embeddings model](https://docs.digitalocean.com/products/knowledge-bases/details/knowledge-base-models/index.html.md#embeddings-models), a project ID, and a datacenter region.

You can also specify the ID of an existing OpenSearch database or a chunking strategy. If you don’t provide a database, we create one and size one for you automatically.

You can configure your chunking strategy for a data source when creating your knowledge base with the following optional fields:

- **`chunking_algorithm`** : The chunking strategy (`section`, `semantic`, `hierarchical`, or `fixed`).
- **`chunking_options`** : A configuration object containing parameters such as `max_chunk_size`, `semantic_threshold`, `parent_chunk_size`, or `child_chunk_size`.

Chunking is applied per data source. Updating chunking settings triggers re-indexing, which consumes tokens. For details and recommendations, see our [chunking best practices](https://docs.digitalocean.com/products/knowledge-bases/concepts/data-services-chunking-strategies/index.html.md) and [chunking parameters reference](https://docs.digitalocean.com/products/knowledge-bases/reference/data-services-chunking-strategies/index.html.md).

If you don’t configure a chunking strategy for a data source, the knowledge base uses section-based chunking (`section`) by default.

To list available embeddings models and their IDs, call the [`/v2/gen-ai/models` endpoint](https://docs.digitalocean.com/reference/api/reference/gradientai-platform/index.html.md#genai_list_models) with the `usecases` query parameter.

## How to Create a Knowledge Base Using the DigitalOcean API

[Create a personal access token](https://docs.digitalocean.com/reference/api/create-personal-access-token/index.html.md) and save it for use with the API.

### cURL

Send a POST request to [`https://api.digitalocean.com/v2/gen-ai/knowledge_bases`](https://docs.digitalocean.com/reference/api/reference/gradientai-platform/index.html.md#genai_create_knowledge_base).

Using cURL:

```shell
curl -X POST \
  -H "Content-Type: application/json"  \
  -H "Authorization: Bearer $DIGITALOCEAN_TOKEN" \
  "https://api.digitalocean.com/v2/gen-ai/knowledge_bases" \
  -d '{
    "name": "kb-api-create",
    "embedding_model_uuid": "05700391-7aa8-11ef-bf8f-4e013e2ddde4",
    "project_id": "37455431-84bd-4fa2-94cf-e8486f8f8c5e",
    "tags": [
      "tag1"
    ],
    "database_id": "abf1055a-745d-4c24-a1db-1959ea819264",
    "datasources": [
      {
          "spaces_data_source": {
              "bucket_name": "test-public-gen-ai",
              "region": "tor1"
            },
            "chunking_algorithm": "CHUNKING_ALGORITHM_HIERARCHICAL",
            "chunking_options": {
              "parent_chunk_size": 1000,
              "child_chunk_size": 350
            }
      },
      {
        "web_crawler_data_source": {
          "base_url": "https://example.com",
          "crawling_option": "SCOPED",
          "embed_media": false,
          "exclude_tags": ["nav","footer","header","aside","script","style","form","iframe", "noscript"]
        },
        "chunking_algorithm": "CHUNKING_ALGORITHM_SEMANTIC",
        "chunking_options": {
          "max_chunk_size": 500,
          "semantic_threshold": 0.6
        }
      },
      {
        "spaces_data_source": {
            "bucket_name": "test-public-gen-ai-2",
            "region": "tor1"
          },
          "chunking_algorithm": "CHUNKING_ALGORITHM_FIXED_LENGTH",
          "chunking_options": {
            "max_chunk_size": 400
          }
      },
    ],
    "region": "tor1",
    "vpc_uuid": "f7176e0b-8c5e-4e32-948e-79327e56225a",
    "reranking_config": {
      "enabled": true,
      "model": "bge-reranker-v2-m3"
    }
  }'
```

After creating your knowledge base, indexing begins automatically. You can [list all knowledge bases](https://docs.digitalocean.com/reference/api/reference/gradientai-platform/index.html.md#genai_list_knowledge_bases), [view a knowledge base](https://docs.digitalocean.com/reference/api/reference/gradientai-platform/index.html.md#genai_get_knowledge_base), or [update one](https://docs.digitalocean.com/reference/api/reference/gradientai-platform/index.html.md#genai_update_knowledge_base).

To add another data source, use the [Data Sources endpoint](https://docs.digitalocean.com/reference/api/reference/gradientai-platform/index.html.md#genai_create_knowledge_base_data_source).

To retrieve metadata for embeddings models, use the [List Models endpoint](https://docs.digitalocean.com/reference/api/reference/gradientai-platform/index.html.md#genai_list_models).