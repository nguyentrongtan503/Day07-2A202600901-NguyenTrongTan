# Báo Cáo Lab 7: Embedding & Vector Store

**Họ tên:** Nguyễn Trọng Tấn  
**Nhóm:** DigitalOcean Knowledge Bases Docs  
**Ngày:** 05/06/2026

---

## 1. Warm-up

### Cosine Similarity

**High cosine similarity nghĩa là gì?**  
Hai text chunks có high cosine similarity khi vector embedding của chúng nằm gần cùng hướng trong không gian vector. Điều này thường có nghĩa là hai đoạn nói về nội dung hoặc ý định tương tự nhau, dù có thể dùng từ khác nhau.

**Ví dụ HIGH similarity:**
- Sentence A: "Vector databases store embeddings for similarity search."
- Sentence B: "A vector store keeps embedding vectors so users can find similar documents."
- Tại sao tương đồng: cả hai đều nói về vector store, embeddings và similarity search.

**Ví dụ LOW similarity:**
- Sentence A: "Metadata filters narrow retrieval results to relevant documents."
- Sentence B: "A chocolate cake needs flour, sugar, and butter."
- Tại sao khác: hai câu thuộc hai domain khác nhau, một câu về retrieval, một câu về nấu ăn.

**Tại sao cosine similarity được ưu tiên hơn Euclidean distance cho text embeddings?**  
Cosine similarity tập trung vào hướng của vector, nên phù hợp với việc đo mức độ giống nhau về nghĩa. Euclidean distance bị ảnh hưởng nhiều bởi độ lớn vector, trong khi text embedding thường quan trọng hướng ngữ nghĩa hơn khoảng cách hình học tuyệt đối.

### Chunking Math

**Document 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**

Formula:

```text
num_chunks = ceil((doc_length - overlap) / (chunk_size - overlap))
           = ceil((10000 - 50) / (500 - 50))
           = ceil(9950 / 450)
           = ceil(22.11)
           = 23 chunks
```

**Nếu overlap tăng lên 100 thì sao?**

```text
num_chunks = ceil((10000 - 100) / (500 - 100))
           = ceil(9900 / 400)
           = ceil(24.75)
           = 25 chunks
```

Overlap lớn hơn làm tăng số chunk, nhưng giúp giữ lại context giữa hai chunk liền tiếp. Điều này hữu ích khi câu trả lời nằm sát ranh giới giữa hai chunk.

---

## 2. Document Selection - Nhóm

### Domain & Lý Do Chọn

**Domain:** DigitalOcean Knowledge Bases / RAG documentation.

Nhóm chọn DigitalOcean Knowledge Bases docs vì tài liệu liên quan trực tiếp đến embedding, chunking, retrieval, metadata filtering và reranking. Đây là bộ docs công khai, có URL rõ ràng, cấu trúc Markdown nhiều heading, rất phù hợp để so sánh các chunking strategy.

### Data Inventory

| # | Tên tài liệu | Nguồn | Số ký tự | Metadata đã gán |
|---|---|---|---:|---|
| 1 | `do_retrieval_best_practices.md` | DigitalOcean Docs | 6779 | `category=retrieval`, `doc_type=concept`, `audience=developer` |
| 2 | `do_chunking_best_practices.md` | DigitalOcean Docs | 8507 | `category=chunking`, `doc_type=concept`, `audience=developer` |
| 3 | `do_system_instructions_best_practices.md` | DigitalOcean Docs | 2323 | `category=prompting`, `doc_type=concept`, `audience=developer` |
| 4 | `do_create_knowledge_bases.md` | DigitalOcean Docs | 26682 | `category=setup`, `doc_type=how_to`, `audience=operator` |
| 5 | `do_test_knowledge_bases.md` | DigitalOcean Docs | 16414 | `category=evaluation`, `doc_type=how_to`, `audience=operator` |

