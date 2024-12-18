import os
import json
import re


def to_camel_case(file_name: str) -> str:
    """
    Convert a file name into a simplified camelCase format.

    :param file_name: The original file name
    :return: A simplified camelCase string
    """
    # Remove extension and split by non-alphanumeric characters or spaces
    name_without_ext = os.path.splitext(file_name)[0]
    words = re.split(r"[^a-zA-Z0-9]+", name_without_ext)

    # Convert to camelCase
    camel_case = words[0].lower() + "".join(word.capitalize() for word in words[1:])
    return camel_case


def ensure_unique_key(existing_keys: set, proposed_key: str) -> str:
    """
    Ensure the key is unique by appending a numeric prefix if there's a collision.

    :param existing_keys: A set of already used keys
    :param proposed_key: The proposed key to check for uniqueness
    :return: A unique key
    """
    if proposed_key not in existing_keys:
        existing_keys.add(proposed_key)
        return proposed_key

    # If a collision occurs, append a numeric prefix
    counter = 1
    unique_key = f"{proposed_key}{counter}"
    while unique_key in existing_keys:
        counter += 1
        unique_key = f"{proposed_key}{counter}"

    existing_keys.add(unique_key)
    return unique_key


def generate_json_from_files(folder_path: str, base_url: str, output_file: str) -> None:
    """
    Generate a JSON array from files in a folder and save it to a file.

    :param folder_path: Path to the folder containing files
    :param base_url: Base URL for the 'value' field
    :param output_file: Path to save the generated JSON
    """
    json_data = []
    existing_keys = set()  # Track used keys to ensure uniqueness

    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            # Remove extension for 'name' field
            name_without_ext = os.path.splitext(file_name)[0]

            # Generate simplified camelCase key
            proposed_key = to_camel_case(file_name)
            unique_key = ensure_unique_key(existing_keys, proposed_key)

            # Prepare JSON object
            file_obj = {
                "key": unique_key,
                "name": name_without_ext,
                "url": f"{base_url}/{file_name.replace(' ', '%20')}",  # Handle spaces in URL
            }
            json_data.append(file_obj)

    # Save JSON data to a file
    with open(output_file, "w") as f:
        json.dump(json_data, f, indent=4)

    print(f"JSON file generated successfully: {output_file}")


# Example usage
if __name__ == "__main__":
    FOLDER_PATH = "./fonts"  # Replace with your folder path
    BASE_URL = "https://raw.githubusercontent.com/Pixro-ai/banner-fonts/main/fonts"
    OUTPUT_FILE = "fonts.json"

    generate_json_from_files(FOLDER_PATH, BASE_URL, OUTPUT_FILE)
