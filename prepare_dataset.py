import sys

sys.path.extend([".."])
import numpy as np
import pickle as pkl
import cv2


def read_image(img_path, label_len, img_h=32, char_w=16):
    valid_img = True
    img = cv2.imread(img_path, 0)
    try:
        curr_h, curr_w = img.shape
        modified_w = int(curr_w * (img_h / curr_h))

        # Remove outliers
        if ((modified_w / label_len) < (char_w / 3)) | (
            (modified_w / label_len) > (3 * char_w)
        ):
            valid_img = False
        else:
            # Resize image so height = img_h and width = char_w * label_len
            img_w = label_len * char_w
            img = cv2.resize(img, (img_w, img_h))

    except AttributeError:
        valid_img = False

    return img, valid_img


def read_data(config):
    """
    Lưu từ điển và label được xử lý trước cho tập dataset đã chọn
    """
    img_h = config.img_h
    char_w = config.char_w
    partition = config.partition
    out_name = config.data_file
    data_folder_path = config.data_folder_path
    dataset = config.dataset

    datasets = []
    if dataset == "all":
        print("dataset", dataset)
        datasets = ["iam_lines", "iam_words", "vietnamese", "vnondb_lines"]
    else:
        datasets = dataset.split(",")

    train_ids = {}  # {'name_dataset': [id1, id2, ...]}
    val_ids = {}
    test_ids = {}
    partition_ids = {}
    words_raw = []

    # Bước 1: Đọc dữ liệu từ các tập dữ liệu đã chọn
    for name_dataset in datasets:
        if partition == "train":
            path = data_folder_path + "/partition/" + name_dataset + "/train.txt"
        elif partition == "val":
            path = data_folder_path + "/partition/" + name_dataset + "/val.txt"
        else:
            path = data_folder_path + "/partition/" + name_dataset + "/test.txt"

        # Lưu data bao gồm: file ảnh + label
        with open(path, "r", encoding="utf-8") as f:
            partition_ids[name_dataset] = f.readlines()

        # Đọc các kí tự
        with open(data_folder_path + "/labels/" + name_dataset + ".txt", "r", encoding='utf-8') as f:
            words_raw = words_raw + f.readlines()

        # with open(path, "rb") as f:
        # ids = f.read().decode("unicode_escape")
        # partition_ids[name_dataset] = [i for i in ids.splitlines()]

        # Đọc nhãn và lọc ra những nhãn chỉ chứa dấu câu
        # with open(data_folder_path + "/labels/" + name_dataset + ".txt", "rb") as f:
        #     char = f.read().decode("unicode_escape")
        #     words_raw = words_raw + char.splitlines()

    # Bước 2: Lưu các kí tự có trong dataset
    punc_list = [".", "", ",", '"', "'", "(", ")", ":", ";", "!"]
    # Nhận danh sách các ký tự duy nhất và tạo từ điển để ánh xạ chúng thành số nguyên
    chars = np.unique(
        np.concatenate(
            [
                [char for char in line.split()[-1] if line.split()[-1] not in punc_list]
                for line in words_raw
            ]
        )
    )
    char_map = {value: idx + 1 for (idx, value) in enumerate(chars)}
    char_map["<BLANK>"] = 0
    num_chars = len(char_map.keys())

    # Bước 3: Lưu dữ liệu từ các tập dữ liệu đã chọn
    word_data = (
        {}
    )  # Lưu dữ liệu bao gồm [mảng 1, mảng 2] với mảng 1 mà mỗi phần tử là số nguyên tương ứng với kí tự trong từ điển và mảng 2 là data của ảnh
    valid_extensions = [".jpg", ".png", ".jpeg"]
    for name_dataset in datasets:
        lines_in_file = partition_ids[name_dataset]
        for line in lines_in_file:
            tmp = line.split()
            print("tmp", tmp)

            img_id = tmp[0]
            img_path = f"{data_folder_path}/dataset/{name_dataset}/{img_id}"
            if not any(img_path.lower().endswith(ext) for ext in valid_extensions):
                # Thêm phần mở rộng ".png" vào cuối đường dẫn
                img_path += ".png"

            label = tmp[1].replace("|", " ")

            img, valid_img = read_image(img_path, len(label), img_h, char_w)
            if valid_img:
                try:
                    word_data[img_id] = [[char_map[char] for char in label], img]
                except KeyError:
                    pass

    print(f"Number of images = {len(word_data)}")
    print(f"Number of unique characters = {num_chars}")
    print(f"charmap = {char_map}")

    # Save the data
    with open(f"{out_name}", "wb") as f:
        pkl.dump(
            {"word_data": word_data, "char_map": char_map, "num_chars": num_chars},
            f,
            protocol=pkl.HIGHEST_PROTOCOL,
        )


if __name__ == "__main__":
    from config import Config

    config = Config
    print("Processing Data:\n")
    read_data(config)
    print("\nData processing completed")
