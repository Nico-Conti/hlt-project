import os
import glob

def remove_last_n_columns(
    input_to_output_dir_map, # Dictionary mapping input directory names to output directory names
    file_extension="*.txt",
    delimiter="|",
    columns_to_remove=2
):
    """
    Reads files from input directories, removes the last N columns from each line,
    and writes the modified content to corresponding output directories.

    Args:
        input_to_output_dir_map (dict): A dictionary where keys are input directory names
                                        (e.g., 'train_data_full') and values are
                                        the desired output directory names (e.g., 'train_clean').
                                        Paths can be relative to the script or absolute.
        file_extension (str): Glob pattern for files to process (e.g., "*.txt").
        delimiter (str): The character used to separate columns in the files.
        columns_to_remove (int): The number of columns to remove from the end of each line.
    """
    # Get the directory where this script is located.
    # This helps resolve relative paths provided in `input_to_output_dir_map`.
    script_dir = os.path.dirname(os.path.abspath(__file__))

    for input_dir_name, output_dir_name in input_to_output_dir_map.items():
        # Determine full input and output paths, handling both relative and absolute paths
        input_dir_path = input_dir_name if os.path.isabs(input_dir_name) else os.path.join(script_dir, input_dir_name)
        output_dir_path = output_dir_name if os.path.isabs(output_dir_name) else os.path.join(script_dir, output_dir_name)

        # Skip if the input directory does not exist
        if not os.path.isdir(input_dir_path):
            print(f"Warning: Input directory '{input_dir_path}' not found. Skipping.")
            continue

        # Create the output directory if it doesn't already exist.
        # `exist_ok=True` prevents an error if the directory is already present.
        os.makedirs(output_dir_path, exist_ok=True)
        print(f"\nProcessing directory: '{input_dir_path}' -> Output directory: '{output_dir_path}'")

        # Find all files matching the pattern in the input directory
        file_search_pattern = os.path.join(input_dir_path, file_extension)
        input_files = glob.glob(file_search_pattern)

        # Inform the user if no files were found
        if not input_files:
            print(f"No files matching '{file_extension}' found in '{input_dir_path}'.")
            continue

        # Process each file found
        for input_filepath in input_files:
            original_filename = os.path.basename(input_filepath)
            output_filepath = os.path.join(output_dir_path, original_filename)

            print(f"  Processing '{original_filename}' -> '{output_filepath}' (removing last {columns_to_remove} columns)")

            try:
                # Open input file for reading and output file for writing
                with open(input_filepath, 'r', encoding='utf-8') as infile, \
                     open(output_filepath, 'w', encoding='utf-8') as outfile:

                    for line_number, line in enumerate(infile, 1): # Keep track of line number for error reporting
                        stripped_line = line.rstrip('\n\r') # Remove trailing newlines

                        if not stripped_line: # Preserve empty lines as they are
                            outfile.write("\n")
                            continue

                        parts = stripped_line.split(delimiter)

                        # Check if there are enough columns to remove
                        if len(parts) > columns_to_remove:
                            parts_to_keep = parts[:-columns_to_remove] # Keep all parts except the last N
                        else:
                            # If there are fewer or equal parts than columns to remove,
                            # the result is an empty line after removal.
                            parts_to_keep = []

                        # Join the remaining parts back with the delimiter and add a newline
                        new_line_content = delimiter.join(parts_to_keep)
                        outfile.write(new_line_content + "\n")

                print(f"  Successfully created '{output_filepath}'")
            except Exception as e:
                # Report error along with the file and approximate line number
                print(f"  Error processing file {input_filepath} at line {line_number}: {e}")

if __name__ == "__main__":
 
    INPUT_OUTPUT_MAPPING = {
        'train_one_act_processed_spksegment': 'train_one_act_cleaned',
        'val_one_act_processed_spksegment': 'val_one_act_cleaned',
        'test_one_act_processed_spksegment': 'test_one_act_cleaned'
    }

    FILE_PATTERN = "*.txt"
    DATA_DELIMITER = "|"
    NUM_COLUMNS_TO_STRIP = 2 # Set this to how many columns you want to remove from the end

    print("Starting script to remove trailing columns...")
    remove_last_n_columns(
        input_to_output_dir_map=INPUT_OUTPUT_MAPPING,
        file_extension=FILE_PATTERN,
        delimiter=DATA_DELIMITER,
        columns_to_remove=NUM_COLUMNS_TO_STRIP
    )
    print("\nScript finished.")