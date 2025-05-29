import os
import glob

def concatenate_files_in_folders(
    input_folder_configs, # List of tuples: (input_dir_name, output_file_name)
    file_extension="*.txt"
):
    """
    Concatenates all files with a given extension from specified input directories
    into respective single output files.

    Args:
        input_folder_configs (list of tuples): Each tuple contains:
            (str) input_directory_name (e.g., "train_processed_spkchange")
            (str) output_filename (e.g., "train.txt")
        file_extension (str): Glob pattern for files to concatenate (e.g., "*.txt").
    """
    # Get the directory where this script is located. This assumes the input
    # subdirectories and the final output files will be relative to this script's location.
    script_dir = os.path.dirname(os.path.abspath(__file__))

    for input_dir_name, output_filename in input_folder_configs:
        input_dir_path = os.path.join(script_dir, input_dir_name)
        # The output file will be placed in the main script directory
        output_filepath = os.path.join(script_dir, output_filename)

        print(f"\nProcessing directory: '{input_dir_path}'")
        print(f"Outputting to: '{output_filepath}'")

        # Skip if the input directory doesn't exist
        if not os.path.isdir(input_dir_path):
            print(f"Warning: Input directory '{input_dir_path}' not found. Skipping.")
            continue

        # Find all files matching the pattern in the input directory.
        # Sorting them ensures a consistent order when concatenating,
        # which is useful if filenames have a natural numerical or alphabetical sort order.
        file_search_pattern = os.path.join(input_dir_path, file_extension)
        files_to_concatenate = sorted(glob.glob(file_search_pattern))

        # Handle cases where no files are found in the input directory
        if not files_to_concatenate:
            print(f"No files matching '{file_extension}' found in '{input_dir_path}'.")
            # Create an empty output file in this case to ensure the file exists.
            with open(output_filepath, 'w', encoding='utf-8') as outfile:
                pass # This just creates an empty file
            print(f"Created empty file: '{output_filepath}'")
            continue

        # Open the final output file in write mode ('w'). This will create the file
        # if it doesn't exist, or overwrite it if it does.
        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            for individual_filepath in files_to_concatenate:
                file_basename = os.path.basename(individual_filepath)
                print(f"  Concatenating: '{file_basename}'")
                try:
                    # Open each individual file for reading
                    with open(individual_filepath, 'r', encoding='utf-8') as infile:
                        # Read the entire content of the individual file
                        content = infile.read()
                        # Write the content directly to the aggregate output file
                        outfile.write(content)
                        # Note: We're relying on the previous processing steps to ensure
                        # each line (and thus each file's content) ends with a newline.
                        # If a file didn't end with a newline, and we wanted to ensure one
                        # between files, we could add a check here:
                        # if content and not content.endswith('\n'):
                        #    outfile.write('\n')
                except Exception as e:
                    print(f"    Error reading or writing file {individual_filepath}: {e}")
        print(f"Successfully created concatenated file: '{output_filepath}'")

if __name__ == "__main__":
    # --- Configuration ---

    # Define the input directories (these should be the output from the speaker change script)
    # and the desired names for the final concatenated output files.
    # Each tuple specifies: (source_folder_name, target_concatenated_filename).
    CONCATENATION_CONFIGS = [
        ("train_one_act_processed_spksegment", "train.txt"),
        ("val_one_act_processed_spksegment", "val.txt"),
        ("test_one_act_processed_spksegment", "test.txt")
    ]

    # The file pattern to look for in each input directory for concatenation.
    FILE_PATTERN_TO_CONCATENATE = "*.txt"

    print("Starting script to concatenate files...")
    concatenate_files_in_folders(
        input_folder_configs=CONCATENATION_CONFIGS,
        file_extension=FILE_PATTERN_TO_CONCATENATE
    )
    print("\nScript finished.")