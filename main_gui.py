# import tkinter as tk
# from tkinter import simpledialog, filedialog
# import subprocess
# import os

# # Hàm để chạy một file python thông qua subprocess
# def run_python_script(script_path, user_name):
#     subprocess.run([r'C:\Users\HP\Desktop\face_recognition\venv\Scripts\python.exe', script_path, user_name])

# # Hàm xử lý khi nhấn nút "Chấm công"
# def mark_attendance():
#     run_python_script('recognize.py', '')

# # Hàm xử lý khi nhấn nút "Đăng ký"
# def register():
#     root.withdraw()  # Ẩn cửa sổ chính
#     open_register_window()

# # Hàm để mở cửa sổ đăng ký
# def open_register_window():
#     register_window = tk.Toplevel(root)
#     register_window.title("Đăng ký khuôn mặt")

#     # Nút chụp ảnh
#     capture_button = tk.Button(register_window, text="Chụp ảnh", command=capture_image)
#     capture_button.pack(pady=10)

#     # Nút tải ảnh
#     upload_button = tk.Button(register_window, text="Tải ảnh", command=upload_image)
#     upload_button.pack(pady=10)

#     # Nút quay lại
#     back_button = tk.Button(register_window, text="Quay lại", command=lambda: go_back(register_window))
#     back_button.pack(pady=10)

#     # Nút thoát
#     exit_button = tk.Button(register_window, text="Thoát", command=exit_program)
#     exit_button.pack(pady=10)

# # Hàm xử lý khi nhấn nút "Chụp ảnh"
# def capture_image():
#     name = simpledialog.askstring("Nhập tên", "Vui lòng nhập tên:")
#     if name:
#         # Chạy file register.py với tên người dùng
#         run_python_script('register.py', name)
# import shutil
# # Hàm xử lý khi nhấn nút "Tải ảnh"
# def upload_image():
#     name = simpledialog.askstring("Nhập tên", "Vui lòng nhập tên:")
#     if name:
#         # Kiểm tra xem thư mục known_faces đã tồn tại chưa, nếu chưa thì tạo nó
#         known_faces_dir = 'C:/Users/HP/Desktop/face_recognition/known_faces'
#         if not os.path.exists(known_faces_dir):
#             os.makedirs(known_faces_dir)

#         file_path = filedialog.askopenfilename(title="Chọn ảnh")
#         if file_path:
#             # Lưu ảnh với tên đã nhập
#             new_image_path = os.path.join(known_faces_dir, f'{name}.jpg')
#             new_image_path = os.path.normpath(new_image_path)  # Chuẩn hóa đường dẫn
#             with open(file_path, 'rb') as file:
#                 with open(new_image_path, 'wb') as new_file:
#                     new_file.write(file.read())
#             print(f"Ảnh đã được lưu tại: {new_image_path}")

# # Hàm quay lại cửa sổ chính
# def go_back(register_window):
#     register_window.destroy()  # Đóng cửa sổ đăng ký
#     root.deiconify()  # Hiện lại cửa sổ chính

# # Hàm xử lý khi nhấn nút "Thoát"
# def exit_program():
#     root.quit()  # Thoát chương trình

# # Tạo cửa sổ chính
# root = tk.Tk()
# root.title("Hệ thống chấm công")

# # Nút chấm công
# attendance_button = tk.Button(root, text="Chấm công", command=mark_attendance)
# attendance_button.pack(pady=10)

# # Nút đăng ký
# register_button = tk.Button(root, text="Đăng ký", command=register)
# register_button.pack(pady=10)

# # Nút thoát
# exit_button = tk.Button(root, text="Thoát", command=exit_program)
# exit_button.pack(pady=10)

# # Bắt đầu giao diện
# root.mainloop()


import tkinter as tk
from tkinter import simpledialog, filedialog
import subprocess
import os

# Hàm để chạy một file python thông qua subprocess
def run_python_script(script_path, user_name):
    subprocess.run([r'C:\Users\HP\Desktop\face_recognition\venv\Scripts\python.exe', script_path, user_name])

