# Bao Cao Lab 7: Embedding & Vector Store

**Ho ten:** Nguyen Trong Tan  
**Nhom:** DigitalOcean Knowledge Bases Docs  
**Ngay:** 05/06/2026

---

## 1. Warm-up

### Cosine Similarity

**High cosine similarity nghia la gi?**  
Hai text chunks co high cosine similarity khi vector embedding cua chung nam gan cung huong trong khong gian vector. Dieu nay thuong co nghia la hai doan noi ve noi dung hoac y dinh tuong tu nhau, du co the dung tu khac nhau.

**Vi du HIGH similarity:**
- Sentence A: "Vector databases store embeddings for similarity search."
- Sentence B: "A vector store keeps embedding vectors so users can find similar documents."
- Tai sao tuong dong: ca hai deu noi ve vector store, embeddings va similarity search.

**Vi du LOW similarity:**
- Sentence A: "Metadata filters narrow retrieval results to relevant documents."
- Sentence B: "A chocolate cake needs flour, sugar, and butter."
- Tai sao khac: hai cau thuoc hai domain khac nhau, mot cau ve retrieval, mot cau ve nau an.

**Tai sao cosine similarity duoc uu tien hon Euclidean distance cho text embeddings?**  
Cosine similarity tap trung vao huong cua vector, nen phu hop voi viec do muc do giong nhau ve nghia. Euclidean distance bi anh huong nhieu boi do lon vector, trong khi text embedding thuong quan trong huong ngu nghia hon khoang cach hinh hoc tuyet doi.

### Chunking Math

**Document 10,000 ky tu, chunk_size=500, overlap=50. Bao nhieu chunks?**

Formula:

```text
num_chunks = ceil((doc_length - overlap) / (chunk_size - overlap))
           = ceil((10000 - 50) / (500 - 50))
           = ceil(9950 / 450)
           = ceil(22.11)
           = 23 chunks
```

**Neu overlap tang len 100 thi sao?**

```text
num_chunks = ceil((10000 - 100) / (500 - 100))
           = ceil(9900 / 400)
           = ceil(24.75)
           = 25 chunks
```

Overlap lon hon lam tang so chunk, nhung giup giu lai context giua hai chunk lien tiep. Dieu nay huu ich khi cau tra loi nam sat ranh gioi giua hai chunk.

---

## 2. Document Selection - Nhom

### Domain & Ly Do Chon

**Domain:** DigitalOcean Knowledge Bases / RAG documentation.

Nhom chon DigitalOcean Knowledge Bases docs vi tai lieu lien quan truc tiep den embedding, chunking, retrieval, metadata filtering va reranking. Day la bo docs cong khai, co URL ro rang, cau truc Markdown nhieu heading, rat phu hop de so sanh cac chunking strategy.

### Data Inventory

| # | Ten tai lieu | Nguon | So ky tu | Metadata da gan |
|---|---|---|---:|---|
| 1 | `do_retrieval_best_practices.md` | DigitalOcean Docs | 6779 | `category=retrieval`, `doc_type=concept`, `audience=developer` |
| 2 | `do_chunking_best_practices.md` | DigitalOcean Docs | 8507 | `category=chunking`, `doc_type=concept`, `audience=developer` |
| 3 | `do_system_instructions_best_practices.md` | DigitalOcean Docs | 2323 | `category=prompting`, `doc_type=concept`, `audience=developer` |
| 4 | `do_create_knowledge_bases.md` | DigitalOcean Docs | 26682 | `category=setup`, `doc_type=how_to`, `audience=operator` |
| 5 | `do_test_knowledge_bases.md` | DigitalOcean Docs | 16414 | `category=evaluation`, `doc_type=how_to`, `audience=operator` |

### Metadata Schema

| Truong metadata | Kieu | Vi du gia tri | Tai sao huu ich cho retrieval? |
|---|---|---|---|
| `doc_id` | string | `do_retrieval_best_practices` | Xac dinh tai lieu goc va dung de delete/filter. |
| `source` | string | `DigitalOcean Docs` | Ghi nguon trong report va demo. |
| `url` | string | URL goc | Trace lai evidence va gold answer. |
| `category` | string | `retrieval`, `chunking` | Loc theo chu de khi query ro domain. |
| `doc_type` | string | `concept`, `how_to` | Phan biet tai lieu giai thich va huong dan thao tac. |
| `language` | string | `en` | Ghi ngon ngu tai lieu. |
| `audience` | string | `developer`, `operator` | Loc theo nhom nguoi dung hoac muc dich su dung. |

---

## 3. Chunking Strategy

### Baseline Analysis

Chay `ChunkingStrategyComparator().compare()` tren 2 tai lieu voi `chunk_size=700`.

