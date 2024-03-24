import hashlib
import json
import base64
import requests

def calculate_checksum(data):
    # Calculate the checksum using the SHA256 algorithm
    checksum = hashlib.sha256(data).hexdigest()
    return checksum

def process_files(json_file_path):
    # Read the JSON file
    with open(json_file_path, "r") as json_file:
        json_data = json.load(json_file)

    # Extract the binary data and checksum for the original file
    original_binary = base64.b64decode(json_data["original_file"]["binary"])
    original_checksum = json_data["original_file"]["checksum"]

    # Extract the binary data and checksum for the attachment file
    attachment_binary = base64.b64decode(json_data["attachment_file"]["binary"])
    attachment_checksum = json_data["attachment_file"]["checksum"]

    # Perform verification and processing operations on the files as needed
    # ...

    # Combine the files (assuming attachment is attached to the PDF)
    combined_data = original_binary + attachment_binary

    # Calculate the checksum of the combined files
    combined_checksum = calculate_checksum(combined_data)

    # Store the information in a new JSON file
    processed_data = {
        "combined_file": {
            "binary": base64.b64encode(combined_data).decode("utf-8"),
            "checksum": combined_checksum
        }
    }

    processed_json_file_path = "/home/shym/Desktop/chaimas2/cc/processFile.json"  # Replace with your desired file path

    with open(processed_json_file_path, "w") as processed_json_file:
        json.dump(processed_data, processed_json_file)

    print("Processed data stored in:", processed_json_file_path)

    # Send the JSON file back to the system or perform further actions
    # ...

# Example usage
json_file_path = "/home/shym/Desktop/chaimas2/cc/output.json"  # Replace with the actual JSON file path

process_files(json_file_path)