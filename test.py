from datetime import datetime
import face_recognition
import cv2
import numpy as np
import os
import csv

# Khởi tạo MediaPipe và face_recognition
video_capture = cv2.VideoCapture(0)

# Khởi tạo thư mục chứa ảnh đã đăng ký
known_faces_dir = 'known_faces'
known_face_encodings = []
known_face_names = []
attendance_status = {}
isRecognize = False

# Tải ảnh khuôn mặt đã đăng ký và mã hóa chúng
for filename in os.listdir(known_faces_dir):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(known_faces_dir, filename)
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)
        if encoding:
            known_face_encodings.append(encoding[0])
            known_face_names.append(filename.split('.')[0])  # Lấy tên từ tên tệp

# Đọc thông tin từ file attendance.csv
def read_attendance_file():
    attendance_data = {}
    try:
        with open('attendance.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                name, date, status = row
                if name not in attendance_data:
                    attendance_data[name] = {}
                attendance_data[name][date] = status
    except FileNotFoundError:
        pass  # Nếu file chưa tồn tại, trả về dictionary rỗng
    return attendance_data

attendance_status = read_attendance_file()

# Hàm để lưu thông tin attendance vào file CSV
def save_attendance(name, status):
    today_date = datetime.now().strftime('%Y-%m-%d')
    with open('attendance.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, today_date, status])
        print(f"{name} đã {status} vào {today_date}")

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
frame_count = 0  # Biến đếm số khung hình

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Tăng biến đếm số khung hình
    frame_count += 1

    # Chỉ xử lý mỗi 5 khung hình
    if frame_count % 5 != 0:
        continue

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")  # Sử dụng model "hog" để nhanh hơn
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # So khớp với khuôn mặt đã đăng ký
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # So sánh khoảng cách khuôn mặt thay vì so khớp trực tiếp
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        if name != "Unknown":
            today_date = datetime.now().strftime('%Y-%m-%d')

            if name not in attendance_status:
                attendance_status[name] = {}

            # Kiểm tra nếu ngày hôm nay đã có trạng thái check-in hoặc check-out
            if today_date not in attendance_status[name]:
                message = f"Xác nhận checkin cho {name} (Nhấn 'o' để xác nhận)"
            else:
                # Nếu lần gần nhất là checkout, thì lưu checkin
                if attendance_status[name][today_date] == 'checkout':
                    message = f"Xác nhận checkin cho {name} (Nhấn 'o' để xác nhận)"
                else:
                    message = f"Xác nhận checkout cho {name} (Nhấn 'o' để xác nhận)"
                    
            cv2.putText(frame, message, (10, 30), font, 1.0, (0, 255, 0), 2)
            isRecognize = True
    
    # Display the resulting image
    cv2.imshow('Video', frame)

    # Chờ người dùng nhấn 'o' để xác nhận
    if isRecognize:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('o'):  # Người dùng nhấn 'o' để xác nhận
            today_date = datetime.now().strftime('%Y-%m-%d')
            for name in face_names:
                if name != "Unknown":
                    if today_date not in attendance_status[name]:
                        # Nếu người dùng chưa check-in, lưu thông tin với status là checkin
                        save_attendance(name, 'checkin')
                        attendance_status[name][today_date] = 'checkin'
                    elif attendance_status[name][today_date] == 'checkin':
                        # Nếu người dùng đã check-in, lưu thông tin với status là checkout
                        save_attendance(name, 'checkout')
                        attendance_status[name][today_date] = 'checkout'
                    elif attendance_status[name][today_date] == 'checkout':
                        # Nếu lần gần nhất là checkout, lưu lại checkin
                        save_attendance(name, 'checkin')
                        attendance_status[name][today_date] = 'checkin'
            isRecognize = False
            # Tắt webcam khi nhấn 'o'
            video_capture.release()
            cv2.destroyAllWindows()
            break

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
