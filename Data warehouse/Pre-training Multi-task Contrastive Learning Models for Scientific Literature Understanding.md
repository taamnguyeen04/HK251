# Mô hình SciMult xử lý 

Truy vấn (query) – Paper pQ
Ứng viên dương (positive candidate pC⁺)
Ứng viên âm (negative candidates pC⁻)

1. Chuẩn hoá input:
    - pQ: `"[CLS] title [SEP] abstract [SEP]"`.
    - pC⁺ / pC⁻: tương tự.
2. Encode bằng **Bi-Encoder** → ra vector embeddings.
3. Tính similarity $\text{sim}(p_Q, p_C)$.
4. Tối ưu **contrastive loss** (Eq. 2): kéo $(p_Q, p_C^+)$ gần, đẩy $(p_Q, p_C^-)$ ra xa.

___
# Task-Aware Specialization

### Có 3 nhiệm vụ : Classification, Link Prediction, Search

#### Classification
- **Mục tiêu.** Gán **một paper** p vào **nhiều nhãn** (nhãn chắc là lấy trong thằng MeSH)
- **Input :**  Paper, Label
- **Output :** thứ hạng nhãn tinhs theo Sim(Paper, Label)
- **Hard negatives**
- **Contrastive loss**
#### Link Prediction
- **Mục tiêu.** Dự đoán liệu tồn tại **liên kết** giữa **paper truy vấn** $p_Q$​ và **paper ứng viên** $p_C$
- **Input :**  Paper, Candidate (ứng viên là paper nếu PAR, bệnh nhân nếu là PPR)
- **Output :** thứ hạng nhãn tinhs theo Sim(Paper, Candidate)
- **Hard negatives**
- **Contrastive loss**
#### Search
- **Mục tiêu.** Với **truy vấn ngắn** qqq (từ người dùng/hệ thống), truy xuất các **paper** liên quan nhất
-  **Input :**  Paper, Query (query từ người dùng/hệ thống)
- **Output :** thứ hạng nhãn tinhs theo Sim(Paper, Query)
- **Hard negatives, SciRepEval-Search**
- **Contrastive loss**

---

Vì có 3 task mà bắt 1 mô hình học cung 1 lúc thì mô hình dễ bị rối với lú nên  cần kĩ thuật MoE
Trong Transformer, một khối gồm:
- **MHA (Multi-Head Attention)** 
- **FFN (Feed-Forward Network)**
Trong thực nghiệm, paper thấy **MHA** thường hiệu quả hơn, vì attention là chỗ mô hình “hiểu ngữ cảnh” → nếu có chuyên gia riêng cho task thì giảm nhiễu rõ hơn.

#### Instruction Tuning
**Một encoder chung** $E_\theta(\cdot)$ cho mọi task, rồi đưa một câu hướng dẫn ngắnb(instruction) cho mô hình biết đang cần làm gì.

#### Chiến thuật lấy Negative Samples (hard negative)

- Nếu $p_Q$​ trích dẫn $p_C^+$​, và $p_C^+​$ trích dẫn $p_C^-​$, nhưng $p_Q$​ **không** trích dẫn $p_C^-$​ → thì $p_C^-$​ là **hard negative**.

- Với cặp đúng $(p, l^+)$:
	- Lấy một paper p′ có **liên hệ chặt** với p (bị p trích dẫn, cùng tác giả, hoặc cùng venue).
	- Nếu p′ có nhãn l′ **không liên quan tới p** → thì l′ là **hard negative** cho $(p, l^+)$.

- Dữ liệu huấn luyện từ Singh et al. (2022): với mỗi query qqq, search engine trả về một danh sách paper. Các paper **người dùng click** = positive, còn **không click** = **hard negatives**.




## Tóm nhanh (flow MHA-Expert cho PAR)

`JSON → “[CLS] title [SEP] abstract [SEP]” → tokenize/pad → (offline) encode articles qua blocks [chung↔MHA(Link)] → index MIPS → (online) encode patient qua [chung↔MHA(Link)] → sim = dot → top-k → (tuỳ) fine-tune DPR với hard+easy negatives.`
