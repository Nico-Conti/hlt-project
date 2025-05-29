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
    # Get the script's directory. This helps in resolving relative paths for
    # both input folders and where the final concatenated files will be saved.
    script_dir = os.path.dirname(os.path.abspath(__file__))

    for input_dir_name, output_filename in input_folder_configs:
        # Construct the full path for the input directory and the target output file.
        input_dir_path = os.path.join(script_dir, input_dir_name)
        output_filepath = os.path.join(script_dir, output_filename) # Output file goes in the script's root directory

        print(f"\nProcessing directory: '{input_dir_path}'")
        print(f"Outputting to: '{output_filepath}'")

        # Skip this configuration if the input directory doesn't exist.
        if not os.path.isdir(input_dir_path):
            print(f"Warning: Input directory '{input_dir_path}' not found. Skipping.")
            continue

        # Find all files within the input directory that match the specified extension.
        # `sorted()` ensures a consistent order of concatenation, which is good practice.
        file_search_pattern = os.path.join(input_dir_path, file_extension)
        files_to_concatenate = sorted(glob.glob(file_search_pattern))

        # If no files are found, create an empty output file and notify.
        if not files_to_concatenate:
            print(f"No files matching '{file_extension}' found in '{input_dir_path}'.")
            with open(output_filepath, 'w', encoding='utf-8') as outfile:
                pass # This simply creates an empty file
            print(f"Created empty file: '{output_filepath}'")
            continue

        # Open the final aggregate output file in write mode ('w').
        # This will create the file or overwrite it if it already exists.
        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            for individual_filepath in files_to_concatenate:
                file_basename = os.path.basename(individual_filepath)
                print(f"  Concatenating: '{file_basename}'")
                try:
                    # Open each individual file for reading.
                    with open(individual_filepath, 'r', encoding='utf-8') as infile:
                        content = infile.read() # Read the entire content of the current file.
                        outfile.write(content)   # Write it to the combined output file.
                        # Our previous scripts should ensure each file ends with a newline.
                        # If not, you might uncomment the following to add one for separation:
                        # if content and not content.endswith('\n'):
                        #    outfile.write('\n')
                except Exception as e:
                    print(f"    Error reading or writing file {individual_filepath}: {e}")
        print(f"Successfully created concatenated file: '{output_filepath}'")

if __name__ == "__main__":
    # --- Configuration ---

    # Define the input folders (these are typically outputs from previous processing steps)
    # and their corresponding desired output filenames for the concatenated data.
    # Each tuple: (source_directory_name, target_concatenated_filename).
    CONCATENATION_CONFIGS = [
        ("train_processed_spksegment", "train.txt"),
        ("val_processed_spksegment", "val.txt"),
        ("test_processed_spksegment", "test.txt")
    ]

    # The file pattern to search for within each input directory (e.g., "*.txt" will find all .txt files).
    FILE_PATTERN_TO_CONCATENATE = "*.txt"

    print("Starting script to concatenate files...")
    concatenate_files_in_folders(
        input_folder_configs=CONCATENATION_CONFIGS,
        file_extension=FILE_PATTERN_TO_CONCATENATE
    )
    print("\nScript finished.")