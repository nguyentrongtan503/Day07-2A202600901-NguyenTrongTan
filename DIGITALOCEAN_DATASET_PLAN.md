# Kế Hoạch Dataset Nhóm: DigitalOcean Knowledge Bases Docs

## 1. Chốt Bộ Dữ Liệu

Nhóm chọn domain:

**DigitalOcean Knowledge Bases / Tài liệu về RAG và Retrieval**

Đây là bộ tài liệu phù hợp nhất cho lab này vì:

- Nội dung liên quan trực tiếp đến embedding, vector store, chunking, retrieval, metadata filtering và RAG.
- Tài liệu công khai, có nguồn rõ ràng, dễ ghi vào report.
- Cấu trúc documentation rõ: có heading, section, concept, how-to, reference.
- Nhiều trang có thể xem hoặc copy dưới dạng Markdown, thuận tiện lưu vào `data/`.
- Dễ thiết kế 5 benchmark queries có gold answers kiểm chứng được.
- Rất phù hợp để 4 thành viên thử 4 strategy khác nhau rồi so sánh.

Nguồn chính:

- DigitalOcean Knowledge Bases docs: https://docs.digitalocean.com/products/knowledge-bases/
- Retrieval Best Practices: https://docs.digitalocean.com/products/knowledge-bases/concepts/data-services-retrieval/

## 2. Các Tài Liệu Cần Lấy

Nhóm nên lấy từ 5 đến 7 trang tài liệu và lưu vào thư mục `data/` dưới dạng `.md` hoặc `.txt`.

Nếu thời gian ít, lấy 5 file đầu tiên là đủ. Nếu muốn bài đầy đủ và dễ demo hơn, lấy cả 7 file.

Lưu ý: các tên file dưới đây là **tên file nhóm tự đặt sau khi copy/tải nội dung về**, không phải file có sẵn trong repo.

| # | Tên file cần lưu trong `data/` | Link bình thường để mở | Category | Vì sao nên lấy |
|---|---|---|---|---|
| 1 | `do_retrieval_best_practices.md` | https://docs.digitalocean.com/products/knowledge-bases/concepts/data-services-retrieval/ | `retrieval` | Tài liệu trung tâm, nói về chất lượng retrieval, filter, hybrid search, reranking. |
| 2 | `do_chunking_best_practices.md` | https://docs.digitalocean.com/products/knowledge-bases/concepts/data-services-chunking-strategies/ | `chunking` | Rất phù hợp để so sánh các chiến lược chunking. |
| 3 | `do_system_instructions_best_practices.md` | https://docs.digitalocean.com/products/knowledge-bases/concepts/data-services-system-instructions/ | `prompting` | Dùng để phân tích cách agent trả lời dựa trên context. |
| 4 | `do_create_knowledge_bases.md` | https://docs.digitalocean.com/products/knowledge-bases/how-to/create/ | `setup` | Nói về cách tạo knowledge base và nạp dữ liệu. |
| 5 | `do_test_knowledge_bases.md` | https://docs.digitalocean.com/products/knowledge-bases/how-to/test-knowledge-bases/ | `evaluation` | Dùng cho query về cách đánh giá knowledge base/retrieval, chunking và reranking. |
| 6 | `do_manage_data_sources.md` | https://docs.digitalocean.com/products/knowledge-bases/how-to/manage-data-sources/ | `data_sources` | Dùng cho query về quản lý nguồn dữ liệu, cập nhật và bảo trì tài liệu. |
| 7 | `do_chunking_parameters.md` | https://docs.digitalocean.com/products/knowledge-bases/reference/data-services-chunking-strategies/ | `chunking` | Dùng để hỏi về chunk size, overlap và cách tune tham số. |

## 3. Cách Lấy Tài Liệu

Trên các trang DigitalOcean docs thường có lựa chọn:

- **Copy page as Markdown**
- **View page as Markdown**

Cách làm đề xuất:

1. Mở từng trang tài liệu trên trình duyệt.
2. Bấm `View page as Markdown` hoặc `Copy page as Markdown`.
3. Lưu nội dung vào file tương ứng trong thư mục `data/`.
4. Kiểm tra lại file sau khi lưu, tránh để quá nhiều menu, navigation hoặc nội dung thừa.
5. Nếu một trang quá dài, giữ lại các section chính liên quan đến retrieval, chunking, testing, filtering hoặc knowledge base setup.

