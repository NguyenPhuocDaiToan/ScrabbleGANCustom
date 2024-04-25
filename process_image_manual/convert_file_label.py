output_file = "iam_lines.txt"

with open("lines.txt", "r", encoding="utf-8") as f, open(
    output_file, "w", encoding="utf-8"
) as out_f:
    for line in f:
        # Tách các từ trong dòng
        words = line.strip().split()

        # Lấy chuỗi a01-000u-00-00 từ đầu tiên
        first_word = words[0]

        # Lấy ký tự cuối cùng trong dòng
        last_character = words[-1]

        # Ghi thông tin vào file mới
        out_f.write(f"{first_word} {last_character}\n")
