import requests

def send_files(original_file_path, attachment_file_path, url):
    # Create a dictionary to hold the files
    files = {
        'original_file': open(original_file_path, 'rb'),
        'attachment_file': open(attachment_file_path, 'rb')
    }

    try:
        # Send the files as a POST request to the specified URL
        response = requests.post(url, files=files, verify=True)  # Set verify=True for SSL/TLS verification

        # Check the response status code
        if response.status_code == requests.codes.ok:
            print("Files sent successfully!")
        else:
            print("Failed to send the files. Status code:", response.status_code)

    except requests.exceptions.RequestException as e:
        print("An error occurred while sending the files:", str(e))

    finally:
        # Close the file handles
        for file in files.values():
            file.close()

# Example usage
original_file_path = '/home/shym/Desktop/chaimas2/saw/SAW-TP1.pdf'
attachment_file_path = '/home/shym/Desktop/chaimas2/ml/markdown/readme.md'
url = 'https://example.com/upload'  # Replace with the actual URL

send_files(original_file_path, attachment_file_path, url)
# The code you provided is a Python function named send_files that 
# sends two files (original_file and attachment_file) as a POST request to a specified URL using the requests library.