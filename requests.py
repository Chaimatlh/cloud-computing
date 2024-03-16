import requests

def upload_file_to_service(file_path, service_url):
    # Open the file in binary mode
    with open(file_path, "rb") as file:
        # Create a dictionary for the file attachment
        files = {"attachment": file}

        # Send the POST request with the file attached
        response = requests.post(service_url, files=files)

        # Check the response status code
        if response.status_code == 200:
            print("File uploaded successfully.")
        else:
            print("File upload failed.")

# Example usage
file_path = "/home/shym/Desktop/chaimas2/cc/output.json"
service_url = "http://localhost:5000/attachment"

upload_file_to_service(file_path, service_url)