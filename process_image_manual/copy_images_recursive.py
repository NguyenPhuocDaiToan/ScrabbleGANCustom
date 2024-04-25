import os
import shutil


def copy_images_recursive(src_dir):
    # Lặp qua tất cả các thư mục và file trong thư mục nguồn
    for item in os.listdir(src_dir):
        # Đường dẫn đầy đủ của item (file hoặc thư mục)
        item_path = os.path.join(src_dir, item)

        # Kiểm tra xem item có phải là thư mục không
        if os.path.isdir(item_path):
            # Nếu là thư mục, đệ quy vào thư mục đó
            copy_images_recursive(item_path)
        # Kiểm tra xem item có phải là file ảnh không
        elif item.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            # Nếu là file ảnh, sao chép vào thư mục đích
            shutil.copy(
                item_path,
                os.path.join(
                    "E:\Image_Processing\ProcessIAM\dataset\iam_lines", item
                ),
            )


# Đường dẫn đến thư mục gốc chứa tất cả các thư mục con
root_dir = "E:\Image_Processing\ProcessIAM\lines"

# Sao chép tất cả các ảnh từ thư mục gốc đến thư mục đầu ra
print("start running...")
copy_images_recursive(root_dir)
print("done")
