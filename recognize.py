import os
import cv2
import face_recognition
import numpy as np
from datetime import datetime

def load_known_faces():

    known_faces = []
    known_names = []

    # Lấy tất cả các ảnh đã đăng ký trong thư mục 'known_faces'
    for filename in os.listdir("known_faces"):
        if filename.endswith(".jpg"):
            image_path = os.path.join("known_faces", filename)
            image = cv2.imread(image_path)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Chuyển đổi từ BGR sang RGB
            face_encoding = face_recognition.face_encodings(rgb_image)

            if face_encoding:
                known_faces.append(face_encoding[0])
                known_names.append(filename.split('_')[0])  # Lấy tên từ tên file (giả sử tên ở đầu file)
    
    return known_faces, known_names

def get_last_attendance(name):
    attendance_file = "attendances/attendance.csv"
    
    if not os.path.exists(attendance_file):
        return None

    with open(attendance_file, "r") as f:
        lines = f.readlines()

    # Tìm chấm công gần nhất của nhân viên
    for line in reversed(lines):
        fields = line.strip().split(',')
        if fields[0] == name:
            return fields[3]  # 'IN' hoặc 'OUT'
    
    return None

def mark_attendance(name, status):
    date_string = datetime.now().strftime("%Y-%m-%d")
    time_string = datetime.now().strftime("%H:%M:%S")

    # Đọc file chấm công để kiểm tra tình trạng đã chấm công vào hay ra
    attendance_file = "attendances/attendance.csv"
    if not os.path.exists(attendance_file):
        os.makedirs("attendances", exist_ok=True)
        open(attendance_file, 'w').close()

    # Kiểm tra chấm công gần nhất
    last_attendance = get_last_attendance(name)

    # Kiểm tra lựa chọn của người dùng với trạng thái chấm công gần nhất
    if last_attendance == status:
        print(f"Ban da thuc hien cham cong {status}, khong the cham cong {status} tiep.")
        return

    # Ghi nhận chấm công mới
    with open(attendance_file, "a") as f:
        f.write(f"{name},{date_string},{time_string},{status}\n")
    
    print(f"Cham cong {status} cho {name} luc {time_string} ngay {date_string}.")

def recognize_and_mark_attendance(known_faces, known_names):
    video_capture = cv2.VideoCapture(0)
    print("Dang nhan dien khuon mat. Nhan 'q' de thoat...")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Chuyển đổi hình ảnh sang định dạng RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Chuyển đổi từ BGR sang RGB

        # Phát hiện các khuôn mặt trong khung hình
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # So sánh với các khuôn mặt đã đăng ký
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            name = "Khong nhan dien duoc"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]

                # Vẽ hộp bao quanh khuôn mặt và hiển thị tên nhân viên
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                # Lựa chọn chấm công
                cv2.putText(frame, "Nhan '1' de cham cong vao, '2' de cham cong ra", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                cv2.imshow("Nhan dien khuon mat va cham cong", frame)

                # Lựa chọn từ người dùng
                key = cv2.waitKey(1) & 0xFF
                if key == ord('1'):
                    mark_attendance(name, status='IN')
                elif key == ord('2'):
                    mark_attendance(name, status='OUT')

        # Thoát nếu nhấn 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Tải các khuôn mặt đã đăng ký và tạo cơ sở dữ liệu
    known_faces, known_names = load_known_faces()

    # Nhận diện và chấm công
    recognize_and_mark_attendance(known_faces, known_names)
