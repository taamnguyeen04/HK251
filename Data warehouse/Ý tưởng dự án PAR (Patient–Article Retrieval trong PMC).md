## 1. Mục tiêu

Xây dựng hệ thống tìm kiếm và liên kết tự động giữa **bài báo y khoa** (trong PMC) và **thông tin bệnh nhân**.  
Hệ thống vừa giúp truy hồi các bài báo liên quan cho bác sĩ (hoặc nghiên cứu viên), vừa lưu trữ, cập nhật và gắn kết dữ liệu bệnh nhân để phục vụ phân tích và hỗ trợ ra quyết định.

---

## 2. Dữ liệu đầu vào

- **corpus.json**: chứa tập bài báo với metadata cơ bản.
- **PMID2MeSH.json**: ánh xạ bài báo với từ khóa/nhãn MeSH.
- **PMC-Patients.json** và **patient2article_relevance.json**: mô tả mối liên kết giữa bệnh nhân và bài báo liên quan.

Mỗi bài báo được biểu diễn dưới dạng vector embedding từ chuỗi:
`[CLS] title [SEP] abstract [SEP]`

---

## 3. Mô hình biểu diễn

- Sử dụng **PubMedBERT** để embed bài báo (paper embeddings).
- Có thể thêm nhãn (labels/MeSH terms) để tinh chỉnh không gian embedding → phục vụ phân cụm (clustering) và gán nhãn (classification).
- Các vector này được lưu vào **database vector** để truy vấn nhanh.

---

## 4. Nhiệm vụ chính
### 4.1. Classification (Gán nhãn bài báo)
- Dùng embedding của paper + embedding của nhãn.
- Giúp gắn bài báo với chủ đề (MeSH terms), đồng thời hỗ trợ downstream task như phân tích hoặc tổ chức tri thức.

### 4.2. Link Prediction (Dự đoán quan hệ)

- Dựa trên file _patient2article_relevance.json_, mô hình học cách xác định mối quan hệ **bài báo ↔ bệnh nhân**.
- Cho phép mở rộng: từ một bệnh nhân → tìm các bài báo liên quan (Patient-to-Article Retrieval).
- Ngược lại, từ một bài báo → tìm bệnh nhân có đặc điểm phù hợp (Article-to-Patient Link).

### 4.3. Retrieval (Truy hồi thông tin)

- Khi có **mô tả bệnh nhân mới** (patient description query), hệ thống:
    1. Encode mô tả thành vector.
    2. So khớp với vector trong DB (retrieval).
    3. Áp dụng pipeline hai tầng:
        - **Stage 1**: PubMedBERT retrieval (zero-shot).
        - **Stage 2**: Rerank bằng Cross-Encoder để tăng chính xác.
## Học đa nhiệm (Multi-task Learning)

- Các head (classification, link prediction, retrieval) cùng học trên nền embedding chung.
    
- Loss tổng hợp từ nhiều nhiệm vụ giúp encoder học được **không gian biểu diễn đa dụng**: vừa phân loại tốt, vừa dự đoán quan hệ chính xác, vừa hỗ trợ retrieval hiệu quả.
    
- Đây chính là tinh thần của **MHA** trong paper: một backbone, nhiều task head, huấn luyện đồng thời.

---
---
---
---
# Pipeline 2 Phase: Pretraining → Fine-tuning

## **Phase 1: Unsupervised Pretraining (11M abstracts)**

**Mục tiêu:** học embedding tốt, chưa cần nhãn.

### Các chiến lược khả thi:
1. **MLM (Masked Language Modeling)**
    - Tiếp tục pretrain PubMedBERT trên corpus 11M của bạn.
    - Mục đích: domain adaptation, model quen văn phong + từ vựng mới.
2. **Contrastive Pretraining từ metadata (không cần nhãn thủ công)**
    - Positive pairs:
        - (title, abstract)
        - (abstract, conclusion / intro)
        - (citing paper, cited paper)
    - Negative: random.
    - Loss = InfoNCE.
    - Ưu: embedding học trực tiếp cách “phân biệt văn bản liên quan vs không liên quan”.
        
