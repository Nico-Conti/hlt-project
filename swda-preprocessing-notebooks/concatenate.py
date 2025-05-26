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
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Assumes script is in the parent project directory

    for input_dir_name, output_filename in input_folder_configs:
        input_dir_path = os.path.join(script_dir, input_dir_name)
        output_filepath = os.path.join(script_dir, output_filename) # Output in the main project directory

        print(f"\nProcessing directory: '{input_dir_path}'")
        print(f"Outputting to: '{output_filepath}'")

        if not os.path.isdir(input_dir_path):
            print(f"Warning: Input directory '{input_dir_path}' not found. Skipping.")
            continue

        # Find all files matching the pattern in the input directory
        # Sorting ensures a consistent order if filenames have a natural sort order
        file_search_pattern = os.path.join(input_dir_path, file_extension)
        files_to_concatenate = sorted(glob.glob(file_search_pattern))

        if not files_to_concatenate:
            print(f"No files matching '{file_extension}' found in '{input_dir_path}'.")
            # Create an empty output file if no input files are found
            with open(output_filepath, 'w', encoding='utf-8') as outfile:
                pass # Creates an empty file
            print(f"Created empty file: '{output_filepath}'")
            continue

        # Open the final output file in write mode (this will overwrite if it exists)
        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            for individual_filepath in files_to_concatenate:
                file_basename = os.path.basename(individual_filepath)
                print(f"  Concatenating: '{file_basename}'")
                try:
                    with open(individual_filepath, 'r', encoding='utf-8') as infile:
                        # Read the content of the individual file
                        content = infile.read()
                        # Write it to the aggregate output file
                        outfile.write(content)
                        # Ensure a newline if the file didn't end with one,
                        # though our previous scripts should ensure this.
                        # If `content` is not empty and doesn't end with a newline, add one.
                        # This is usually not needed if files are well-formed.
                        # if content and not content.endswith('\n'):
                        #    outfile.write('\n')
                except Exception as e:
                    print(f"    Error reading or writing file {individual_filepath}: {e}")
        print(f"Successfully created concatenated file: '{output_filepath}'")

if __name__ == "__main__":
    # --- Configuration ---

    # Define the input directories (output from the speaker change script)
    # and the desired name for the final concatenated output file.
    # Each tuple is (source_folder_name, target_concatenated_filename)
    CONCATENATION_CONFIGS = [
        ("train_processed_spksegment", "train.txt"),
        ("val_processed_spksegment", "val.txt"),
        ("test_processed_spksegment", "test.txt")
    ]

    # File pattern to look for in each directory for concatenation
    FILE_PATTERN_TO_CONCATENATE = "*.txt"

    print("Starting script to concatenate files...")
    concatenate_files_in_folders(
        input_folder_configs=CONCATENATION_CONFIGS,
        file_extension=FILE_PATTERN_TO_CONCATENATE
    )
    print("\nScript finished.")