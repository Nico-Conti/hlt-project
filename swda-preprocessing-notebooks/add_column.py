import os
import glob

def process_files_in_directories(
    input_dirs,
    output_dir_suffix="_processed",
    file_extension="*.txt",
    delimiter="|",  # Changed to '|' based on your example
    append_full_filename=True # New option
):
    """
    Processes text files in specified input directories, adds a filename column,
    and saves them to new output directories.

    Args:
        input_dirs (list): A list of input directory names (e.g., ['train', 'val', 'test']).
        output_dir_suffix (str): Suffix to append to input directory names to create output directory names.
        file_extension (str): Glob pattern for files to process (e.g., "*.txt").
        delimiter (str): Delimiter to use before adding the filename column.
        append_full_filename (bool): If True, appends full filename (e.g., "file.txt").
                                     If False, appends filename without extension (e.g., "file").
    """
    # Get the directory where the script is located
    # Assumes train/val/test are subdirectories relative to the script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))

    for input_dir_name in input_dirs:
        input_dir_path = os.path.join(script_dir, input_dir_name)
        output_dir_name = f"{input_dir_name}{output_dir_suffix}"
        output_dir_path = os.path.join(script_dir, output_dir_name)

        if not os.path.isdir(input_dir_path):
            print(f"Warning: Input directory '{input_dir_path}' not found. Skipping.")
            continue

        os.makedirs(output_dir_path, exist_ok=True)
        print(f"\nProcessing directory: '{input_dir_path}' -> Output directory: '{output_dir_path}'")

        file_search_pattern = os.path.join(input_dir_path, file_extension)
        input_files = glob.glob(file_search_pattern)

        if not input_files:
            print(f"No files matching '{file_extension}' found in '{input_dir_path}'.")
            continue

        for input_filepath in input_files:
            base_filename = os.path.basename(input_filepath) # e.g., "2121.txt"

            if append_full_filename:
                filename_to_append = base_filename
            else:
                filename_to_append = os.path.splitext(base_filename)[0] # e.g., "2121"

            output_filepath = os.path.join(output_dir_path, base_filename) # Save with same original name

            print(f"  Processing '{base_filename}' -> '{output_filepath}' (appending: '{filename_to_append}')")

            try:
                with open(input_filepath, 'r', encoding='utf-8') as infile, \
                     open(output_filepath, 'w', encoding='utf-8') as outfile:
                    for line in infile:
                        stripped_line = line.rstrip('\n\r')
                        new_line = f"{stripped_line}{delimiter}{filename_to_append}\n"
                        outfile.write(new_line)
                print(f"  Successfully created '{output_filepath}'")
            except Exception as e:
                print(f"  Error processing file {input_filepath}: {e}")

if __name__ == "__main__":
    # --- Configuration ---
    INPUT_DIRECTORIES = ['train', 'val', 'test']
    OUTPUT_DIRECTORY_SUFFIX = "_processed"
    FILE_PATTERN_TO_PROCESS = "*.txt" # Process all .txt files

    # Set your desired delimiter here based on your example:
    COLUMN_DELIMITER = "|"

    # Choose whether to append the full filename (e.g., "2121.txt")
    # or just the name without extension (e.g., "2121")
    # For your example "A|...|2121", you likely want False.
    APPEND_FULL_FILENAME = False # Set to False to get "2121" from "2121.txt"
                                 # Set to True to get "2121.txt" from "2121.txt"

    print("Starting script...")
    process_files_in_directories(
        input_dirs=INPUT_DIRECTORIES,
        output_dir_suffix=OUTPUT_DIRECTORY_SUFFIX,
        file_extension=FILE_PATTERN_TO_PROCESS,
        delimiter=COLUMN_DELIMITER,
        append_full_filename=APPEND_FULL_FILENAME
    )
    print("\nScript finished.")