👉 Nếu muốn embedding tốt cho retrieval, **contrastive learning là bắt buộc**, MLM chỉ nên là bước phụ để adapt.

---

## **Phase 2: Supervised Fine-tuning (32k MeSH + 167k relevance)**
**Mục tiêu:** align encoder với ontology MeSH và task PAR.
### Multi-task training:
- Loss function:
    `L = α * L_contrastive + β * L_mesh + γ * L_relevance`
    - `L_contrastive`: contrastive loss từ phase 1 (có thể giữ nhẹ để regularize).
    - `L_mesh`: BCE loss cho multi-label MeSH classification.
    - `L_relevance`: contrastive/triplet loss cho patient–article relevance.
- Cách chia batch:
    - 1 batch contrastive (unsup).
    - 1 batch MeSH.
    - 1 batch patient relevance.
    - Cộng loss theo hệ số.

👉 Bước này sẽ tránh overfit vì model đã “cứng” nhờ pretraining 11M.

---
# ⚡ Một số mẹo để mô hình tốt hơn “một chút”:

1. **Layer-wise learning rate decay** khi fine-tune:
    - Encoder layers LR nhỏ.
    - Classification head LR lớn.
2. **Hard negative mining** cho contrastive:
    - Negative = doc cùng disease nhưng khác treatment → khó phân biệt.
3. **Curriculum training**:
    - Phase 1 chỉ unsupervised.
    - Phase 2 supervised nhưng ban đầu LR nhỏ + α lớn (ưu tiên unsup).
    - Sau vài epoch → tăng dần β, γ (ưu tiên supervised).
4. **Pseudo-labeling** sau fine-tune:
    - Dùng model đã fine-tuned → sinh thêm MeSH/patient label cho data unlabelled.
    - Re-train lại → model align hơn.



---
---
---
---
---
---
---
---

Tổng quan chiến lược (tóm tắt)

Unsupervised backbone trên 11M (contrastive pretrain) — bắt buộc để có embedding tốt cho retrieval & clustering.

Weak / distant supervision — dùng MeSH, metadata, string-match, UMLS để gán nhãn tạm cho nhiều paper hơn.

Pseudo-labeling + self-training loop — mở rộng nhãn MeSH/patient bằng model đã fine-tune, lọc bằng confidence.

Label propagation trên graph — gán nhãn qua cấu trúc citation / co-authorship / similarity graph.

Active learning / human-in-loop — chỉ cho bác sĩ/annotator xem top uncertain samples.

Multi-task fine-tune: kết hợp tất cả (MeSH, relevance) với regularization từ unsupervised contrastive.

Kết hợp các bước trên sẽ cho hiệu quả tốt hơn: unsupervised cung cấp backbone ổn định, weak supervision + pseudo-labeling tăng coverage nhãn, label propagation tận dụng cấu trúc tài liệu.

Chi tiết giải pháp & cách triển khai (theo thứ tự ưu tiên)
A. code phần Pretrain contrastive trên 11M (unsupervised)
Mục tiêu: học embedding domain-specific cho retrieval và clustering.
Method: InfoNCE / SimCLR style using pairs: (title, abstract).
Batch size: càng lớn càng tốt (128–1024)
Embedding projection dim:theo số chiều của "microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract-fulltext", L2-normalize.
Kết quả mong đợi: embedding giúp tìm gần nhau các paper tương tự → cơ sở cho bước label propagation và pseudo-label.

B. Weak / Distant Supervision (mở rộng MeSH & patient labels)

Nguồn tín hiệu:

PMID2MeSH: map sẵn cho một số papers → seed labels.

String matching / synonyms: dùng UMLS / MeSH synonyms / scispacy NER để detect disease/drug/phenotype trong abstract → map lại MeSH hoặc cluster mới.