Cách đơn giản nhất:

1. Mở link bình thường trong bảng trên.
2. Ở đầu trang DigitalOcean, tìm nút `Copy page as Markdown` hoặc `View page as Markdown`.
3. Nếu có `Copy page as Markdown`, bấm vào đó rồi paste vào file trong `data/`.
4. Nếu không thấy nút đó, copy phần nội dung chính của trang, không cần copy menu/sidebar.
5. Lưu thành đúng tên file đề xuất.

Tên file nên đặt như sau:

```text
data/do_retrieval_best_practices.md
data/do_chunking_best_practices.md
data/do_system_instructions_best_practices.md
data/do_create_knowledge_bases.md
data/do_test_knowledge_bases.md
data/do_manage_data_sources.md
data/do_chunking_parameters.md
```

## 4. Metadata Schema

Mỗi document hoặc mỗi chunk nên có metadata. Metadata giúp nhóm test `search_with_filter()` và giải thích rõ vì sao filter có thể cải thiện retrieval.

Schema đề xuất:

| Field | Kiểu | Ví dụ | Tác dụng |
|---|---|---|---|
| `doc_id` | string | `do_retrieval_best_practices` | Định danh tài liệu, dùng cho filter hoặc delete. |
| `source` | string | `DigitalOcean Docs` | Ghi nguồn rõ ràng trong report. |
| `url` | string | URL gốc | Dùng để trace lại gold answer và nguồn tài liệu. |
| `category` | string | `retrieval`, `chunking`, `evaluation` | Lọc theo chủ đề. |
| `doc_type` | string | `concept`, `how_to`, `reference` | Lọc theo loại tài liệu. |
| `language` | string | `en` | Ghi ngôn ngữ tài liệu. |
| `audience` | string | `developer`, `operator` | Lọc theo nhóm người đọc hoặc mục đích sử dụng. |

Metadata đề xuất cho từng file:

| File | `category` | `doc_type` | `audience` |
|---|---|---|---|
| `do_retrieval_best_practices.md` | `retrieval` | `concept` | `developer` |
| `do_chunking_best_practices.md` | `chunking` | `concept` | `developer` |
| `do_system_instructions_best_practices.md` | `prompting` | `concept` | `developer` |
| `do_create_knowledge_bases.md` | `setup` | `how_to` | `operator` |
| `do_test_knowledge_bases.md` | `evaluation` | `how_to` | `operator` |
| `do_manage_data_sources.md` | `data_sources` | `how_to` | `operator` |
| `do_chunking_parameters.md` | `chunking` | `reference` | `developer` |

## 5. Phân Công Strategy Cho 4 Thành Viên

Tất cả thành viên dùng cùng một dataset và cùng 5 benchmark queries. Điểm khác nhau là mỗi người dùng một strategy riêng để có cơ sở so sánh.

### Thành viên 1: Fixed-size Baseline - Chức

Strategy:

- Dùng `FixedSizeChunker`.
- Tham số đề xuất: `chunk_size=500`, `overlap=50`.

Mục tiêu:

- Tạo baseline đơn giản để các strategy khác so sánh.
- Đo chunk count, average chunk length và top-3 relevance.

Điểm cần quan sát:

- Chunk có bị cắt ngang câu hoặc ngang section không?
- Query về chunking/retrieval có retrieve đủ ý không?
- Chunk lớn chứa nhiều ý có làm kết quả retrieval bị nhiễu không?

Kết luận dự kiến:

- Strategy này dễ chạy và ổn định, nhưng có thể kém về chunk coherence vì không quan tâm đến ranh giới câu hoặc heading.

### Thành viên 2: Sentence-based Chunking - Quang

Strategy:

- Dùng `SentenceChunker`.
- Gom nhiều câu thành một chunk khoảng 400-700 ký tự.

Mục tiêu:

- Giữ chunk tự nhiên hơn vì không cắt giữa câu.
- Phù hợp với các trang dạng giải thích như retrieval best practices hoặc system instructions.

Điểm cần quan sát:

- Chunk có dễ đọc hơn fixed-size không?
- Có chunk nào quá dài vì sentence hoặc section dài không?
- Top-1 retrieved chunk có trả lời đúng gold answer hơn baseline không?

Kết luận dự kiến:

- Strategy này thường tốt hơn fixed-size về độ dễ đọc, nhưng độ dài chunk có thể không đều.