### Metadata Schema

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho retrieval? |
|---|---|---|---|
| `doc_id` | string | `do_retrieval_best_practices` | Xác định tài liệu gốc và dùng để delete/filter. |
| `source` | string | `DigitalOcean Docs` | Ghi nguồn trong report và demo. |
| `url` | string | URL gốc | Trace lại evidence và gold answer. |
| `category` | string | `retrieval`, `chunking` | Lọc theo chủ đề khi query rõ domain. |
| `doc_type` | string | `concept`, `how_to` | Phân biệt tài liệu giải thích và hướng dẫn thao tác. |
| `language` | string | `en` | Ghi ngôn ngữ tài liệu. |
| `audience` | string | `developer`, `operator` | Lọc theo nhóm người dùng hoặc mục đích sử dụng. |

---

## 3. Chunking Strategy

### Baseline Analysis

Chạy `ChunkingStrategyComparator().compare()` trên 2 tài liệu với `chunk_size=700`.

| Tài liệu | Strategy | Chunk Count | Avg Length | Preserves Context? |
|---|---|---:|---:|---|
| `do_retrieval_best_practices.md` | FixedSizeChunker | 11 | 679.9 | Trung bình, có thể cắt ngang section |
| `do_retrieval_best_practices.md` | SentenceChunker | 10 | 675.8 | Tốt hơn về câu, nhưng không bám heading |
| `do_retrieval_best_practices.md` | RecursiveChunker | 13 | 511.5 | Tốt, giữ paragraph/section nhỏ hơn |
| `do_chunking_best_practices.md` | FixedSizeChunker | 14 | 672.6 | Trung bình |
| `do_chunking_best_practices.md` | SentenceChunker | 20 | 423.1 | Dễ đọc, nhiều chunk hơn |
| `do_chunking_best_practices.md` | RecursiveChunker | 17 | 498.6 | Cân bằng size và context |

### Strategy Của Tôi

**Loại:** Custom Markdown Heading Chunker.

Strategy của tôi chia tài liệu Markdown theo heading `#`, `##`, `###`. Mỗi chunk giữ heading và nội dung bên dưới heading để khi retrieve có thể trace về section gốc. Nếu một section quá dài, chunker fallback sang `RecursiveChunker` để chia nhỏ body nhưng vẫn gắn lại heading lên từng chunk con.

**Tại sao tôi chọn strategy này cho domain nhóm?**  
DigitalOcean docs có cấu trúc heading rõ ràng theo concept/how-to/reference. Vì vậy chia theo heading phù hợp hơn fixed-size, vì ranh giới heading thường là ranh giới ý nghĩa thật của tài liệu. Cách này cũng dễ giải thích khi demo: query hỏi concept nào thì kỳ vọng retrieve đúng section đó.

**Code snippet:**

```python
class MarkdownHeadingChunker:
    HEADING_PATTERN = re.compile(r"(?m)^(#{1,3})\s+.+$")

    def __init__(self, max_chunk_size: int = 900, fallback_chunk_size: int = 700) -> None:
        self.max_chunk_size = max_chunk_size
        self.fallback_chunker = RecursiveChunker(chunk_size=fallback_chunk_size)

    def chunk(self, text: str) -> list[str]:
        matches = list(self.HEADING_PATTERN.finditer(text))
        if not matches:
            return self.fallback_chunker.chunk(text)
        # Split by heading, keep heading in each chunk.
```

### So Sánh: Strategy của tôi vs Baseline

| Tài liệu | Strategy | Chunk Count | Avg Length | Retrieval Quality? |
|---|---|---:|---:|---|
| `do_retrieval_best_practices.md` | best baseline: RecursiveChunker | 13 | 511.5 | Tốt, nhưng heading trace không rõ bằng custom |
| `do_retrieval_best_practices.md` | **MarkdownHeadingChunker** | 11 | ~616 | Tốt, top-3 relevant với retrieval queries |
| `do_chunking_best_practices.md` | best baseline: RecursiveChunker | 17 | 498.6 | Tốt, chia paragraph ổn định |
| `do_chunking_best_practices.md` | **MarkdownHeadingChunker** | 16 | ~532 | Tốt, giữ heading như `Improve Chunking Performance` |

### So Sánh Với Thành Viên Khác

