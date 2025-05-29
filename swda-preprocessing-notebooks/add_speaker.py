import os
import glob

def add_speaker_change_column(
    input_base_dirs, # e.g., ['train_processed', 'val_processed', 'test_processed']
    output_dir_suffix="_spksegment", # New suffix for the output directories
    file_extension="*.txt",
    delimiter="|"
):
    """
    Adds a speaker segment indicator column (0 or 1, flipping on speaker change) to files.
    Reads from input_base_dirs and writes to new directories with output_dir_suffix.

    Example:
    Original speaker sequence (first column): <0, 0, 1, 2, 3, 3, 1>
    New appended column:                       <0, 0, 1, 0, 1, 1, 0>

    Args:
        input_base_dirs (list): List of directory names to process (e.g., ['train_processed']).
        output_dir_suffix (str): Suffix to append to input_base_dir names for output.
        file_extension (str): Glob pattern for files.
        delimiter (str): The delimiter used in the files.
    """
    # Get the script's directory for resolving relative paths.
    script_dir = os.path.dirname(os.path.abspath(__file__))

    for input_dir_name in input_base_dirs:
        # Construct full paths for input and new output directories.
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
            original_filename = os.path.basename(input_filepath)
            output_filepath = os.path.join(output_dir_path, original_filename)

            print(f"  Processing '{original_filename}' -> '{output_filepath}'")

            try:
                # Open input and output files.
                with open(input_filepath, 'r', encoding='utf-8') as infile, \
                     open(output_filepath, 'w', encoding='utf-8') as outfile:

                    previous_speaker = None
                    current_alternating_label = 0 # Start with 0 for the first segment
                    first_line_in_file = True

                    for line in infile:
                        stripped_line = line.rstrip('\n\r')
                        if not stripped_line: # Preserve empty lines
                            outfile.write("\n")
                            continue

                        parts = stripped_line.split(delimiter)
                        # Check for malformed lines or missing speaker ID (first part).
                        if not parts or not parts[0]:
                            print(f"    Warning: Malformed line or missing speaker ID in '{original_filename}': '{line.strip()}'."
                                  f" Appending current label: {current_alternating_label}")
                            new_line = f"{stripped_line}{delimiter}{current_alternating_label}\n"
                            outfile.write(new_line)
                            continue

                        current_speaker = parts[0] # Assume speaker ID is the first column

                        if first_line_in_file:
                            first_line_in_file = False # Mark that the first line has been processed
                        elif previous_speaker is not None and current_speaker != previous_speaker:
                            # If speaker changed, flip the label (0 to 1, 1 to 0).
                            current_alternating_label = 1 - current_alternating_label
                        # If speaker is the same, label remains unchanged.

                        new_line = f"{stripped_line}{delimiter}{current_alternating_label}\n"
                        outfile.write(new_line)

                        previous_speaker = current_speaker # Update for the next line
                print(f"  Successfully created '{output_filepath}'")
            except Exception as e:
                print(f"  Error processing file {input_filepath}: {e}")

if __name__ == "__main__":
    # --- Configuration ---
    # Input directories, typically outputs from a previous processing step.
    PROCESSED_DIRECTORIES = ['train_processed', 'val_processed', 'test_processed']

    # Suffix for the new output directories (e.g., 'train_processed_spksegment').
    SPEAKER_SEGMENT_OUTPUT_SUFFIX = "_spksegment"

    # File pattern to search for.
    FILE_PATTERN = "*.txt"
    # Delimiter used in the data.
    DATA_DELIMITER = "|"

    print("Starting script to add speaker segment column...")
    add_speaker_change_column(
        input_base_dirs=PROCESSED_DIRECTORIES,
        output_dir_suffix=SPEAKER_SEGMENT_OUTPUT_SUFFIX,
        file_extension=FILE_PATTERN,
        delimiter=DATA_DELIMITER
    )
    print("\nScript finished.")