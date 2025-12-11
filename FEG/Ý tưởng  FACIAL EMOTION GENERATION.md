				SINH ẢNH CẢM XÚC TỪ KHUÔN MẶT
## 1) Ý tưởng cốt lõi

- **Làm việc trong miền wavelet**: biến đổi ảnh sang 4 sub-band **LL, LH, HL, HH** bằng **DWT** (ảnh RGB → 12 kênh sau concat) rồi **denoise hoàn toàn trong miền này**; cuối cùng **IWT** để khôi phục ảnh. Điều này giảm kích thước không gian làm việc xuống **H/2×W/2** (tiết kiệm FLOPs) đồng thời giữ/cấy chi tiết tần số cao qua đường skip tần số khi upsample.

- **UNet tần số** (encoder–bottleneck–decoder) dùng:
    - **Frequency-aware downsampling/upsampling**: tách **lo-sub** để xử lý (giảm mẫu) và **giữ hi-sub** (LH/HL/HH) chuyển thẳng sang decoder cho **IWT** khi tăng mẫu → khôi phục chi tiết đúng “nguồn gốc”.
    - **Frequency bottleneck**: ở đáy UNet, chỉ **xử lý low-frequency**, **truyền thẳng high-frequency** rồi **IWT** ghép lại → học cấu trúc thô hiệu quả mà vẫn bảo toàn chi tiết.
    - **Frequency residual from source**: ở mỗi mức encoder, **DWT ảnh nguồn** → concat → conv 1×1 → **add** vào feature encoder để bơm “dấu vết tần số gốc” ngay từ sớm.
- **Khác paper gốc**: thay vì G/D (DDGAN), ta dùng **DDPM thuần** (mục tiêu dự đoán nhiễu $\epsilon$) nhưng **giữ toàn bộ cơ chế wavelet** ở mức ảnh & feature như trên.

---
## 2) Điều kiện (conditioning) cho “chỉnh cảm xúc theo prompt”

Mapping từ prompt/nhãn (emotion), **landmarks**, **valence/arousal** đến thay đổi biểu cảm đúng vùng, đúng cường độ:
- **Văn bản (prompt)**:  phân loại -> emotion (dùng như cũ hoặc api gemini)
- **Landmarks**: rasterize thành **heatmaps đa kênh** (môi, mắt, lông mày, mũi…) + optional face-parsing mask. Đây là “bản đồ hình học” neo vị trí biến đổi (miệng cười, nhíu mày…).
- **Expression (categorical)**: one-hot (hoặc label smoothing) → MLP → embedding.
- **Valence/Arousal (liên tục)**: chuẩn hoá [−1,1]  → MLP → embedding; dùng làm **knob cường độ**.
- **Trộn điều kiện**: hợp nhất mọi embedding vào **timestep embedding** (FiLM/AdaGN) của từng block **và** đưa thêm **mask/heatmaps** như **kênh vào** (concat) ở encoder mức đầu.

---
## 3) Kiến trúc chi tiết (WaveEmotion-DDPM)

### 3.1 Front-end (miền wavelet)

- Ảnh nguồn  → **DWT** → [LL,LH,HL,HH] theo kênh (RGB ⇒ 12 kênh) → **Conv 1×1** chiếu về D kênh cơ sở → $y_0$ (miền wavelet).

- Trong training, lấy **noise schedule** (cosine hoặc linear) theo phần [[add noise]]

### 3.2 UNet tần số (backbone dự đoán)

![[Pasted image 20250915022408.png]]
---
![[Pasted image 20250915022421.png]]


## 4) Mục tiêu huấn luyện

- **DDPM loss (wavelet-space)**:
    $\mathcal{L}_{\text{DDPM}}=\mathbb{E}_{y_0,t,\epsilon}\big[\|\epsilon-\epsilon_\theta(y_t,t,c)\|_2^2\big]$
