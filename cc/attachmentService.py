from flask import Flask, request, jsonify #web framework like Flask in Python is a server 

app = Flask(__name__)

@app.route("/attachment", methods=["POST"]) # attachment it's the endpoint
def process_attachment():
    # Check if a file is included in the request
    if "attachment" not in request.files:
        return jsonify({"error": "No attachment file provided."}), 400

    attachment_file = request.files["attachment"]

    # Check if the file is a JSON file
    if not attachment_file.filename.endswith(".json"):
        return jsonify({"error": "Invalid file format. Only JSON files are allowed."}), 400

    # Save the file
    attachment_file.save("output.json")

    return jsonify({"message": "Attachment file received and saved successfully."}), 200 
    #uploads a file to a specified service URL using the requests library.


    # Additional processing to combine the files
    combined_data = {}

    # Read the uploaded file
    with open("output.json", "r") as file:
        uploaded_data = json.load(file)
        combined_data["uploaded_data"] = uploaded_data

    # Combine with other data or perform any necessary operations
    # ...

    # Save the combined data to a new file
    combined_file_path = "combined_output.json"
    with open(combined_file_path, "w") as file:
        json.dump(combined_data, file)
      

    # Remove the temporary uploaded file
    os.remove("output.json")

    # Return the combined file as the response
    return send_file(combined_file_path, as_attachment=True)

    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)