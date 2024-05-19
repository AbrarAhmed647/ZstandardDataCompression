#!/usr/bin/env python3
import zstandard as zstd
import time
import os
import argparse
from tqdm import tqdm

def decompress_file(input_file_path,dict_path):

    with open(dict_path, 'rb') as dict_file:
        dictionary = zstd.ZstdCompressionDict(dict_file.read())

    try:
        decompressor = zstd.ZstdDecompressor(dict_data=dictionary)
        
        # Open the .zst file to decompress
        with open(input_file_path, 'rb') as compressed_file:
            decompressed_data = decompressor.decompress(compressed_file.read())
        
        # Construct the output file path by removing .zst extension
        output_file_path = input_file_path.rsplit('.zst', 1)[0]
        
        # Write the decompressed data
        with open(output_file_path, 'wb') as output_file:
            output_file.write(decompressed_data)
        
        # Optionally delete the original .zst file
        os.remove(input_file_path)
        
       # print(f"Decompressed '{input_file_path}' and created '{output_file_path}'. Original .zst file has been deleted.")
    except FileNotFoundError:
        print(f"Error: The file '{input_file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred while decompressing '{input_file_path}': {e}")

def decompress_folder(input_folder_path, dict_path):

    files_to_decompress = [os.path.join(root, file)
                           for root, dirs, files in os.walk(input_folder_path)
                           for file in files if file.endswith('.zst')]
    
    with tqdm(total=len(files_to_decompress), desc="Decompressing files", unit="file") as pbar:
        for file_path in files_to_decompress:
            decompress_file(file_path, dict_path)
            pbar.update(1)
    
    print(f"All .zst files in '{input_folder_path}' have been decompressed and the original .zst files have been deleted.")


def main():
    parser = argparse.ArgumentParser(description="Compress files in a folder using Zstandard.")
    parser.add_argument("input_folder_path", type=str, help="The path of the folder to compress.")
    parser.add_argument("--dict_path", type=str, default="", help="Optional dictionary path for compression.")
   
    args = parser.parse_args()

    decompress_folder(args.input_folder_path, args.dict_path)

if __name__ == "__main__":
    main()