| Thành viên | Strategy | Retrieval Score (/10) | Điểm mạnh | Điểm yếu |
|---|---|---:|---|---|
| Tôi - Tấn | Markdown heading custom | 9 | Trace đúng section, có rationale rõ | Cần fallback nếu section dài |
| Chức | Fixed-size baseline | TBD | Đơn giản, ổn định | Dễ cắt ngang ý/heading |
| Quang | Sentence-based | TBD | Chunk dễ đọc | Size không đều, không bám heading |
| Lam | Recursive | TBD | Cân bằng context và size | Cần tune separator |

**Strategy nào tốt nhất cho domain này?**  
Với DigitalOcean docs, Markdown heading custom rất phù hợp vì docs có section rõ ràng và query thường hỏi theo concept. Recursive chunking có thể là baseline mạnh, nhưng heading custom dễ trace nguồn hơn và dễ trình bày trong demo hơn.

---

## 4. My Approach - Cá Nhân

### Chunking Functions

**`SentenceChunker.chunk`**  
Dùng regex `(?<=[.!?])(?:\s+|\n+)` để tách câu sau dấu `.`, `!`, `?`. Sau đó gom mỗi `max_sentences_per_chunk` câu thành một chunk và strip whitespace. Edge case: text rỗng trả về `[]`.

**`RecursiveChunker.chunk` / `_split`**  
Thuật toán thử các separator theo thứ tự ưu tiên `\n\n`, `\n`, `. `, space, sau đó mới fallback fixed-size. Base case là khi text đã nhỏ hơn `chunk_size`. Nếu một piece vẫn quá dài, hàm tiếp tục recurse với separator tiếp theo.

### EmbeddingStore

**`add_documents` + `search`**  
Mỗi `Document` được normalize thành record gồm `id`, `doc_id`, `content`, `metadata`, `embedding`. Search embed query, tính cosine similarity với từng record, sort score giảm dần và trả về top-k.

**`search_with_filter` + `delete_document`**  
`search_with_filter` filter metadata trước, rồi mới search trên tập ứng viên đã lọc. `delete_document` xóa tất cả chunk có `metadata['doc_id']` hoặc `doc_id` trùng với document cần xóa.

### KnowledgeBaseAgent

**`answer`**  
Agent retrieve top-k chunk từ store, ghép thành context có nhãn `[Source 1]`, `[Source 2]`, sau đó tạo prompt yêu cầu LLM chỉ trả lời dựa trên context. Cách này theo pattern RAG: retrieve trước, generate sau.

### Test Results

```text
pytest tests/ -v
42 passed
```

**Số tests pass:** 42 / 42

---

## 5. Similarity Predictions

Dùng `_mock_embed` để embed câu, sau đó gọi `compute_similarity()`.

| Pair | Sentence A | Sentence B | Dự đoán | Actual Score | Đúng? |
|---|---|---|---|---:|---|
| 1 | Python programming tutorial | Python coding guide for developers | high | 0.052 | Không |
| 2 | Knowledge base retrieval uses chunks | Vector search retrieves relevant document chunks | high | -0.142 | Không |
| 3 | Hybrid search combines semantic and keyword search | Reranking improves the order of retrieved chunks | medium | 0.081 | Gần đúng |
| 4 | Create a database cluster | Bake a chocolate cake | low | -0.067 | Đúng |
| 5 | Metadata filters narrow retrieval results | Marketing campaign budget planning | low | 0.037 | Đúng |

**Kết quả bất ngờ nhất:**  
Hai câu retrieval/chunking ở pair 2 về nghĩa khá gần nhau nhưng score lại âm. Điều này cho thấy `_mock_embed` chỉ phù hợp cho test deterministic của lab, không phải embedding semantic thật. Khi benchmark nghiêm túc nên dùng local embedder hoặc OpenAI embedder.

---

## 6. Results - Cá Nhân

### Benchmark Queries & Gold Answers

