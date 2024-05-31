#insert two files: first is pdf and others are attachments
#verify the integrity of the sent files using checksums (each file has its own checksum) then return the checksum validity
#test your service
#send and return in json format
#cloud database: in-memory

#no pdf regeneration
#add token for auth
#dockerize it
#add a domain name
#add auto-deploy if possible

#install swagger
#create a log file for flask

#add requirements.txt for your service containing python libs



import hashlib
import PyPDF2
from flask import Flask, request, jsonify, send_file, redirect, url_for, render_template
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import DecodedStreamObject, NameObject, DictionaryObject, createStringObject, ArrayObject
import os
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)


SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)



def calculate_file_checksum(file):
    sha256_hash = hashlib.sha256()
    file.seek(0)  # Move to the start of the file
    for byte_block in iter(lambda: file.read(4096), b""):
        sha256_hash.update(byte_block)
    file.seek(0)  # Reset the file pointer to the start
    return sha256_hash.hexdigest()

def rresolve_indirect_object(obj):
    """ Helper function to resolve indirect objects in PyPDF2. """
    while isinstance(obj, PyPDF2.generic.IndirectObject):
        obj = obj.get_object()
    return obj

@app.route('/', methods=['GET'])
def index():
    with open('index.html', 'r') as f:
        html_content = f.read()
    return html_content

@app.route('/attach_files', methods=['GET'])
def attach_index():
    with open('attach_file.html', 'r') as f:
        attach_content = f.read()
    return attach_content

@app.route('/extract_files', methods=['GET'])
def extract_index():
    with open('extract_files.html', 'r') as f:
        extract_content = f.read()
    return extract_content

@app.route('/upload', methods=['POST'])
def handle_upload():
    main_file = request.files['main_file']
    attachments = request.files.getlist('attachments')
    
    client_mf_checksum = request.form['main_file_checksum']
    client_a_checksums = request.form['attachments_checksums'].split(',')
    
    server_mf_checksum = calculate_checksum(main_file)
    server_a_checksums = [calculate_checksum(attachment) for attachment in attachments]
    
    mf_checksum_match = client_mf_checksum == server_mf_checksum
    a_checksums_match = client_a_checksums == server_a_checksums

    main_file_result = {
        "filename": main_file.filename,
        "checksum": server_mf_checksum,
        "verification_status": "valid" if mf_checksum_match else "invalid"
    }

    attachments_results = []
    for attachment, server_checksum, client_checksum in zip(attachments, server_a_checksums, client_a_checksums):
        attachment_result = {
            "filename": attachment.filename,
            "checksum": server_checksum,
            "verification_status": "valid" if server_checksum == client_checksum else "invalid"
        }
        attachments_results.append(attachment_result)
    
    if mf_checksum_match and a_checksums_match:
        # Attach files to the main PDF
        main_pdf_writer = PdfWriter()
        main_pdf_reader = PdfReader(main_file)
        
        for page in main_pdf_reader.pages:
            main_pdf_writer.add_page(page)
        
        for attachment in attachments:
            append_attachment(main_pdf_writer, attachment.filename, attachment.read())
        
        output_pdf_path = "output.pdf"
        with open(output_pdf_path, "wb") as output_pdf_file:
            main_pdf_writer.write(output_pdf_file)
        
        return send_file(output_pdf_path, as_attachment=True)
    else:
        return jsonify({'error': 'Checksum verification failed for main file or attachments!'})
    
@app.route('/extract', methods=['POST'])
def extract_attachments():
    if 'main_file' not in request.files:
        return jsonify({'error': 'No file part in the request'})

    main_file = request.files['main_file'].stream

    output_dir = 'extracted_attachments'

    client_mf_checksum = request.form['main_file_checksum']

    server_mf_checksum = calculate_checksum(main_file)

    mf_checksum_match = client_mf_checksum == server_mf_checksum

    if mf_checksum_match:
        extract_attachments_from_pdf(main_file, output_dir)
        return render_template('success_toast.html', message='Extraction complete.')
    else:
        return render_template('error_toast.html', message='Checksum verification failed for your file!')
    

def extract_attachments_from_main_pdf(input_pdf, output_dir):
    try:
        reader = PyPDF2.PdfReader(input_pdf)
        
        root = resolve_indirect(reader.trailer['/Root'])
        if '/Names' not in root:
            print('No attachments found in the PDF.')
            return

        names = resolve_indirect(root['/Names'])
        if '/EmbeddedFiles' not in names:
            print('No attachments found in the PDF.')
            return
        
        embedded_files = resolve_indirect(names['/EmbeddedFiles'])
        attachments = embedded_files['/Names']
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for i in range(0, len(attachments), 2):
            attachment_name = attachments[i].get_object()
            attachment_file = attachments[i+1].get_object()
            
            file_spec = resolve_indirect(attachment_file)
            file_data = resolve_indirect(file_spec['/EF']['/F']).get_data()

            output_path = os.path.join(output_dir, attachment_name)
            with open(output_path, 'wb') as output_file:
                output_file.write(file_data)
    
    except Exception as e:
        return jsonify({'error': str(e)})


def append_attachment(pdf_writer, fname, fdata):
    # The entry for the file
    file_entry = DecodedStreamObject()
    file_entry.set_data(fdata)
    file_entry.update({NameObject("/Type"): NameObject("/EmbeddedFile")})

    # The Filespec entry
    efEntry = DictionaryObject()
    efEntry.update({ NameObject("/F"): file_entry })

    filespec = DictionaryObject()
    filespec.update({NameObject("/Type"): NameObject("/Filespec"), NameObject("/F"): createStringObject(fname), NameObject("/EF"): efEntry})

    if "/Names" not in pdf_writer._root_object.keys():
        # No files attached yet. Create the entry for the root, as it needs a reference to the Filespec
        embeddedFilesNamesDictionary = DictionaryObject()
        embeddedFilesNamesDictionary.update({NameObject("/Names"): ArrayObject([createStringObject(fname), filespec])})

        embeddedFilesDictionary = DictionaryObject()
        embeddedFilesDictionary.update({NameObject("/EmbeddedFiles"): embeddedFilesNamesDictionary})
        pdf_writer._root_object.update({NameObject("/Names"): embeddedFilesDictionary})
    else:
        # There are files already attached. Append the new file.
        pdf_writer._root_object["/Names"]["/EmbeddedFiles"]["/Names"].append(createStringObject(fname))
        pdf_writer._root_object["/Names"]["/EmbeddedFiles"]["/Names"].append(filespec)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)