| Tai lieu | Strategy | Chunk Count | Avg Length | Preserves Context? |
|---|---|---:|---:|---|
| `do_retrieval_best_practices.md` | FixedSizeChunker | 11 | 679.9 | Trung binh, co the cat ngang section |
| `do_retrieval_best_practices.md` | SentenceChunker | 10 | 675.8 | Tot hon ve cau, nhung khong bam heading |
| `do_retrieval_best_practices.md` | RecursiveChunker | 13 | 511.5 | Tot, giu paragraph/section nho hon |
| `do_chunking_best_practices.md` | FixedSizeChunker | 14 | 672.6 | Trung binh |
| `do_chunking_best_practices.md` | SentenceChunker | 20 | 423.1 | De doc, nhieu chunk hon |
| `do_chunking_best_practices.md` | RecursiveChunker | 17 | 498.6 | Can bang size va context |

### Strategy Cua Toi

**Loai:** Custom Markdown Heading Chunker.

Strategy cua toi chia tai lieu Markdown theo heading `#`, `##`, `###`. Moi chunk giu heading va noi dung ben duoi heading de khi retrieve co the trace ve section goc. Neu mot section qua dai, chunker fallback sang `RecursiveChunker` de chia nho body nhung van gan lai heading len tung chunk con.

**Tai sao chon strategy nay cho domain nhom?**  
DigitalOcean docs co cau truc heading ro rang theo concept/how-to/reference. Vi vay chia theo heading phu hop hon fixed-size, vi ranh gioi heading thuong la ranh gioi y nghia that cua tai lieu. Cach nay cung de giai thich khi demo: query hoi concept nao thi ky vong retrieve dung section do.

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

### So Sanh: Strategy cua toi vs Baseline

| Tai lieu | Strategy | Chunk Count | Avg Length | Retrieval Quality? |
|---|---|---:|---:|---|
| `do_retrieval_best_practices.md` | best baseline: RecursiveChunker | 13 | 511.5 | Tot, nhung heading trace khong ro bang custom |
| `do_retrieval_best_practices.md` | **MarkdownHeadingChunker** | 11 | ~616 | Tot, top-3 relevant voi retrieval queries |
| `do_chunking_best_practices.md` | best baseline: RecursiveChunker | 17 | 498.6 | Tot, chia paragraph on dinh |
| `do_chunking_best_practices.md` | **MarkdownHeadingChunker** | 16 | ~532 | Tot, giu heading nhu `Improve Chunking Performance` |

### So Sanh Voi Thanh Vien Khac

| Thanh vien | Strategy | Retrieval Score (/10) | Diem manh | Diem yeu |
|---|---|---:|---|---|
|Nguyễn Trọng Tấn-2A202600901 | Markdown heading custom | 9 | Trace dung section, co rationale ro | Can fallback khi section dai |
| Chuc | Fixed-size baseline | TBD | Don gian, on dinh | De cat ngang y/heading |
| Quang | Sentence-based | TBD | Chunk de doc | Size khong deu, khong bam heading |
| Lam | Recursive | TBD | Can bang context va size | Can tune separator |

**Strategy nao tot nhat cho domain nay?**  
Voi DigitalOcean docs, Markdown heading custom rat phu hop vi docs co section ro rang va query thuong hoi theo concept. Recursive chunking co the la baseline manh, nhung heading custom de trace nguon hon va de trinh bay trong demo hon.

---

## 4. My Approach - Ca Nhan

### Chunking Functions

**`SentenceChunker.chunk`**  
Dung regex `(?<=[.!?])(?:\s+|\n+)` de tach cau sau dau `.`, `!`, `?`. Sau do gom moi `max_sentences_per_chunk` cau thanh mot chunk va strip whitespace. Edge case: text rong tra ve `[]`.

**`RecursiveChunker.chunk` / `_split`**  
Thuat toan thu cac separator theo thu tu uu tien `\n\n`, `\n`, `. `, space, sau do moi fallback fixed-size. Base case la khi text da nho hon `chunk_size`. Neu mot piece van qua dai, ham tiep tuc recurse voi separator tiep theo.

### EmbeddingStore

**`add_documents` + `search`**  
Moi `Document` duoc normalize thanh record gom `id`, `doc_id`, `content`, `metadata`, `embedding`. Search embed query, tinh cosine similarity voi tung record, sort score giam dan va tra ve top-k.

**`search_with_filter` + `delete_document`**  
`search_with_filter` filter metadata truoc, roi moi search tren tap ung vien da loc. `delete_document` xoa tat ca chunk co `metadata['doc_id']` hoac `doc_id` trung voi document can xoa.

### KnowledgeBaseAgent

**`answer`**  
Agent retrieve top-k chunk tu store, ghep thanh context co nhan `[Source 1]`, `[Source 2]`, sau do tao prompt yeu cau LLM chi tra loi dua tren context. Cach nay theo pattern RAG: retrieve truoc, generate sau.

### Test Results

```text
pytest tests/ -v
42 passed
```

**So tests pass:** 42 / 42

---

## 5. Similarity Predictions

Dung `_mock_embed` de embed cau, sau do goi `compute_similarity()`.

| Pair | Sentence A | Sentence B | Du doan | Actual Score | Dung? |
|---|---|---|---|---:|---|
| 1 | Python programming tutorial | Python coding guide for developers | high | 0.052 | Khong |
| 2 | Knowledge base retrieval uses chunks | Vector search retrieves relevant document chunks | high | -0.142 | Khong |
| 3 | Hybrid search combines semantic and keyword search | Reranking improves the order of retrieved chunks | medium | 0.081 | Gan dung |
| 4 | Create a database cluster | Bake a chocolate cake | low | -0.067 | Dung |
| 5 | Metadata filters narrow retrieval results | Marketing campaign budget planning | low | 0.037 | Dung |

