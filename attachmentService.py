from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/attachment", methods=["POST"])
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

    # Do further processing with the JSON file as needed
    # ...

    return jsonify({"message": "Attachment file received and saved successfully."}), 200 