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
    Original speaker sequence: <0, 0, 1, 2, 3, 3, 1>
    Relabeled sequence:        <0, 0, 1, 0, 1, 1, 0> (appended as the new column)

    Args:
        input_base_dirs (list): List of directory names to process (e.g., ['train_processed']).
        output_dir_suffix (str): Suffix to append to input_base_dir names for output.
        file_extension (str): Glob pattern for files.
        delimiter (str): The delimiter used in the files.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))

    for input_dir_name in input_base_dirs:
        input_dir_path = os.path.join(script_dir, input_dir_name)
        # Construct the new output directory name, e.g., "train_processed_spksegment"
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
            original_filename = os.path.basename(input_filepath)
            output_filepath = os.path.join(output_dir_path, original_filename)

            print(f"  Processing '{original_filename}' -> '{output_filepath}'")

            try:
                with open(input_filepath, 'r', encoding='utf-8') as infile, \
                     open(output_filepath, 'w', encoding='utf-8') as outfile:

                    previous_speaker = None
                    # Start with label 0 for the first speaker segment
                    current_alternating_label = 0
                    first_line_in_file = True

                    for line in infile:
                        stripped_line = line.rstrip('\n\r')
                        if not stripped_line: # Skip empty lines if any
                            outfile.write("\n") # Preserve empty lines
                            continue

                        parts = stripped_line.split(delimiter)
                        if not parts or not parts[0]: # Check if first part (speaker) is empty
                            # If line is malformed or speaker ID is missing,
                            # append the current label and log a warning or handle as needed.
                            # For robustness, let's assume it's a continuation of the previous segment
                            # or if it's the first line, it gets the initial label.
                            print(f"    Warning: Malformed line or missing speaker ID in '{original_filename}': '{line.strip()}'."
                                  f" Appending current label: {current_alternating_label}")
                            new_line = f"{stripped_line}{delimiter}{current_alternating_label}\n"
                            outfile.write(new_line)
                            continue

                        current_speaker = parts[0] # Speaker is the first part

                        if first_line_in_file:
                            # The first line establishes the first speaker and gets the initial label (0)
                            # No change in current_alternating_label needed here.
                            first_line_in_file = False
                        elif previous_speaker is not None and current_speaker != previous_speaker:
                            # Speaker has changed, flip the label
                            current_alternating_label = 1 - current_alternating_label # Flips 0 to 1 and 1 to 0
                        # If speaker is the same as previous, current_alternating_label remains unchanged.

                        new_line = f"{stripped_line}{delimiter}{current_alternating_label}\n"
                        outfile.write(new_line)

                        previous_speaker = current_speaker
                print(f"  Successfully created '{output_filepath}'")
            except Exception as e:
                print(f"  Error processing file {input_filepath}: {e}")

if __name__ == "__main__":
    # --- Configuration ---
    # These should be the output directories from the PREVIOUS script
    # (e.g., train_processed, val_processed, test_processed)
    PROCESSED_DIRECTORIES = ['train_processed', 'val_processed', 'test_processed']

    # This will be appended to the names above to create the new output dirs
    # e.g., train_processed_spksegment
    SPEAKER_SEGMENT_OUTPUT_SUFFIX = "_spksegment" # Changed suffix to reflect new meaning

    FILE_PATTERN = "*.txt"
    DATA_DELIMITER = "|"


    print("Starting script to add speaker segment column...")
    add_speaker_change_column(
        input_base_dirs=PROCESSED_DIRECTORIES,
        output_dir_suffix=SPEAKER_SEGMENT_OUTPUT_SUFFIX,
        file_extension=FILE_PATTERN,
        delimiter=DATA_DELIMITER
    )
    print("\nScript finished.")

 