### Thành viên 3: Recursive Chunking - Lam

Strategy:

- Dùng `RecursiveChunker`.
- Ưu tiên tách theo heading/paragraph trước, sau đó mới tách theo dòng, câu, từ.
- Tham số đề xuất: `chunk_size=700`, `overlap=80`.

Mục tiêu:

- Giữ cấu trúc documentation tốt hơn fixed-size và sentence-only.
- Phù hợp với Markdown docs vì tài liệu có nhiều heading và paragraph.

Điểm cần quan sát:

- Strategy này có giữ đủ context trong cùng một section không?
- Overlap có giúp câu trả lời đầy đủ hơn không?
- Retrieval score trên 5 queries có cao hơn các strategy khác không?

Kết luận dự kiến:

- Đây có thể là strategy mạnh nhất nếu code xử lý separator tốt, vì nó cân bằng giữa kích thước chunk và ý nghĩa nội dung.

### Thành viên 4: Custom Markdown Heading Chunker - Tấn

Strategy:

- Tự viết custom chunker chia theo Markdown heading: `#`, `##`, `###`.
- Mỗi chunk nên giữ cả heading và nội dung bên dưới heading.
- Nếu một section quá dài, fallback sang recursive hoặc sentence chunking.

Mục tiêu:

- Tận dụng cấu trúc tài liệu DigitalOcean.
- Dễ giải thích trong demo vì strategy dựa trên đặc điểm thật của dataset.

Điểm cần quan sát:

- Query hỏi về một concept cụ thể có retrieve đúng section không?
- Heading có giúp chunk dễ trace nguồn hơn không?
- Các trang how-to/reference có cần chia nhỏ thêm theo subsection không?

Kết luận dự kiến:

- Đây là strategy có rationale rõ nhất. Nếu xử lý tốt section dài, nó có thể đạt kết quả rất tốt và dễ trình bày.

## 6. Benchmark Queries Và Gold Answers

Nhóm thống nhất dùng 5 queries dưới đây. Khi làm thật, cần kiểm chứng lại gold answers bằng chính tài liệu đã tải về.

| # | Query | Gold answer mong đợi | Metadata/filter nên thử |
|---|---|---|---|
| 1 | What are DigitalOcean's recommended best practices for a strong retrieval setup? | Một retrieval setup tốt nên kết hợp semantic search và keyword search khi cần, dùng filter để giới hạn phạm vi tìm kiếm, kiểm tra chunking khi kết quả thiếu hoặc nhiễu, và dùng reranking nếu cần sắp xếp lại các chunk liên quan. | `category=retrieval` |
| 2 | Why can chunks that are too small or too large hurt retrieval quality? | Chunk quá nhỏ có thể làm mất ngữ cảnh; chunk quá lớn có thể chứa nhiều ý không liên quan và làm giảm độ chính xác retrieval. | `category=chunking` |
| 3 | When should filters be used in knowledge base retrieval? | Filter nên dùng khi muốn giới hạn retrieval theo file, document, metadata hoặc URL path để tránh lấy nhầm nguồn không liên quan. | `category=retrieval` |
| 4 | What is the difference between chunking, retrieval, and reranking in a RAG system? | Chunking quyết định cách chia dữ liệu để index; retrieval chọn các chunk ứng viên; reranking sắp xếp lại các chunk ứng viên để đưa context tốt hơn vào LLM. | `category=retrieval` hoặc `category=chunking` |
| 5 | How should a team test whether a knowledge base returns useful answers? | Nên test bằng câu hỏi thực tế, kiểm tra top-k retrieved chunks, so sánh filtered với unfiltered search, và đối chiếu câu trả lời với source evidence. | `category=evaluation` |

Yêu cầu khi chạy benchmark:

- Mỗi thành viên chạy cùng 5 query.
- Ghi lại top-3 retrieved chunks cho từng query.
- Đánh dấu chunk nào relevant.
- Ghi score similarity.
- Ghi agent answer tóm tắt.
- So sánh agent answer với gold answer.

## 7. Bảng Cần Điền Trong Report

### Document Inventory

