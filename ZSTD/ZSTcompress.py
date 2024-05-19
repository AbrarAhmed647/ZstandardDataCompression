#!/usr/bin/env python3
import zstandard as zstd
import time
import os
import argparse
from tqdm import tqdm

def compress_file(input_file_path, dict_path, compression_level=9):  #default compression level =9; if it's not user defined
    
    # Open the dictionary file you want to use
    with open(dict_path, 'rb') as dict_file:
        dictionary = zstd.ZstdCompressionDict(dict_file.read())
    
    #open the file to compress
    try:
        with open(input_file_path, 'rb') as input_file:
            data = input_file.read()
    except FileNotFoundError:
        print(f"Error: The file '{input_file_path}' does not exist. Please check the file path and try again.")

    compressor = zstd.ZstdCompressor(level=compression_level,threads=30,dict_data=dictionary)
    #calculating compression time
    start_time = time.time()
    # Compress the data
    try:
        output_file_path=input_file_path+'.zst'

        with open(output_file_path, 'wb') as output_file:
            output_file.write(compressor.compress(data))

        os.remove(input_file_path)

        end_time=time.time()

        duration= end_time-start_time

        #print(f"File '{input_file_path}' compressed to '{output_file_path}' with compression level {compression_level}")
       # print(f"Compression took {duration:.2f} seconds.")

    except FileNotFoundError:
        print(f"Error: The path '{output_file_path}' is not correct. Please check the file path and try again.")
    
def compress_folder(input_folder_path, dict_path, compression_level=9): #default compression level =9 if it's not user defined

    start_time=time.time()

    files_to_compress = [os.path.join(root, file)
                         for root, dirs, files in os.walk(input_folder_path)
                         for file in files if file.endswith('.mat')]
    
    with tqdm(total=len(files_to_compress), desc="Compressing files", unit="file") as pbar:
        for file_path in files_to_compress:
            compress_file(file_path, dict_path, compression_level)
            pbar.update(1)

    end_time=time.time()
    duration =end_time-start_time

    #print(f"All files in '{input_folder_path}' have been compressed and saved to '{output_folder_path}'.")
    print(f"Compression took {duration:.2f} seconds.")



def main():
    parser = argparse.ArgumentParser(description="Compress files in a folder using Zstandard.")
    parser.add_argument("input_folder_path", type=str, help="The path of the folder to compress.")
    parser.add_argument("--dict_path", type=str, default="", help="Optional dictionary path for compression.")
    parser.add_argument("--compression_level", type=int, default=9, help="Compression level (1-22). Default is 9.")

    args = parser.parse_args()

    compress_folder(args.input_folder_path, args.dict_path, args.compression_level)

if __name__ == "__main__":
    main()



