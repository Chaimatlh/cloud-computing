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
        
        # Print the response content
        print(response.text)
# Example usage
file_path = "/home/shym/Desktop/chaimas2/cc/output.json"
service_url = "http://0.0.0.0:8000/attachment" # url of our flask service 

upload_file_to_service(file_path, service_url)
#To upload the output.json file to the Flask service as an input, 
# you can use the requests library in Python to send a POST request with the file attached




# the my_requests.py(client side ) code sends the file to the Flask service using the upload_file_to_service() function. 

#The code opens the file in binary mode and creates a dictionary with the file attached
# using the files parameter in the requests.post() function. It then sends a 
# POST request to the specified service_url with the file attached.