# Hàm xử lý khi nhấn nút "Chấm công"
def mark_attendance():
    run_python_script('recognize.py', '')

# Hàm xử lý khi nhấn nút "Đăng ký"
def register():
    root.withdraw()  # Ẩn cửa sổ chính
    open_register_window()

# Hàm để mở cửa sổ đăng ký
def open_register_window():
    register_window = tk.Toplevel(root)
    register_window.title("Đăng ký khuôn mặt")
    register_window.geometry("400x300")
    register_window.configure(bg="#f0f0f0")

    # Nút chụp ảnh
    capture_button = tk.Button(register_window, text="Chụp ảnh", command=capture_image, width=20, height=2, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
    capture_button.pack(pady=15)

    # Nút tải ảnh
    upload_button = tk.Button(register_window, text="Tải ảnh", command=upload_image, width=20, height=2, bg="#2196F3", fg="white", font=("Arial", 12, "bold"))
    upload_button.pack(pady=15)

    # Nút quay lại
    back_button = tk.Button(register_window, text="Quay lại", command=lambda: go_back(register_window), width=20, height=2, bg="#f44336", fg="white", font=("Arial", 12, "bold"))
    back_button.pack(pady=15)

    # Nút thoát
    exit_button = tk.Button(register_window, text="Thoát", command=exit_program, width=20, height=2, bg="#9E9E9E", fg="white", font=("Arial", 12, "bold"))
    exit_button.pack(pady=15)

# Hàm xử lý khi nhấn nút "Chụp ảnh"
def capture_image():
    name = simpledialog.askstring("Nhập tên", "Vui lòng nhập tên:")
    if name:
        # Chạy file register.py với tên người dùng
        run_python_script('register.py', name)

import shutil
# Hàm xử lý khi nhấn nút "Tải ảnh"
def upload_image():
    name = simpledialog.askstring("Nhập tên", "Vui lòng nhập tên:")
    if name:
        # Kiểm tra xem thư mục known_faces đã tồn tại chưa, nếu chưa thì tạo nó
        known_faces_dir = 'C:/Users/HP/Desktop/face_recognition/known_faces'
        if not os.path.exists(known_faces_dir):
            os.makedirs(known_faces_dir)

        file_path = filedialog.askopenfilename(title="Chọn ảnh")
        if file_path:
            # Lưu ảnh với tên đã nhập
            new_image_path = os.path.join(known_faces_dir, f'{name}.jpg')
            new_image_path = os.path.normpath(new_image_path)  # Chuẩn hóa đường dẫn
            with open(file_path, 'rb') as file:
                with open(new_image_path, 'wb') as new_file:
                    new_file.write(file.read())
            print(f"Ảnh đã được lưu tại: {new_image_path}")

# Hàm quay lại cửa sổ chính
def go_back(register_window):
    register_window.destroy()  # Đóng cửa sổ đăng ký
    root.deiconify()  # Hiện lại cửa sổ chính

# Hàm xử lý khi nhấn nút "Thoát"
def exit_program():
    root.quit()  # Thoát chương trình

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Hệ thống chấm công")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

# Thêm logo hoặc hình ảnh nếu cần
# logo = tk.PhotoImage(file="path/to/logo.png")
# root.iconphoto(True, logo)

# Nút chấm công
attendance_button = tk.Button(root, text="Chấm công", command=mark_attendance, width=20, height=2, bg="#4CAF50", fg="white", font=("Arial", 14, "bold"))
attendance_button.pack(pady=20)

# Nút đăng ký
register_button = tk.Button(root, text="Đăng ký", command=register, width=20, height=2, bg="#2196F3", fg="white", font=("Arial", 14, "bold"))
register_button.pack(pady=20)

# Nút thoát
exit_button = tk.Button(root, text="Thoát", command=exit_program, width=20, height=2, bg="#f44336", fg="white", font=("Arial", 14, "bold"))
exit_button.pack(pady=20)

# Bắt đầu giao diện
root.mainloop()