| # | Tên tài liệu | Nguồn | Số ký tự | Metadata đã gán |
|---|---|---|---|---|
| 1 | `do_retrieval_best_practices.md` | DigitalOcean Docs | TBD | `category=retrieval`, `doc_type=concept` |
| 2 | `do_chunking_best_practices.md` | DigitalOcean Docs | TBD | `category=chunking`, `doc_type=concept` |
| 3 | `do_system_instructions_best_practices.md` | DigitalOcean Docs | TBD | `category=prompting`, `doc_type=concept` |
| 4 | `do_create_knowledge_bases.md` | DigitalOcean Docs | TBD | `category=setup`, `doc_type=how_to` |
| 5 | `do_test_knowledge_bases.md` | DigitalOcean Docs | TBD | `category=evaluation`, `doc_type=how_to` |

### Strategy Comparison

| Thành viên | Strategy | Chunk size / overlap | Có dùng metadata filter? | Retrieval score `/10` | Điểm mạnh | Điểm yếu |
|---|---|---|---|---|---|---|
| TV1 | Fixed-size baseline | 500 / 50 | Optional | TBD | Đơn giản, ổn định | Dễ cắt ngang ý |
| TV2 | Sentence-based | 400-700 ký tự | Optional | TBD | Chunk dễ đọc | Size không đều |
| TV3 | Recursive | 700 / 80 | Optional | TBD | Cân bằng context và size | Cần tune separator |
| TV4 | Markdown heading custom | Theo section | Có | TBD | Trace đúng section | Cần fallback nếu section dài |

### Per-query Result

Mỗi thành viên điền bảng này trong report cá nhân:

| # | Query | Top-1 chunk tóm tắt | Top-3 có relevant không? | Score | Agent answer đúng gold không? |
|---|---|---|---|---|---|
| 1 | | | Yes/No | | Yes/No |
| 2 | | | Yes/No | | Yes/No |
| 3 | | | Yes/No | | Yes/No |
| 4 | | | Yes/No | | Yes/No |
| 5 | | | Yes/No | | Yes/No |

## 8. Failure Case Cần Tìm

Nhóm cần tìm ít nhất 1 failure case để viết phần phân tích lỗi. Một số lỗi có thể gặp:

- Query hỏi về `chunking` nhưng retrieve nhầm tài liệu `retrieval` vì hai chủ đề gần nghĩa.
- Fixed-size chunk cắt mất nửa sau của ý quan trọng.
- Filter `category=chunking` quá chặt, làm mất kết quả tốt nằm trong tài liệu `retrieval`.
- Heading custom chunk tạo chunk quá dài nếu một section có nhiều nội dung.
- Mock embedding có thể xếp hạng kết quả không đúng kỳ vọng với các query gần nghĩa.

Cách viết failure analysis:

1. Ghi query nào bị fail.
2. Ghi strategy nào fail.
3. Ghi top-3 retrieved chunks sai ở đâu.
4. Giải thích nguyên nhân: chunk quá nhỏ, chunk quá lớn, metadata thiếu, query mơ hồ, embedding yếu.
5. Đề xuất cải thiện: đổi chunk size, thêm overlap, thêm metadata, dùng recursive chunking hoặc heading chunker.

## 9. Timeline Làm Nhóm

### Buổi 1: Chuẩn bị data

- Lấy 5-7 trang DigitalOcean docs.
- Lưu vào thư mục `data/`.
- Gắn metadata schema.
- Thống nhất 5 benchmark queries và gold answers.

### Buổi 2: Code cá nhân

- Mỗi thành viên implement các TODO trong `src/`.
- Chạy `pytest tests/ -v`.
- Sửa đến khi tests pass.

### Buổi 3: Chạy benchmark

- Mỗi thành viên chạy strategy riêng.
- Ghi top-3 chunks, score, relevant/not relevant.
- So sánh filtered vs unfiltered cho ít nhất 1 query.

### Buổi 4: Tổng hợp và demo

- Gom bảng strategy comparison.
- Chọn strategy tốt nhất và giải thích vì sao.
- Chọn 1 failure case.
- Hoàn thành `report/REPORT.md`.

## 10. Kết Luận Có Thể Đưa Vào Report

Nhóm chọn DigitalOcean Knowledge Bases docs vì bộ tài liệu này có domain rõ ràng, nguồn công khai, cấu trúc documentation tốt và liên quan trực tiếp đến RAG retrieval. Dataset này giúp nhóm đánh giá được ảnh hưởng của chunking strategy, metadata filtering và grounding quality trên các câu hỏi có gold answer kiểm chứng được từ nguồn.