| # | Query | Gold Answer |
|---|---|---|
| 1 | What are DigitalOcean's recommended best practices for a strong retrieval setup? | Nên cân bằng semantic/keyword search, dùng filters, test chunking khi kết quả bị fragmented/noisy, và enable reranking khi cần sắp xếp lại chunk liên quan. |
| 2 | Why can chunks that are too small or too large hurt retrieval quality? | Chunk quá nhỏ làm mất context; chunk quá lớn có thể chứa nội dung không liên quan và làm giảm độ chính xác retrieval. |
| 3 | When should filters be used in knowledge base retrieval? | Dùng filters khi cần giới hạn retrieval theo document, file, metadata hoặc URL path để tránh lấy nhầm nguồn. |
| 4 | What is the difference between chunking, retrieval, and reranking in a RAG system? | Chunking chia data để index; retrieval chọn candidate chunks; reranking sắp xếp lại candidate chunks trước khi đưa vào LLM. |
| 5 | How should a team test whether a knowledge base returns useful answers? | Test bằng query thực tế, xem top-k chunks, so sánh filtered/unfiltered search, và đối chiếu answer với source evidence. |

### Kết Quả Của Tôi

Benchmark chạy bằng `benchmark_digitalocean_heading.py`, strategy `MarkdownHeadingChunker`, filter theo `category` khi query có chủ đề rõ.

| # | Query | Top-1 Retrieved Chunk | Score | Relevant? | Agent Answer tóm tắt |
|---|---|---|---:|---|---|
| 1 | Strong retrieval setup best practices | `Retrieval Example` / retrieval docs | 0.707 | Yes | Cần dùng hybrid retrieval, filters, chunking test và reranking. |
| 2 | Chunks too small/large | `Improve Chunking Performance` / chunking docs | 0.378 | Yes | Chunk size ảnh hưởng context và noise; cần test/tune chunking. |
| 3 | When use filters | `DigitalOcean Knowledge Base Retrieval Best Practices` | 0.781 | Yes | Filters giới hạn kết quả theo file, document, metadata, URL path. |
| 4 | Chunking vs retrieval vs reranking | `DigitalOcean Knowledge Base Retrieval Best Practices` | 0.880 | Yes | Chunking tạo indexed data, retrieval lấy candidates, reranking sắp xếp lại. |
| 5 | Test useful answers | `Test Reranking` / evaluation docs | 0.862 | Yes | Kiểm tra retrieval/reranking bằng query và source evidence. |

**Bao nhiêu queries trả về chunk relevant trong top-3?** 5 / 5

---

## 7. What I Learned

**Điều hay nhất tôi học được từ thành viên khác trong nhóm:**  
Fixed-size baseline rất cần thiết vì nó tạo mốc so sánh đơn giản. Sentence-based và recursive chunking giúp thấy rõ trade-off giữa readability, chunk count và context preservation.

**Điều hay nhất tôi học được từ nhóm khác qua demo:**  
Cần đánh giá retrieval bằng evidence, không chỉ nhìn score. Top-1 cao nhưng sai source vẫn có thể làm agent trả lời sai.

**Nếu làm lại, tôi sẽ thay đổi gì trong data strategy?**  
Tôi sẽ lấy thêm 2 file reference/how-to để benchmark có nhiều case hơn, đặc biệt query về parameter và data source management. Tôi cũng sẽ dùng local semantic embedder thay vì mock/keyword embedder để kết quả gần thực tế hơn.

### Failure Analysis

**Failure case:** Query 4 có top-2 là `Configure Reranking` trong category `setup`, không nằm trong expected category `retrieval/chunking`.  
**Nguyên nhân:** Query có từ "reranking" nên lexical embedding ưu tiên chunk nào lặp lại từ này, dù context chính của câu hỏi là phân biệt chunking, retrieval và reranking.  
**Cải thiện:** Dùng semantic embedding thật, thêm metadata filter `category=retrieval` hoặc tăng trọng số cho heading/context thay vì chỉ đếm keyword.

---

## Tự Đánh Giá

| Tiêu chí | Loại | Điểm tự đánh giá |
|---|---|---:|
| Warm-up | Cá nhân | 5 / 5 |
| Document selection | Nhóm | 9 / 10 |
| Chunking strategy | Nhóm | 14 / 15 |
| My approach | Cá nhân | 10 / 10 |
| Similarity predictions | Cá nhân | 4 / 5 |
| Results | Cá nhân | 9 / 10 |
| Core implementation (tests) | Cá nhân | 30 / 30 |
| Demo | Nhóm | 4 / 5 |
| **Tổng** | | **95 / 100** |
