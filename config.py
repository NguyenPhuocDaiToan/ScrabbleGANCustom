import torch


class Config:
    # 'iam_lines,iam_words,vietnamese,vnondb_lines' (or 'all')
    dataset = "iam_lines,iam_words,vietnamese,vnondb_lines"
    data_folder_path = "./data"  # use to run prepare_dataset.pu
    img_h = 32
    char_w = 16
    partition = "train"  # 'train' / 'val' / 'test'

    batch_size = 8
    num_epochs = 32
    epochs_lr_decay = 100  # learning rate decay will be applied for last these many steps (should be <= num_epochs)
    resume_training = False
    start_epoch = 5

    train_gen_steps = (
        4  # generator weights to be updated after every specified number of steps
    )
    grad_alpha = 1
    grad_balance = True

    root_path = "ScrabbleGANCustom"
    data_file = f"/content/ScrabbleGAN/process_data.pkl"
    lexicon_file = f"/content/ScrabbleGANCustom/data/lexicon/iam/words.txt"
    lmdb_output = f"./content/result/{dataset}_{partition}_data"

    architecture = "ScrabbleGAN"
    # Recognizer network
    r_ks = [3, 3, 3, 3, 3, 3, 2]
    r_pads = [1, 1, 1, 1, 1, 1, 0]
    r_fs = [64, 128, 256, 256, 512, 512, 512]

    # Generator and Discriminator networks
    # arch[g_resolution] defines the architecture to be selected
    # arch[16] has been added in BigGAN.py with parameters as specified in the paper
    resolution = 16
    bn_linear = "SN"
    g_shared = False

    g_lr = 2e-4
    d_lr = 2e-4
    r_lr = 2e-4
    g_betas = [0.0, 0.999]
    d_betas = [0.0, 0.999]
    r_betas = [0.0, 0.999]
    g_loss_fn = "HingeLoss"
    d_loss_fn = "HingeLoss"
    r_loss_fn = "CTCLoss"

    # Noise vector
    z_dim = 128
    num_chars = 170

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
