import os
import glob

def process_files_in_directories(
    input_dirs,
    output_dir_suffix="_processed",
    file_extension="*.txt",
    delimiter="|",  # Using '|' as the default delimiter, based on common needs
    append_full_filename=True # Option to include file extension in the appended filename
):
    """
    Processes text files in specified input directories, adds a filename column,
    and saves them to new output directories.

    Args:
        input_dirs (list): A list of input directory names (e.g., ['train', 'val', 'test']).
        output_dir_suffix (str): Suffix to append to input directory names to create output directory names.
        file_extension (str): Glob pattern for files to process (e.g., "*.txt").
        delimiter (str): Delimiter to use before adding the filename column.
        append_full_filename (bool): If True, appends the full filename (e.g., "file.txt").
                                     If False, appends the filename without extension (e.g., "file").
    """
    # Get the directory where this script is located.
    # This helps in resolving relative paths for input/output directories.
    script_dir = os.path.dirname(os.path.abspath(__file__))

    for input_dir_name in input_dirs:
        # Construct the full paths for the input and corresponding output directories
        input_dir_path = os.path.join(script_dir, input_dir_name)
        output_dir_name = f"{input_dir_name}{output_dir_suffix}"
        output_dir_path = os.path.join(script_dir, output_dir_name)

        # Skip processing if the input directory doesn't exist
        if not os.path.isdir(input_dir_path):
            print(f"Warning: Input directory '{input_dir_path}' not found. Skipping.")
            continue

        # Create the output directory if it doesn't already exist.
        # `exist_ok=True` prevents an error if the directory is already there.
        os.makedirs(output_dir_path, exist_ok=True)
        print(f"\nProcessing directory: '{input_dir_path}' -> Output directory: '{output_dir_path}'")

        # Build the search pattern for files (e.g., "path/to/train_one_act/*.txt")
        file_search_pattern = os.path.join(input_dir_path, file_extension)
        input_files = glob.glob(file_search_pattern)

        # Inform the user if no files were found matching the pattern
        if not input_files:
            print(f"No files matching '{file_extension}' found in '{input_dir_path}'.")
            continue

        # Process each file found in the input directory
        for input_filepath in input_files:
            # Extract just the filename (e.g., "2121.txt") from the full path
            base_filename = os.path.basename(input_filepath)

            # Determine whether to append the full filename or just its name without extension
            if append_full_filename:
                filename_to_append = base_filename  # Use "2121.txt"
            else:
                # Get the filename without its extension (e.g., "2121" from "2121.txt")
                filename_to_append = os.path.splitext(base_filename)[0]

            # Define the full path for the new output file, keeping the original filename
            output_filepath = os.path.join(output_dir_path, base_filename)

            print(f"  Processing '{base_filename}' -> '{output_filepath}' (appending: '{filename_to_append}')")

            try:
                # Open the input file for reading and the output file for writing.
                # 'utf-8' encoding is used for broad character support.
                with open(input_filepath, 'r', encoding='utf-8') as infile, \
                     open(output_filepath, 'w', encoding='utf-8') as outfile:
                    for line in infile:
                        # Remove any trailing newline or carriage return characters from the line
                        stripped_line = line.rstrip('\n\r')
                        # Construct the new line: original content + delimiter + filename + newline
                        new_line = f"{stripped_line}{delimiter}{filename_to_append}\n"
                        outfile.write(new_line)
                print(f"  Successfully created '{output_filepath}'")
            except Exception as e:
                # Catch and report any errors encountered during file processing
                print(f"  Error processing file {input_filepath}: {e}")

if __name__ == "__main__":
    # --- Script Configuration ---
    # List of input subdirectories to process. These should be relative to where the script is run.
    INPUT_DIRECTORIES = ['train_one_act', 'val_one_act', 'test_one_act']
    # Suffix to add to input directory names to create the output directories (e.g., 'train_one_act_processed')
    OUTPUT_DIRECTORY_SUFFIX = "_processed"
    # File pattern to search for within the input directories (e.g., "*.txt" will find all .txt files)
    FILE_PATTERN_TO_PROCESS = "*.txt"

    # The character or string to use as a separator before the appended filename.
    # For example, if your line is "Hello World" and filename is "doc1", output could be "Hello World|doc1".
    COLUMN_DELIMITER = "|"

    # Control whether the full filename (e.g., "2121.txt") or just the name without extension (e.g., "2121")
    # should be appended to each line.
    # Set to 'False' if you want "2121" from "2121.txt" (as per your example "A|...|2121").
    # Set to 'True' if you want "2121.txt" from "2121.txt".
    APPEND_FULL_FILENAME = False

    print("Starting file processing script...")
    process_files_in_directories(
        input_dirs=INPUT_DIRECTORIES,
        output_dir_suffix=OUTPUT_DIRECTORY_SUFFIX,
        file_extension=FILE_PATTERN_TO_PROCESS,
        delimiter=COLUMN_DELIMITER,
        append_full_filename=APPEND_FULL_FILENAME
    )
    print("\nScript finished.")