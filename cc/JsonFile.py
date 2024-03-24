import hashlib
import json
import base64

def calculate_checksum(file_path):
    # Read the contents of the file in binary mode
    with open(file_path, "rb") as file:
        data = file.read()

    # Calculate the checksum using the SHA256 algorithm
    checksum = hashlib.sha256(data).hexdigest()

    return checksum

def convert_files_to_binary(original_file_path, attachment_file_path, json_file_path):
    # Convert original file to binary
    with open(original_file_path, "rb") as original_file:
        original_binary = original_file.read()

    # Calculate checksum for original file
    original_checksum = calculate_checksum(original_file_path)

    # Convert attachment file to binary
    with open(attachment_file_path, "rb") as attachment_file:
        attachment_binary = attachment_file.read()

    # Calculate checksum for attachment file
    attachment_checksum = calculate_checksum(attachment_file_path)

    # Encode binary data as base64 strings
    original_base64 = base64.b64encode(original_binary).decode("utf-8")
    attachment_base64 = base64.b64encode(attachment_binary).decode("utf-8")

    # Create a dictionary to store the base64 strings and checksum information
    file_data = {
        "original_file": {
            "binary": original_base64,
            "checksum": original_checksum
        },
        "attachment_file": {
            "binary": attachment_base64,
            "checksum": attachment_checksum
        }
    }

    # Write the file data to a JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(file_data, json_file)

    print("Files converted to binary, checksum calculated, and JSON file created.")

# Example usage
original_file_path = "/home/shym/Desktop/chaimas2/saw/SAW-TP1.pdf"
attachment_file_path = "/home/shym/Desktop/chaimas2/ml/markdown/readme.md"
json_file_path = "/home/shym/Desktop/chaimas2/cc/output.json"

convert_files_to_binary(original_file_path, attachment_file_path, json_file_path)







