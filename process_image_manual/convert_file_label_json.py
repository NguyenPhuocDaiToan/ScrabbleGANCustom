import json

# Đường dẫn tới file JSON và file văn bản đầu ra
json_file = "E:\Image_Processing\ProcessIAM\IAM\labels.json"
txt_file = "vietnamese.txt"

# Đọc dữ liệu từ file JSON
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Mở file văn bản để ghi dữ liệu
with open(txt_file, "w", encoding="utf-8") as f:
    # Lặp qua từng cặp key-value trong dữ liệu JSON
    for filename, label in data.items():
        # Thay thế khoảng trắng trong label bằng dấu |
        label = label.replace(" ", "|")
        # Ghi dữ liệu vào file văn bản
        f.write(f'{filename} {label}\n')
