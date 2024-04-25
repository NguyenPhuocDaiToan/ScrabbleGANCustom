import os

def merge_images_and_labels(image_dir, output_dir):
    # Tạo thư mục output nếu nó không tồn tại
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Tạo file txt để ghi tên ảnh và label
    with open(
        os.path.join("E:\Image_Processing\ProcessIAM\data\labels", "vnondb_lines.txt"),
        "w",
        encoding="utf-8",
    ) as output_file:
        # Lặp qua tất cả các file trong thư mục ảnh
        for filename in os.listdir(image_dir):
            # Kiểm tra nếu là file ảnh
            if filename.endswith(".png") or filename.endswith(".jpg"):
                image_path = os.path.join(image_dir, filename)
                label_path = os.path.join(
                    image_dir, filename[:-4] + ".txt"
                )  # Tên file label tương ứng

                # Kiểm tra nếu file label tồn tại
                if os.path.exists(label_path):
                    # Copy file ảnh vào thư mục output
                    os.rename(image_path, os.path.join(output_dir, filename))

                    # Ghi tên ảnh và label vào file txt
                    with open(label_path, "r", encoding="utf-8") as label_file:
                        label = label_file.read()
                        label = label.replace(" ", "|")
                        output_file.write(f"{filename} {label} \n")


# Sử dụng hàm merge_images_and_labels
print('start running')
merge_images_and_labels(
    "E:\Image_Processing\ProcessIAM\VNOnDB_Line",
    "E:\Image_Processing\ProcessIAM\data\dataset\\vnondb_lines",
)
print('end running')