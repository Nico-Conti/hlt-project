import os
import glob

def process_files_in_directories(
    input_dirs,
    output_dir_suffix="_processed",
    file_extension="*.txt",
    delimiter="|",
    append_full_filename=True
):
    """
    Processes text files in specified input directories, adds a filename column,
    and saves them to new output directories.

    Args:
        input_dirs (list): List of input directory names (e.g., ['train', 'val', 'test']).
        output_dir_suffix (str): Suffix for output directory names.
        file_extension (str): Glob pattern for files to process (e.g., "*.txt").
        delimiter (str): Delimiter to use before adding the filename column.
        append_full_filename (bool): If True, appends full filename (e.g., "file.txt").
                                     If False, appends filename without extension (e.g., "file").
    """
    # Get the script's directory for resolving relative paths.
    script_dir = os.path.dirname(os.path.abspath(__file__))

    for input_dir_name in input_dirs:
        # Construct full paths for input and output directories.
        input_dir_path = os.path.join(script_dir, input_dir_name)
        output_dir_name = f"{input_dir_name}{output_dir_suffix}"
        output_dir_path = os.path.join(script_dir, output_dir_name)

        # Skip if input directory doesn't exist.
        if not os.path.isdir(input_dir_path):
            print(f"Warning: Input directory '{input_dir_path}' not found. Skipping.")
            continue

        # Create output directory if it doesn't exist.
        os.makedirs(output_dir_path, exist_ok=True)
        print(f"\nProcessing directory: '{input_dir_path}' -> Output directory: '{output_dir_path}'")

        # Find all files matching the pattern in the input directory.
        file_search_pattern = os.path.join(input_dir_path, file_extension)
        input_files = glob.glob(file_search_pattern)

        # Skip if no files are found.
        if not input_files:
            print(f"No files matching '{file_extension}' found in '{input_dir_path}'.")
            continue

        for input_filepath in input_files:
            base_filename = os.path.basename(input_filepath)

            # Decide whether to append full filename or just the name.
            if append_full_filename:
                filename_to_append = base_filename
            else:
                filename_to_append = os.path.splitext(base_filename)[0]

            # Define the output file path (keeps original filename).
            output_filepath = os.path.join(output_dir_path, base_filename)

            print(f"  Processing '{base_filename}' -> '{output_filepath}' (appending: '{filename_to_append}')")

            try:
                # Open input and output files.
                with open(input_filepath, 'r', encoding='utf-8') as infile, \
                     open(output_filepath, 'w', encoding='utf-8') as outfile:
                    for line in infile:
                        stripped_line = line.rstrip('\n\r') # Remove existing newlines
                        new_line = f"{stripped_line}{delimiter}{filename_to_append}\n" # Add column and new line
                        outfile.write(new_line)
                print(f"  Successfully created '{output_filepath}'")
            except Exception as e:
                print(f"  Error processing file {input_filepath}: {e}")

if __name__ == "__main__":
    # --- Configuration ---
    # Directories to process (e.g., 'train', 'val', 'test').
    INPUT_DIRECTORIES = ['train', 'val', 'test']
    # Suffix for new output directories (e.g., 'train_processed').
    OUTPUT_DIRECTORY_SUFFIX = "_processed"
    # File type to look for (e.g., "*.txt" for all text files).
    FILE_PATTERN_TO_PROCESS = "*.txt"

    # Delimiter for columns (e.g., "|" for pipe-separated).
    COLUMN_DELIMITER = "|"

    # Option to include the file extension in the appended filename column.
    # Set to False to get "2121" from "2121.txt", True for "2121.txt".
    APPEND_FULL_FILENAME = False

    print("Starting script...")
    process_files_in_directories(
        input_dirs=INPUT_DIRECTORIES,
        output_dir_suffix=OUTPUT_DIRECTORY_SUFFIX,
        file_extension=FILE_PATTERN_TO_PROCESS,
        delimiter=COLUMN_DELIMITER,
        append_full_filename=APPEND_FULL_FILENAME
    )
    print("\nScript finished.")