Metadata signals: journal, title keywords, citation edges, references, authors — dùng rules để gán nhãn tạm.

Cross-document heuristics: nếu nhiều paper cite same review, inherit its MeSH.

Practical:

Dùng scispacy + UMLS lookup để tìm candidate MeSH per abstract.

Gán confidence score theo rule (exact match high, fuzzy match thấp).

Lưu nhãn “soft” (probability) chứ không ghi đè nhãn gốc.

C. Pseudo-labeling / Self-training loop (scale-up labels automatically)

Quy trình:

Fine-tune MeSH classifier + relevance head trên 32k MeSH + 100k patient (supervised).

Áp model lên phần unlabeled (11M minus labeled). Lấy những dự đoán có confidence cao > τ.

τ ban đầu cao (0.9) → tránh noise. Sau một vòng, hạ τ xuống 0.8 để thêm volume.

Thêm pseudo-labeled examples vào train set (gán weight thấp hoặc dùng label smoothing).

Re-train model (hoặc continue fine-tune) với mix of true labels + pseudo labels (use smaller lr on pseudo).

Lặp lại 2–4 vài lần; dùng validation strict để kiểm soát drift.

Hyperparams khởi điểm:

Initial τ = 0.9, second round τ = 0.85, third τ = 0.8.

Weight for pseudo labels in loss: 0.5 (trước đó 1.0 cho ground-truth).

Max percent of unlabeled accepted per round: 5–10% of corpus để giảm noise.

D. Graph-based label propagation (tận dụng citation / similarity graph)

Xây graph nodes = papers; edges = citation edges và similarity edges (k-NN in embedding space, k=5–20).

Seed nodes = papers có MeSH (32k) + high-confidence pseudo-labeled.

Sử dụng Label Propagation / Graph Neural Network (GCN) để lan tỏa label probabilities.

Điều chỉnh: normalize edge weights; giới hạn propagation depth; early stopping based on validation.

Advantages: lan nhãn tốt cho cụm tài liệu liên quan - hữu ích khi MeSH cover một số chủ đề nhưng thiếu cho nhiều paper.

E. Clustering + cluster labeling

Cluster 11M embedding (approx): dùng scalable approach — HNSW/IVF + k-means on IVF centroids hoặc MiniBatchKMeans trên sample, sau đó assign.

Cho mỗi cluster, aggregate keywords / top-N tf-idf terms → propose MeSH / label for cluster.

Human-in-loop: chỉ review top clusters (ví dụ 1k clusters) để gán nhãn nhanh hàng loạt.

F. Zero-shot / LLM-based labeling (khi cần cover niche)

Dùng LLM (e.g., instruction-tuned biomedical LLM hoặc general LLM with prompt) để gợi MeSH candidates per abstract/title.

Ưu: có thể nhanh chóng tạo nhãn cho các paper lạ; Nhược: chi phí & cần kiểm soát chất lượng.

Dùng làm nguồn weak label kết hợp confidence scoring.

G. Hard negative mining & curriculum

Khi học relevance, nếu nhãn bị imbalanced, mining hard negatives từ papers có cùng MeSH nhưng không relevant → cải thiện discriminative power.

Một pipeline kết hợp mẫu (áp dụng ngay)

Pretrain contrastive trên 11M → lưu embeddings.

Seed expansion: apply scispacy(UMLS)/string-match → generate soft MeSH labels for ~X% papers.

Fine-tune supervised on true labels (32k MeSH + 100k patient) + weighted soft labels.

Pseudo-label pass 1: predict unlabeled → accept high-confidence (τ=0.9) → add to training as pseudo (weight 0.5).

Re-train (or continue) with mixed dataset.

Label propagation on citation + k-NN graph → smooth labels across graph.

Cross-encoder rerank fine-tune using high-quality relevance pairs.

Active learning: sample most uncertain or high-impact clusters for human annotation to bootstrap next loop.
