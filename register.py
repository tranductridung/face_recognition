import cv2
import os
import face_recognition
import numpy as np
from datetime import datetime
import time
import sys

# Kiểm tra nếu tên người dùng được truyền vào từ command line
if len(sys.argv) != 2:
    print("Vui lòng nhập tên người dùng!")
    sys.exit(1)

user_name = sys.argv[1]  # Lấy tên người dùng từ tham số dòng lệnh

# Tạo thư mục lưu ảnh khuôn mặt nếu chưa tồn tại
known_faces_dir = 'known_faces'
if not os.path.exists(known_faces_dir):
    os.makedirs(known_faces_dir)

# Khởi tạo video capture
video_capture = cv2.VideoCapture(0)

# Khởi tạo biến lưu các ảnh đã chụp
face_count = 0
image_list = []

# Hàm kiểm tra độ sắc nét của ảnh
def is_image_clear(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var > 100  # Nếu biến đổi Laplacian > 100 thì ảnh sắc nét

# Hàm kiểm tra độ sáng của ảnh
def is_image_bright(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    brightness = np.mean(hsv[:, :, 2])  # Lấy kênh độ sáng (Value) trong HSV
    return brightness > 100  # Nếu độ sáng > 100 thì đủ sáng

# Bắt đầu hiển thị webcam
print("Đang bật camera...")

# Bộ đếm 3 giây (hiển thị trực tiếp trên video feed)
font = cv2.FONT_HERSHEY_SIMPLEX
for i in range(3, 0, -1):
    ret, frame = video_capture.read()
    cv2.putText(frame, f"Chup trong: {i}", (250, 250), font, 2, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.imshow('Video', frame)
    time.sleep(1)

# Sau 3 giây, bắt đầu chụp ảnh
while face_count < 5:
    ret, frame = video_capture.read()

    # Chuyển đổi hình ảnh sang định dạng RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Tìm các khuôn mặt trong hình ảnh
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Kiểm tra xem có khuôn mặt nào không
    if len(face_locations) > 0:
        # Kiểm tra chất lượng ảnh
        if not is_image_clear(frame):
            cv2.putText(frame, "Anh mo hoac nhoe, vui long chup lai!", (50, 50), font, 1.0, (0, 0, 255), 2, cv2.LINE_AA)
        elif not is_image_bright(frame):
            cv2.putText(frame, "Anh thieu sang, vui long chup lai!", (50, 50), font, 1.0, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            # Vẽ khung quanh các khuôn mặt phát hiện
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Lưu ảnh nếu có khuôn mặt
            image_path = os.path.join(known_faces_dir, f'{user_name}_{face_count + 1}.jpg')
            cv2.imwrite(image_path, frame)  # Lưu ảnh vào thư mục 'known_faces'
            image_list.append(image_path)
            face_count += 1
            print(f"Đã lưu ảnh {face_count} cho {user_name}.")
    else:
        # Nếu không phát hiện khuôn mặt
        cv2.putText(frame, "Khong phat hien khuon mat, vui long dieu chinh vi tri va chup lai!", (50, 50), font, 1.0, (0, 0, 255), 2, cv2.LINE_AA)

    # Hiển thị khung hình cho người dùng
    cv2.imshow('Video', frame)

    # Chờ 1ms và kiểm tra xem người dùng có nhấn 'q' để thoát không
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Đóng webcam và cửa sổ OpenCV
video_capture.release()
cv2.destroyAllWindows()

# In thông tin các ảnh đã lưu
print(f"Tất cả ảnh đã lưu: {image_list}")
print(f"Đã đăng ký thành công người dùng: {user_name} với 5 ảnh.")