- **Wavelet reconstruction consistency**: tăng ổn định **giữa sub-band** (nhẹ, tùy chọn). Dự đoán $\hat{y}_0$​ bằng công thức DDPM :
    $\mathcal{L}_{\text{wav}}=\sum_{s\in\{LL,LH,HL,HH\}}\lambda_s\| \hat{y}_0^{(s)}-y_0^{(s)} \|_1$
    (đặt $\lambda_{LH,HL,HH} > \lambda_{LL}$ để **ưu tiên chi tiết**).
- **Loss theo điều kiện cảm xúc**:
    - **Expression CE loss**: classifier phụ $\Phi$ trên ảnh IWT($\hat{y}_0$​) dự đoán nhãn **expression** phù hợp prompt → $\mathcal{L}_{\text{expr}}$​.
    - **Valence/Arousal regression**: regressor phụ $\Psi$ dự đoán v,av,av,a khớp điều kiện → $\mathcal{L}_{VA}$​.
    - **Landmark alignment**: detector landmarks $\Omega$ trên output khớp **heatmaps đích** (từ prompt/nhãn) → $\mathcal{L}_{\text{lm}}$​.
- **Identity preservation**: **ArcFace cosine** giữa input và output (cắt vùng mặt) → $\mathcal{L}_{\text{id}}$​.
- **Perceptual** (LPIPS) và **masked L1/L2** trên **vùng ngoài mặt** để **giữ background**.

 Tổng: $\mathcal{L} = \mathcal{L}_{\text{DDPM}} + \lambda_{\text{wav}}\mathcal{L}_{\text{wav}} + \lambda_{\text{expr}}\mathcal{L}_{\text{expr}} + \lambda_{VA}\mathcal{L}_{VA} + \lambda_{\text{lm}}\mathcal{L}_{\text{lm}} + \lambda_{\text{id}}\mathcal{L}_{\text{id}} + \lambda_{\text{perc}}\mathcal{L}_{\text{perc}}​$.

---

## 5) Thí nghiệm đề xuất

- **Kiến trúc**:
    1. DDPM pixel-space vs **WaveEmotion-DDPM** (wavelet).
    2. **Haar vs bior4.4 vs bior1.5** ;
    3. Vùng tần số add noise:  
	    1. Cao HL, LH, HH
	    2. Thấp LL
	    3. Cao, thấp LL, LH, HL, HH
    4. Add noise linear vs cosine
        
- **Điều kiện**: 
    - Expr
    - Expr+VA
    - Expr+Landmarks
    - Expr+VA+Landmarks.
    -  Một số bài tham khảo: [EmoStyle](https://openaccess.thecvf.com/content/WACV2024/papers/Azari_EmoStyle_One-Shot_Facial_Expression_Editing_Using_Continuous_Emotion_Parameters_WACV_2024_paper.pdf), https://arxiv.org/pdf/2103.15792
        ![[Pasted image 20250915084632.png]]
- **Chỉ số đánh giá**:
    - **Acc/MAE** của classifier/regressor (expr, valence, arousal) trên output;
    - **Identity cosine** (ArcFace), **LPIPS**, **FID** 
    - **Landmark distance** (NME) giữa target và output;


---

## 6) Điểm mới

1. **Diffusion thuần trong miền wavelet cho emotion editing** (không GAN), **dự đoán nhiễu trên sub-band concat** với **khối tần số** (down/up/bottleneck/residual) — kế thừa cơ chế wavelet của paper gốc nhưng chuyển sang **DDPM**.

2. **CFG tách biệt low/high** + **tối ưu loss theo sub-band** (trọng số lớn cho LH/HL/HH) để kiểm soát **mức độ chi tiết** biểu cảm.
    
3. **Kết hợp điều kiện đa mô thức** (prompt + landmarks + expression + valence/arousal) trong **miền wavelet**, đặc biệt **landmarks** như cho biến đổi chính xác vùng (miệng, mắt, lông mày).