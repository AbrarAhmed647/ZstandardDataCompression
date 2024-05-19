# Zstandard Compression and Decompression Usage Document


Initial Requirements-
1. Python 3 (version >3.7) 
    - Check if your PC has Python installed using "python --version"; if not download using the following link.
2. (For Windows) VScode or other IDE (Optional, but preferred to view, edit, and run the code)
    (For Linux) Use CLI to run directly or code editors to make changes to code

Download links-
1. Python - https://www.python.org/downloads/
2. VScode - https://code.visualstudio.com/download

# Initial steps-
1. Unzip the ZstandardDataCompression.zip package and open the ZSTD folder on VScode.
2. On VScode, open terminal by selecting 'Terminal -> New Terminal' on menu bar or press ctrl+shift+` to open a new terminal.
3. Navigate to the ZSTD folder and Run the command "pip install -r requirements.txt"

- This command installs zstandard and other requirements; if it fails with "pip not found" error, then install pip on python. reference: https://pip.pypa.io/en/stable/installation/ .


# Dictionary building using zstd_dict.py

NOTE: This step is a one-time step that builds a dictionary used for compression, initially the package comes with a default dictionary that has been trained on a random sample of RadioLF data, however, if you come across that the performance of compression is worse, then re-training the dictionary on a new sample or bigger sample might be useful. However, keep in mind that training on a very large sample i.e., huge no.of files in dict_data folder might not give the expected results, because of various issues such as overhead.

Format: python zstd_dict.py 'dict_folder_path' 'output_file_path' --dict_size [size in MB]

Example: python zstd_dict.py 'test_14/dict' 'test_14/traineddict.dict' --dict_size 1

- arguments:
    dict_folder_path : Path to folder that contains .mat files samples to create the dictionary
    output_file_path : Path to output .dict dictionary file 
    --dict_size: Size of dictionary in MB (Default=1)

- Notes:
    1. Adjust the dict_size parameter according to your desired dictionary size. Default is 1  (1 MB)
    2. In the case that there are not enough files in 'dict_folder_path', this function throws error of "zstd.ZstdError: cannot train dict: Src size is incorrect", in this case please add sufficient data on the folder atleast 200MB of .mat files to train the dictionary correctly.

Functions:
 read_mat_files_as_bytes(folder_path)
    Description: Reads .mat files from the specified folder and returns their contents as a list of bytes.
    Parameters:
        folder_path: Path to the folder containing .mat files.
    Returns:
        samples: List of bytes representing the contents of .mat files.

 train_dictionary(dict_size, samples, output_file_path)
    Description: Trains a Zstandard dictionary using the provided samples.
    Parameters:
        dict_size: Size of the dictionary in MegaBytes.
        samples: List of bytes representing data samples to train the dictionary. Returned by previous function.
        output_file_path : Path of output dictionary file
    Output:
        Saves the trained dictionary as a file given in output_file_path


# COMPRESSION using ZSTcompress.py:
- The script will remove the raw .mat input data and replace it with compressed .zst data in the same folder as input data. You can make a copy of original data if you choose to do so. Moreover, decompressing the .zst files will result in original .mat files

- This script takes 'input_folder_path' as mandatory argument and takes two optional arguments 'dict_path' and 'compression level'.

Format: python ZSTcompress.py 'input_folder_path' --dict_path 'path_to_dictionary' --compression_level [1-19]

Example: python ZSTcompress.py 'test_14/PS' --dict_path trained_dict.dict --compression_level 10

- arguments:
    input_folder_path: Path to the folder containing files to be compressed.
    dict_path: Path to the dictionary file to be used for compression.
    compression_level: Compression level to be used (default is 9). Compression level allows the user to specify an integer value between 1 to 19.  1 is fast compression with low compression rate, where as 19 is best compression rate thus the compression takes time.

- Notes:
    The script automatically appends the .zst extension to the compressed files.
    If a dictionary file is not provided, the script will use the default Zstandard compression without a custom dictionary, which can reduce performance.
	
# Decompression using ZSTdecompress.py
-  The script will decompress the .zst files  and replace it with original .mat files in the same folder and deletes the .zst files.

- This script takes 'input_folder_path' as mandatory argument and takes one optional arguments 'dict_path'

Format: python ZSTdecompress.py 'input_folder_path' --dict_path 'path_to_dictionary'

Example: python ZSTdecompress.py 'test_14/PS' --dict_path 'test_14/trained_dict.dict'

- arguments
    input_folder_path: Path to the folder containing files to be compressed.
    dict_path: Path to the dictionary file to be used for compression.