**Ket qua bat ngo nhat:**  
Hai cau retrieval/chunking o pair 2 ve nghia kha gan nhau nhung score lai am. Dieu nay cho thay `_mock_embed` chi phu hop cho test deterministic cua lab, khong phai embedding semantic that. Khi benchmark nghiem tuc nen dung local embedder hoac OpenAI embedder.

---

## 6. Results - Ca Nhan

### Benchmark Queries & Gold Answers

| # | Query | Gold Answer |
|---|---|---|
| 1 | What are DigitalOcean's recommended best practices for a strong retrieval setup? | Nen can bang semantic/keyword search, dung filters, test chunking khi ket qua bi fragmented/noisy, va enable reranking khi can sap xep lai chunk lien quan. |
| 2 | Why can chunks that are too small or too large hurt retrieval quality? | Chunk qua nho lam mat context; chunk qua lon co the chua noi dung khong lien quan va lam giam do chinh xac retrieval. |
| 3 | When should filters be used in knowledge base retrieval? | Dung filters khi can gioi han retrieval theo document, file, metadata hoac URL path de tranh lay nham nguon. |
| 4 | What is the difference between chunking, retrieval, and reranking in a RAG system? | Chunking chia data de index; retrieval chon candidate chunks; reranking sap xep lai candidate chunks truoc khi dua vao LLM. |
| 5 | How should a team test whether a knowledge base returns useful answers? | Test bang query thuc te, xem top-k chunks, so sanh filtered/unfiltered search, va doi chieu answer voi source evidence. |

### Ket Qua Cua Toi

Benchmark chay bang `benchmark_digitalocean_heading.py`, strategy `MarkdownHeadingChunker`, filter theo `category` khi query co chu de ro.

| # | Query | Top-1 Retrieved Chunk | Score | Relevant? | Agent Answer tom tat |
|---|---|---|---:|---|---|
| 1 | Strong retrieval setup best practices | `Retrieval Example` / retrieval docs | 0.707 | Yes | Can dung hybrid retrieval, filters, chunking test va reranking. |
| 2 | Chunks too small/large | `Improve Chunking Performance` / chunking docs | 0.378 | Yes | Chunk size anh huong context va noise; can test/tune chunking. |
| 3 | When use filters | `DigitalOcean Knowledge Base Retrieval Best Practices` | 0.781 | Yes | Filters gioi han ket qua theo file, document, metadata, URL path. |
| 4 | Chunking vs retrieval vs reranking | `DigitalOcean Knowledge Base Retrieval Best Practices` | 0.880 | Yes | Chunking tao indexed data, retrieval lay candidates, reranking sap xep lai. |
| 5 | Test useful answers | `Test Reranking` / evaluation docs | 0.862 | Yes | Kiem tra retrieval/reranking bang query va source evidence. |

**Bao nhieu queries tra ve chunk relevant trong top-3?** 5 / 5

---

## 7. What I Learned

**Dieu hay nhat toi hoc duoc tu thanh vien khac trong nhom:**  
Fixed-size baseline rat can thiet vi no tao moc so sanh don gian. Sentence-based va recursive chunking giup thay ro trade-off giua readability, chunk count va context preservation.

**Dieu hay nhat toi hoc duoc tu nhom khac qua demo:**  
Can danh gia retrieval bang evidence, khong chi nhin score. Top-1 cao nhung sai source van co the lam agent tra loi sai.

**Neu lam lai, toi se thay doi gi trong data strategy?**  
Toi se lay them 2 file reference/how-to de benchmark co nhieu case hon, dac biet query ve parameter va data source management. Toi cung se dung local semantic embedder thay vi mock/keyword embedder de ket qua gan thuc te hon.

### Failure Analysis

**Failure case:** Query 4 co top-2 la `Configure Reranking` trong category `setup`, khong nam trong expected category `retrieval/chunking`.  
**Nguyen nhan:** Query co tu "reranking" nen lexical embedding uu tien chunk nao lap lai tu nay, du context chinh cua cau hoi la phan biet chunking, retrieval va reranking.  
**Cai thien:** Dung semantic embedding that, them metadata filter `category=retrieval` hoac tang trong so cho heading/context thay vi chi dem keyword.

---

## Tu Danh Gia

| Tieu chi | Loai | Diem tu danh gia |
|---|---|---:|
| Warm-up | Ca nhan | 5 / 5 |
| Document selection | Nhom | 9 / 10 |
| Chunking strategy | Nhom | 14 / 15 |
| My approach | Ca nhan | 10 / 10 |
| Similarity predictions | Ca nhan | 4 / 5 |
| Results | Ca nhan | 9 / 10 |
| Core implementation (tests) | Ca nhan | 30 / 30 |
| Demo | Nhom | 4 / 5 |
| **Tong** | | **95 / 100** |
