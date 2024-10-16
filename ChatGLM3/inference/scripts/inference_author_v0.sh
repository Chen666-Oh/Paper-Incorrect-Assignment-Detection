#!/bin/bash

#SBATCH -p gpu
#SBATCH -J inference_author_v0
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -o inference_author_v0.o
#SBATCH -e inference_author_v0.e
#SBATCH --gres=gpu:8

# Please replace with your environment path
export PATH=/xxx/xxx/python3.10:$PATH
export PATH=/xxx/anaconda3/envs/xxx/bin:$PATH
export PATH=/xxx/cuda-12.1/bin:$PATH

MAX_SOURCE_LEN=30000
MAX_TARGET_LEN=16
LORA_PATH=../../train/output/chatglm_author
MODEL_PATH=/xxx/ChatGLM/ZhipuAI/chatglm3-6b-32k  # The Path of Large Language Models
PUB_PATH=../../dataset/pid_to_info_all.json
EVAL_PATH=../../dataset/ind_valid_author.json
SAVED_DIR=../test_result
TEST_SCORE_FILE=None
SAVE_NAME=author_v0_seed42.json

accelerate launch --num_processes 8 ../inference_authors.py \
    --lora_path $LORA_PATH \
    --model_path $MODEL_PATH \
    --pub_path $PUB_PATH  \
    --eval_path $EVAL_PATH \
    --saved_dir $SAVED_DIR \
    --seed 42 \
    --max_source_length $MAX_SOURCE_LEN \
    --max_target_length $MAX_TARGET_LEN \
    --test_score_file $TEST_SCORE_FILE \
    --save_name $SAVE_NAME
