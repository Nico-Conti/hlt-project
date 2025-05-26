import os
import glob

def remove_last_n_columns(
    input_to_output_dir_map, # Dictionary mapping input dir names to output dir names
    file_extension="*.txt",
    delimiter="|",
    columns_to_remove=2
):
    """
    Reads files from input directories, removes the last N columns from each line,
    and writes the modified content to corresponding output directories.

    Args:
        input_to_output_dir_map (dict): A dictionary where keys are input directory names
                                        (e.g., 'train_processed_spksegment_filename') and values are
                                        the desired output directory names (e.g., 'train_one_act').
        file_extension (str): Glob pattern for files to process.
        delimiter (str): The delimiter used in the files.
        columns_to_remove (int): The number of columns to remove from the end of each line.
    """
    # Get the directory where the script is located
    # Assumes input directories are subdirectories relative to the script's location
    # or absolute paths if provided as such in input_to_output_dir_map keys
    script_dir = os.path.dirname(os.path.abspath(__file__))

    for input_dir_name, output_dir_name in input_to_output_dir_map.items():
        # Check if input_dir_name is already an absolute path
        if os.path.isabs(input_dir_name):
            input_dir_path = input_dir_name
        else:
            input_dir_path = os.path.join(script_dir, input_dir_name)

        # Check if output_dir_name is already an absolute path
        if os.path.isabs(output_dir_name):
            output_dir_path = output_dir_name
        else:
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
            original_filename = os.path.basename(input_filepath)
            output_filepath = os.path.join(output_dir_path, original_filename)

            print(f"  Processing '{original_filename}' -> '{output_filepath}' (removing last {columns_to_remove} columns)")

            try:
                with open(input_filepath, 'r', encoding='utf-8') as infile, \
                     open(output_filepath, 'w', encoding='utf-8') as outfile:

                    for line_number, line in enumerate(infile, 1):
                        stripped_line = line.rstrip('\n\r')

                        if not stripped_line: # Preserve empty lines
                            outfile.write("\n")
                            continue

                        parts = stripped_line.split(delimiter)

                        # Determine parts to keep
                        if len(parts) > columns_to_remove:
                            parts_to_keep = parts[:-columns_to_remove]
                        else:
                            # If there are fewer or equal parts than columns_to_remove,
                            # the result will be an empty line.
                            parts_to_keep = []

                        new_line_content = delimiter.join(parts_to_keep)
                        outfile.write(new_line_content + "\n")

                print(f"  Successfully created '{output_filepath}'")
            except Exception as e:
                print(f"  Error processing file {input_filepath} (line ~{line_number if 'line_number' in locals() else 'unknown'}): {e}")

if __name__ == "__main__":
    # --- Configuration ---

    # Define the mapping from your current input directories (which contain the extra columns)
    # to the new output directories where the cleaned files will be saved.
    # The keys should be the names of the directories produced by your *previous* script
    # (e.g., the one that added the speaker segment and filename).
    # The values are the target names you specified.
    INPUT_OUTPUT_MAPPING = {
        'train': 'train_one_act',
        'val': 'val_one_act',
        'test': 'test_one_act'
    }
    # IMPORTANT: Adjust the keys and values in INPUT_OUTPUT_MAPPING to match
    # your actual input directory names and desired output directory names.
    # These can be relative paths (from the script's location) or absolute paths.

    FILE_PATTERN = "*.txt"
    DATA_DELIMITER = "|"
    NUM_COLUMNS_TO_STRIP = 2 # We want to remove the last two columns

    print("Starting script to remove last two columns...")
    remove_last_n_columns(
        input_to_output_dir_map=INPUT_OUTPUT_MAPPING,
        file_extension=FILE_PATTERN,
        delimiter=DATA_DELIMITER,
        columns_to_remove=NUM_COLUMNS_TO_STRIP
    )
    print("\nScript finished.")