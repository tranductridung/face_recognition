import os
import cv2
import face_recognition
import numpy as np

def is_face_clear(rgb_frame, face_locations):
    """
    Kiểm tra xem khuôn mặt có rõ ràng và đầy đủ không.
    """
    if not face_locations:
        return False

    # Lấy tọa độ khuôn mặt đầu tiên (nếu có nhiều khuôn mặt, chỉ kiểm tra cái đầu tiên)
    top, right, bottom, left = face_locations[0]
    face_area = rgb_frame[top:bottom, left:right]

    # Kiểm tra điều kiện cơ bản: ánh sáng và độ sắc nét
    brightness = np.mean(face_area)  # Độ sáng trung bình
    if brightness < 50:  # Ngưỡng kiểm tra thiếu sáng
        print("Ảnh bị thiếu sáng. Vui lòng điều chỉnh ánh sáng.")
        return False

    # Đảm bảo nhận diện đầy đủ các đặc điểm khuôn mặt
    face_landmarks = face_recognition.face_landmarks(face_area)
    if not face_landmarks or not all(key in face_landmarks[0] for key in ["left_eye", "right_eye", "nose_tip", "top_lip", "bottom_lip"]):
        print("Khuôn mặt không rõ ràng hoặc không đầy đủ. Vui lòng điều chỉnh.")
        return False

    return True

def register_face(name):
    # Tạo thư mục lưu khuôn mặt nếu chưa tồn tại
    os.makedirs("known_faces", exist_ok=True)

    # Khởi tạo webcam
    video_capture = cv2.VideoCapture(0)
    print("Chương trình sẽ chụp ảnh liên tục cho đến khi đủ 5 ảnh.")

    count = 0
    while count < 5:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Phát hiện khuôn mặt trong khung hình
        # rgb_frame = frame[:, :, ::-1]  # Chuyển đổi BGR sang RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        face_locations = face_recognition.face_locations(rgb_frame)

        # Kiểm tra xem ảnh có đạt chất lượng không
        if is_face_clear(rgb_frame, face_locations):
            file_path = os.path.join("known_faces", f"{name}_{count}.jpg")
            cv2.imwrite(file_path, frame)
            print(f"Đã lưu ảnh: {file_path}")
            count += 1
        else:
            print("Ảnh không đạt yêu cầu. Thử chụp lại.")

        # Hiển thị khung hình
        cv2.imshow("Đăng ký khuôn mặt", frame)

        # Nhấn 'q' để thoát sớm nếu cần
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    name = input("Nhập tên nhân viên: ")
    register_face(name)
    print("Quá trình chụp ảnh hoàn tất.")
