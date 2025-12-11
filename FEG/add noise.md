Dưới đây là 3 chiến lược từ “khóa hẳn LL” đến “cho LL thay đổi tối thiểu” để bạn chọn:

---

## Phương án A — **Khóa LL, chỉ khuếch tán H = (LH, HL, HH)**

- **Dòng dữ liệu huấn luyện (DDPM trong wavelet):**
    
    1. DWT ảnh → (LL,H)(LL, H)(LL,H); concat theo kênh (RGB → 12 kênh) là **đầu vào miền wavelet**.
        
        Wavelet Diffusion Models are fa…
        
    2. **Chỉ thêm nhiễu lên HHH**:
        
        Ht=αˉtH0+1−αˉt εH,εH ⁣∼ ⁣N(0,I)H_t=\sqrt{\bar\alpha_t}H_0+\sqrt{1-\bar\alpha_t}\,\varepsilon_H,\quad \varepsilon_H\!\sim\!\mathcal N(0,I)Ht​=αˉt​​H0​+1−αˉt​​εH​,εH​∼N(0,I)
        
        còn **LL giữ nguyên** làm **điều kiện (conditioning)** cho mạng.
        
    3. UNet tần số nhận [LL, Ht, t, cond][LL,\ H_t,\ t,\ \text{cond}][LL, Ht​, t, cond] và **dự đoán nhiễu ε^H\hat\varepsilon_Hε^H​**.
        
    4. Suy luận: dùng **LLsrc_\text{src}src​** và **H** đã được khử nhiễu để **IWT** ra ảnh.
        
        Wavelet Diffusion Models are fa…
        
- **Ưu**: giữ **danh tính/nền** cực tốt (LL không đổi); chỉnh được **chi tiết cảm xúc** (viền môi, lông mày, nếp nhăn).
    
- **Nhược**: **khó thay đổi hình học lớn** (há miệng rộng, nâng hạ khối cơ mặt) vì LL bị “đóng băng”.
    

> Mẹo: dùng **mask ROI** (mặt/miệng/mắt) để **chỉ khuếch tán H** trong vùng cần đổi cảm xúc; ngoài ROI giữ **Hsrc_\text{src}src​** → nền/danh tính an toàn.

---

## Phương án B — **LL “mềm”: cho phép ΔLL\Delta LLΔLL nhỏ trong ROI**

Giữ LL phần lớn, nhưng cho **một residual rất nhỏ** trong vùng mặt để “nắn hình” nhẹ:

LLnew=LLsrc+α⋅M⋅ΔLL,α∈[0,0.3],LL_{\text{new}} = LL_{\text{src}} + \alpha\cdot M\cdot \Delta LL,\quad \alpha\in[0,0.3],LLnew​=LLsrc​+α⋅M⋅ΔLL,α∈[0,0.3], Hnew=Hsrc⋅(1−M)+(Hsrc+ΔH)⋅M.H_{\text{new}} = H_{\text{src}}\cdot(1-M) + (H_{\text{src}}+\Delta H)\cdot M.Hnew​=Hsrc​⋅(1−M)+(Hsrc​+ΔH)⋅M.

Trong đó MMM là mask ROI đã **downsample** về cùng kích thước sub-band; ΔH\Delta HΔH do mạng dự đoán (từ diffusion trên HHH), ΔLL\Delta LLΔLL có thể do một **nhánh nông** dự đoán.

- **Ưu**: vẫn **giữ danh tính**, nhưng đủ **linh hoạt** để thay đổi **hình học vừa phải** (mở miệng, nhíu mày nhẹ).
    
- **Loss gợi ý**:
    
    - **Wavelet per-subband**: λH>λLL\lambda_H > \lambda_{LL}λH​>λLL​ để ưu tiên chi tiết cảm xúc.
        
    - **Identity + perceptual** sau **IWT**.
        
    - **Consistency** LL–H: L1L_1L1​ hoặc Charbonnier trên **gradient ảnh** để giảm “halo” khi IWT ghép sub-band.
        
- **Noise**: **Dual-schedule**: cho **H** nhiều nhiễu ở đầu (dễ “bẻ” chi tiết) rồi giảm dần; **LL** nhiễu rất nhỏ (hoặc không nhiễu) để ổn định hình học.
    

---

## Phương án C — **Warp LL có điều khiển + chỉnh H**

Giữ LL về mặt cường độ, nhưng **dự đoán trường dịch chuyển** w=(u,v)\mathbf{w}=(u,v)w=(u,v) trong ROI để **warp(LLsrc_\text{src}src​)** (từ landmarks/prompt). Sau đó **khuếch tán H** như A/B và **IWT**:

LLnew=Warp(LLsrc,w),Hnew=Hsrc+ΔH (trong ROI).LL_{\text{new}} = \text{Warp}(LL_{\text{src}}, \mathbf{w}),\qquad H_{\text{new}} = H_{\text{src}} + \Delta H \text{ (trong ROI)}.LLnew​=Warp(LLsrc​,w),Hnew​=Hsrc​+ΔH (trong ROI).

- **Ưu**: làm được **biến dạng lớn** (há miệng rõ) mà vẫn giữ tone sáng–tối của nguồn; **H** bù chi tiết răng/môi/viền.
    
- **Nhược**: cần **ổn định warp** (flow loss, smoothness) và đồng bộ với ΔH\Delta HΔH để tránh “lệch bậc”.
    

---

## Lưu ý quan trọng khi “giữ LL, sửa H”

1. **Nhất quán sub-band khi IWT**: Nếu **LL** và **H** mâu thuẫn (ví dụ LL không mở miệng nhưng H tạo răng/môi), ảnh sau IWT có thể “rung/halo”. Giải pháp:
    
    - Cho **ΔLL\Delta LLΔLL nhỏ** trong ROI (B), **hoặc** warp LL (C).
        
    - Thêm **loss nhất quán** giữa ∇\nabla∇ ảnh sau IWT và biên từ landmarks/ROI.
        
2. **Kênh điều kiện**: giữ cơ chế **freq-aware** của paper (down/up/bottleneck/residual) — đặc biệt **upsampling bằng IWT** để ghép **H đã sửa** với **LL** hiệu quả và rẻ.
    
    Wavelet Diffusion Models are fa…
    
3. **Huấn luyện không cần cặp ảnh cùng ID khác cảm xúc**: bạn có thể dựa vào **classifier/regressor** (expression, valence/arousal) + **identity** + **landmark alignment** làm mục tiêu; **wavelet loss theo sub-band** giúp mạng “cấy” đúng chi tiết vào H.
    
4. **Chọn wavelet**: Haar nhanh & trực chuẩn (dễ phân tích); bior4.4 mượt biên hơn (ít rung mép), đổi kernel DWT/IWT là xong.
    
    Wavelet Diffusion Models are fa…