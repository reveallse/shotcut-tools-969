import os
import xml.etree.ElementTree as ET
import argparse
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def rename_clips(project_file, naming_pattern):
    """
    Renames video clips in the Shotcut project file based on a naming pattern.
    
    Args:
        project_file (str): Path to the Shotcut project file (.mlt).
        naming_pattern (str): The pattern to rename clips (e.g. 'Clip_{index}').
    """
    try:
        # Load the MLT project file
        tree = ET.parse(project_file)
        root = tree.getroot()

        # Find all clips in the project - filter for actual video clips
        clips = root.findall('.//producer[@id]')
        for index, clip in enumerate(clips):
            # Get the current clip name with null check
            old_name = clip.get('id') or 'unnamed'
            # Create new name using the provided pattern
            new_name = naming_pattern.format(index=index + 1)  # Start index from 1
            clip.set('id', new_name)
            logging.info(f'Renamed clip: {old_name} to {new_name}')

        # Save the modified project file
        tree.write(project_file, encoding='utf-8', xml_declaration=True)
        logging.info(f'Successfully updated the project file: {project_file}')

    except ET.ParseError as e:
        logging.error(f'Error parsing the project file: {e}')
    except FileNotFoundError:
        logging.error(f'The project file was not found: {project_file}')
    except Exception as e:
        logging.error(f'An error occurred: {e}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rename video clips in a Shotcut project.')
    parser.add_argument('project_file', type=str, help='Path to the Shotcut project file (.mlt)')
    parser.add_argument('naming_pattern', type=str, help='Pattern for renaming clips (e.g. "Clip_{index}")')
    
    args = parser.parse_args()
    
    rename_clips(args.project_file, args.naming_pattern)

# TODO: Add more robust error handling for edge cases.
# TODO: Implement a backup feature for original project files before renaming.
