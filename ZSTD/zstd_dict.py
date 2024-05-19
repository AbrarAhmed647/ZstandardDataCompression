#!/usr/bin/env python3

import os
import zstandard as zstd
from tqdm import tqdm
import argparse

def read_mat_files_as_bytes(folder_path):
    samples = []
    for filename in tqdm(os.listdir(folder_path), desc="Reading .mat files"):
        if filename.endswith('.mat'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'rb') as file:
                file_bytes = file.read()
                samples.append(file_bytes)
    return samples

def train_dictionary(dict_size, samples, output_file_path):
    #dict_data = zstd.ZstdCompressionDict(samples, dict_type=zstd.DICT_TYPE_FULLDICT)

    dict_data = zstd.train_dictionary(dict_size*1024*1024, samples, notifications=4 )
    with open(output_file_path, "wb") as dict_file:
        dict_file.write(dict_data.as_bytes())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a Zstandard dictionary from .mat files.")
    parser.add_argument('dict_folder_path', type=str, help='Path to the folder containing .mat files.')
    parser.add_argument('output_file_path', type=str, help='Path to save the trained dictionary file.')
    parser.add_argument('--dict_size', type=int, default=1, help='Size of the dictionary in MegaBytes (default: 1MB).')
    
    args = parser.parse_args()
    
    samples = read_mat_files_as_bytes(args.dict_folder_path)
    train_dictionary(args.dict_size, samples, args.output_file_path)
    print("Dictionary is created")

    
