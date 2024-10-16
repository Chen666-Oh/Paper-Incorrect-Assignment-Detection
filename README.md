# Paper-Incorrect-Assignment-Detection

## Introduction
We have currently made public only the code related to the ChatGLM used in our paper. Once our paper is accepted, we will release the remaining parts of the code.

## Preparation
### prerequisites
- Linux
- Python 3.10
- PyTorch 2.2.0+cu121

### data
1. Download the dataset(WhoIsWho-na-v3.1) and place it in the folder `./ChatGLM3/dataset`.  
The WhoIsWho-na-v3.1 dataset used in our paper is sourced from [AMiner.cn](https://www.aminer.cn/open/article?id=5de9efd2530c707ed8b87d99). We have already compressed the dataset and uploaded it to Google Cloud. You can click [here](https://drive.google.com/drive/folders/1p731oybOZ6J7Iji43htE790q_yzf_MSA?usp=sharing) to download it.  

2. After downloading and decompressing, you can see the following three data files:  
1）train_author.json:  
This file is organized into a dictionary. The key is the author ID, and the value includes the author's name ("name"), the ID of the paper published by the relevant author ("normal_data"), and the ID of the paper incorrectly assigned to the author ("outliers")  
2）pid_to_info_all.json:  
This file contains specific paper information for all papers that may be involved in the paper.  
3）ind_valid_author.json:   
Is organized in the same format as train_author.json

### requirements
```
pip install -r requirements
```

## Experiments
### train
```bash
cd ChatGLM3/train
```

1.Use the title information to train the **Titles Model**:
```bash
sh scripts/train_title.sh
```

2.Use the author information to train the **Authors Model**:
```bash
sh scripts/train_author.sh
```

3.Use all the information to train the **Full Deatails Model**:
```bash
sh scripts/train_all_info.sh
```
