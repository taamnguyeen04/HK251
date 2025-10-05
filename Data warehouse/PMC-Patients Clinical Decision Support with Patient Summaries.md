<audio controls>
  <source src="audio/PMC-Patients.m4a" type="audio/mpeg">
  Trình duyệt của bạn không hỗ trợ phát audio.
</audio>

[PMC-Patients dataset](https://github.com/pmc-patients/pmc-patients)
[PMC-Patients benchmark](https://github.com/pmc-patients/pmc-patients)
[PMC-Patients leaderboard](https://pmc-patients.github.io/)
# Tổng quan ngắn

**PMC-Patients** là một dataset lớn trích xuất từ case-reports trên PubMed Central (PMC). Mục tiêu chính: làm benchmark cho các hệ thống **Retrieval-based Clinical Decision Support (ReCDS)** — tức hệ thống tìm tài liệu/bệnh nhân liên quan để hỗ trợ quyết định lâm sàng. Dataset chứa:

- ~**167k** bản tóm tắt bệnh nhân (patient summaries),
- ~**3.1M** cặp patient-article relevance,
- ~**293k** cặp patient-patient similarity.
# 1) PMC-Patients (file chính: `PMC-Patients.json`)

`PMC-Patients.json` là file “core” chứa tất cả thông tin patient. Mỗi phần tử là một dictionary (một record bệnh nhân) với các trường chính:
- **patient_id**: `string` — id liên tiếp (bắt đầu 0).  
    Ví dụ: `"0"`, `"1"`.
- **patient_uid**: `string` — định danh duy nhất dạng `PMID-x` (PMID là PubMed ID của bài báo nguồn; x là chỉ số note trong bài).  
    Ví dụ: `"3996084-1"` (bài có PMID 3996084, note thứ 1).
- **PMID**: `string` — PubMed Identifier của bài báo nguồn.
- **file_path**: `string` — đường dẫn tới file XML của bài báo nguồn (trong bộ dữ liệu gốc).
- **title**: `string` — tiêu đề bài báo nguồn.
- **patient**: `string` — **nội dung tóm tắt bệnh nhân** (patient note) — đây là text bạn thường dùng làm query cho task PAR hoặc làm document cho PPR.
- **age**: `list of tuples` — mỗi phần là `(value, unit)`; `unit` ∈ {'year','month','week','day','hour'}.  
    Ví dụ: `[[1.0, "year"], [2.0, "month"]]` → em bé 1 năm 2 tháng.
- **gender**: `'M'` hoặc `'F'`.
- **relevant_articles**: `dict` — key = PMID của article liên quan, value = score (2 hoặc 1). (dùng cho PAR ground truth trong file tổng hợp này).
- **similar_patients**: `dict` — key = patient_uid của patient tương tự, value = similarity score (2 hoặc 1).

**Lưu ý:** `relevant_articles` và `similar_patients` là annotation gốc từ quá trình thu thập dữ liệu. Tuy nhiên, khi author tách train/dev/test cho benchmark, **qrels** (xem bên dưới) có thể khác với thông tin này — vì có thể một số target đã được loại vào set train/dev/test khác nhau.

# 2) PMC-Patients ReCDS benchmark (định dạng giống BEIR)

Để benchmark họ cung cấp dữ liệu theo **mô hình retrieval** chuẩn — gồm **queries**, **corpus**, và **qrels** (TREC style). Có hai task:
- **PAR (Patient-to-Article Retrieval)**: input = patient summary (query), output = bài báo PubMed liên quan (document).
- **PPR (Patient-to-Patient Retrieval)**: input = patient summary (query), output = patient summaries khác có độ tương tự.

## Queries
- Có cho từng split `train`, `dev`, `test`.
- File là **JSONL** (mỗi dòng 1 JSON object). Mỗi object có:
    - `_id`: `patient_uid` (unique query id), ví dụ `"3996084-1"`.
    - `text`: nội dung patient summary (chuỗi văn bản) — đây chính là query text.

## Corpus

- File **jsonl** chung cho task:
    - **PAR corpus**: ~**11.7M** PubMed articles (rất lớn). Mỗi record:
        - `_id`: PMID (document id)
        - `title`: title of article
        - `text`: abstract (nội dung document để tìm)
    - **PPR corpus**: ~**155.2k** reference patients (là subset từ PMC-Patients). Mỗi record:
        - `_id`: patient_uid
        - `title`: thường là chuỗi rỗng cho PPR
        - `text`: patient summary (đây là document text khi tìm patient tương tự)

**Lưu ý về kích thước:** PAR corpus rất lớn — cần lưu ý về không gian đĩa, indexing (faiss / ElasticSearch / Anserini …) và cách xử lý streaming.

## Qrels (TREC-style .tsv)

- File qrels là TSV có 3 cột: `query_id`, `corpus_id`, `score` (tab-separated).
    - `score` = 2 (mức liên quan cao) hoặc 1 (liên quan thấp).
- Qrels là ground truth để đánh giá retrieval (tương ứng với train/dev/test split).
    
**Lưu ý:** qrels có thể khác với `relevant_articles`/`similar_patients` trong `PMC-Patients.json` vì split dataset và quy trình chia sample — luôn dùng qrels tương ứng với split bạn chạy.

# 3) Evaluation & Submission

- Họ cung cấp code đánh giá dựa trên **BEIR** (thường là tính các metrics retrieval).
- **Định dạng kết quả (result file)** mà evaluation.py mong đợi: một JSON mapping `query_id` → `{doc_id: score, doc_id2: score2, ...}`.  
    Ví dụ:

`{   "3996084-1": {     "8821503": 360.5629,     "15793714": 359.9751   },   "6250493-1": {     "27524922": 340.9844   } }`

- Sau đó chạy:
`python evaluation.py --task PPR --split test --result_path YOUR_RESULT_PATH`

(`--task` là `PAR` hoặc `PPR`; `--split` là `train`/`dev`/`test`)

- Nếu muốn submit leaderboard: gửi email chứa retrieval scores (file kết quả) + mô tả ngắn hệ thống tới tác giả (địa chỉ email được nêu trong trang).

# 4) Một số metrics thường dùng (đã xuất hiện trên trang/leaderboard)

- **MRR (Mean Reciprocal Rank)**: trung bình 1/rank của first relevant doc. Đánh giá tìm đúng doc liên quan càng sớm càng tốt.
- **P@10 (Precision at 10)**: tỷ lệ document relevant trong top-10 trả về.
- **nDCG@10**: normalized Discounted Cumulative Gain ở cutoff 10 — tính đến mức độ liên quan (2 > 1).
- **R@1k (Recall at 1000)**: có lấy bao nhiêu relevant docs trong top-1000.

Các chỉ số này phản ánh cả **độ chính xác vị trí top** (MRR, P@10, nDCG) và **khả năng thu hồi** (Recall@k).

# 5) Lưu ý thực tiễn khi xử lý dataset này

- **Tệp rất lớn** (ví dụ PAR corpus 11.7M articles) → không thể load toàn bộ vào RAM. Dùng:
    - indexing (FAISS, Anserini, Elasticsearch), hoặc
    - streaming / chunked processing (pandas `read_json(..., lines=True, chunksize=...)`), hoặc
    - xử lý offline: build sparse index (BM25) với Anserini/Whoosh hay dense index với FAISS/HNSW.
- **Format chuẩn**: giữ nguyên cấu trúc jsonl/csv và đặt folder `datasets` như hướng dẫn nếu bạn dùng evaluation code kèm theo.
- **Đồng nhất ID**: `_id` trong queries phải khớp `query_id` trong qrels và với `_id` trong corpus (PMID hoặc patient_uid) — nếu không, evaluation sẽ bỏ qua.
- **Tạo result file**: đảm bảo giá trị score là số (float) và không nhất thiết phải normalized.
- **Độ liên quan đa mức**: vì qrels có 2 mức (2 hoặc 1), khi tính nDCG hoặc learning-to-rank bạn nên tận dụng trọng số này.

# 6) Baseline
citation graph của PubMed cũng ngầu
## 6.1) Sparse retriever
- Xử lý dữ liệu có sẵn:
	- Trích xuất các thông tin quan trọng từ file PMC-Patients.json và cospus.jsonl
	- Chuẩn hóa dữ liệu theo pipeline NLP (làm sạch, tokenize,...) tập trung vào **title**, **abstract**, **patient summary**.
	- Lưu vào elasticsearch
- Xử lý thông tin bệnh nhân mới vô:
	- Thu thập các thông tin cần thiết về bệnh nhân
	- Truy vấn dựa vào BM25 tính similarity giữa query và các articles trong DB
- Trả về kết quả
## 6.2) Dense retriever
- Một số mô hình encoder PubMedBERT ngầu, ClinicalBERT vs BioLinkBERT cũng ngầu
- Xử lý dữ liệu có sẵn giống trên nhưng ở bước lưu vô elastic thì đổi thành dùng mô hình encoder -> vector -> FAISS, Milvus, Weaviate, Pinecone
- Bệnh nhân mới vô thì thu thập thông tin rồi chuyển thành vector rồi tính tương đồng
- Kết quả có thể rerank bằng cross-encoder
## 6.3) K Nearest Neighbor (KNN) retriever
- Ý tưởng: Nếu hai bệnh nhân tương tự nhau, thì tập relevant articles của họ cũng sẽ giống nhau.
- Quy trình:
    1. Với mỗi query patient q, tìm K bệnh nhân gần nhất trong tập training bằng BM25.
    2. Lấy union tập relevant articles của các bệnh nhân này → candidate set.
    3. Ranking lại các candidate bằng score sNN(q, ci) dựa trên độ tương đồng BM25 giữa q và từng neighbor pk, có trọng số nếu article ci thuộc R(pk).