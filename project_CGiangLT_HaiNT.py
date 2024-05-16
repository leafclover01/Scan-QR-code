import cv2
import matplotlib.pyplot as plt 
from tkinter import Tk, filedialog 
from pyzbar.pyzbar import decode 
import numpy as np

def tien_xu_ly_anh(image, clip_limit=5.0, tile_grid_size=(8, 8)):
    # Tính toán thông tin về độ sáng của ảnh
    hist, _ = np.histogram(image.flatten(), 256, [0, 256])
    total_pixels = image.shape[0] * image.shape[1]

    # Tính toán tổng của mỗi giá trị pixel nhân với tần suất và chia cho tổng số pixel
    sum_brightness = np.sum(np.arange(256) * hist)
    do_sang_trung_binh = sum_brightness / total_pixels

    # Tìm giá trị tối nhất và sáng nhất của ảnh từ histogram
    min_brightness = np.min(np.where(hist > 0))
    max_brightness = np.max(np.where(hist > 0))

    alpha = 1
    beta = 0
    if min_brightness < 128:
        if max_brightness < 128:
            alpha = 128 / (max_brightness - min_brightness)
            beta = 128 * (255 - max_brightness) / (max_brightness - 128)
        else:
            grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            do_sang_trung_binh = int(cv2.mean(grayscale_image)[0])
            lam_min_anh = cv2.GaussianBlur(grayscale_image, (1, 1), 0)

            do_tuong_phan = cv2.convertScaleAbs(lam_min_anh, alpha=1.5, beta=0)
            print("Mức độ ánh sáng trung bình của ảnh được nhận : ", do_sang_trung_binh)
            if 0 <= do_sang_trung_binh <= 80:
                do_sang_alpha = 2
                do_sang_beta = 10
                hinh_anh_da_xu_ly = cv2.convertScaleAbs(do_tuong_phan, alpha=do_sang_alpha, beta=do_sang_beta)
                return hinh_anh_da_xu_ly
            elif 81 <= do_sang_trung_binh <= 127:
                 alpha = (255 - max_brightness) / 128
                 beta = max_brightness
            elif 128 <= do_sang_trung_binh <= 159:
                do_sang_alpha = 0.5
                do_sang_beta = 10
                hinh_anh_da_xu_ly = cv2.convertScaleAbs(do_tuong_phan, alpha=do_sang_alpha, beta=do_sang_beta)
                return hinh_anh_da_xu_ly
            elif 160 <= do_sang_trung_binh <= 179:
                alpha = 128 / (max_brightness - min_brightness)
                beta = - min_brightness * (128 / (max_brightness - min_brightness))
            elif 180 <= do_sang_trung_binh <= 200:
                do_sang_alpha = 0.5
                do_sang_beta = 5
                hinh_anh_da_xu_ly = cv2.convertScaleAbs(do_tuong_phan, alpha=do_sang_alpha, beta=do_sang_beta)
                return hinh_anh_da_xu_ly
            else:
                do_sang_alpha = 0.5
                do_sang_beta = -1
                hinh_anh_da_xu_ly = cv2.convertScaleAbs(do_tuong_phan, alpha=do_sang_alpha, beta=do_sang_beta)
                return hinh_anh_da_xu_ly
    elif min_brightness >= 128:
        if max_brightness >= 128:
            alpha = 128 / (max_brightness - min_brightness)
            beta = 128 * (255 - max_brightness) / (max_brightness - 128)
        else:
            alpha = (255 - max_brightness) / 128
            beta = max_brightness

    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    # Chuyển đổi sang không gian màu LAB để tăng cường độ sáng (L channel)
    lab_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab_image)

    # Tạo bộ cân bằng tương phản giới hạn hàm
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)

    # Áp dụng cân bằng tương phản giới hạn hàm vào kênh L
    enhanced_l = clahe.apply(l)

    updated_lab_image = cv2.merge((enhanced_l, a, b))
    enhanced_image = cv2.cvtColor(updated_lab_image, cv2.COLOR_LAB2BGR)

    # Làm mịn hình ảnh để giảm nhiễu và tăng cường rõ nét
    blurred_image = cv2.GaussianBlur(enhanced_image, (5, 5), 0)

    return blurred_image

def nhan_dien_ma_qr(image):

    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    qr_codes = decode(image)
    qr_code_ketqua = []
    duong_vien_quanh_qrcode = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    for qr_code in qr_codes:
        x, y, w, h = qr_code.rect
        cv2.rectangle(duong_vien_quanh_qrcode, (x, y), (x + w, y + h), (0, 255, 0), 2)
        qr_code_ketqua.append((qr_code.data.decode('utf-8')))
        cv2.putText(duong_vien_quanh_qrcode, qr_code.data.decode('utf-8'), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    return qr_code_ketqua, duong_vien_quanh_qrcode

# Hiển thị chọn tệp ảnh từ máy tính
def choose_image():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

image_path = choose_image()

image = cv2.imread(image_path)

hinh_anh_da_xu_ly = tien_xu_ly_anh(image)

qr_code_ketqua, duong_vien_quanh_qrcode = nhan_dien_ma_qr(hinh_anh_da_xu_ly)

plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Ảnh ban đầu: ')
plt.axis('off') 
plt.show()

plt.imshow(cv2.cvtColor(hinh_anh_da_xu_ly, cv2.COLOR_BGR2RGB))
plt.title('Ảnh sau khi áp dụng tiền xử lí:')        
plt.axis('off')
plt.show()

plt.imshow(cv2.cvtColor(duong_vien_quanh_qrcode, cv2.COLOR_BGR2RGB))
plt.title('Phát hiện mã QR Code:')
plt.axis('off')
plt.show()

if qr_code_ketqua:
    for i, content in enumerate(qr_code_ketqua):
        print(f"Nội Dung QR Code {i+1}: {content}")
    
if qr_code_ketqua:
    print(f"Đã phát hiện {len(qr_code_ketqua)} mã QR trong ảnh!")
else:
    print("Không tìm thấy mã QR nào trong ảnh!")
    
    
