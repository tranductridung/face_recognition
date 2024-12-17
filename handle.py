import os
import pickle
import face_recognition

def process_images_and_save_features(folder="known_faces"):
    """
    Xử lý ảnh trong thư mục và lưu đặc trưng khuôn mặt vào file `face_features.pkl`.
    """
    face_encodings = {}
    for file in os.listdir(folder):
        if file.endswith(".jpg"):
            name = "_".join(file.split("_")[:-1])  # Lấy tên từ file (loại bỏ số thứ tự)
            image_path = os.path.join(folder, file)
            image = face_recognition.load_image_file(image_path)
            
            # Trích xuất đặc trưng khuôn mặt
            encoding = face_recognition.face_encodings(image)
            if encoding:  # Chỉ lưu nếu phát hiện khuôn mặt
                face_encodings[name] = encoding[0]
    
    # Lưu các đặc trưng khuôn mặt vào file
    with open("face_features.pkl", "wb") as f:
        pickle.dump(face_encodings, f)
    print(f"Đã lưu đặc trưng của {len(face_encodings)} khuôn mặt vào cơ sở dữ liệu.")

if __name__ == "__main__":
    process_images_and_save_features()
