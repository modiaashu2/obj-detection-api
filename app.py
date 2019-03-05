import os
from flask import Flask, request, make_response, jsonify, send_file, Response
from werkzeug.utils import secure_filename
from object_detection import objdec
from flask_cors import CORS

UPLOAD_FOLDER = 'uploads'
SEND_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/<path:path>')
def static_file(path):
	return app.send_static_file(path)

@app.route('/detect', methods=['POST'])
def detect():
    print("hi1")
    if request.method == 'POST':
        if 'file' not in request.files:
            return make_response(jsonify({"message": "No file uploaded"})), 400

        file = request.files['file']
        print(file)
        
        if "." not in file.filename:
            file.filename = file.filename + ".jpg"

        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            objdec.get_result(app.config['UPLOAD_FOLDER'], filename)
            print("Opening image")
            img = open(os.path.join(SEND_FOLDER, filename), 'rb')
            print("Opened ", filename)
            a_name = filename.split(".")[0] + ".jpg"
            # os.remove(os.path.join(SEND_FOLDER, filename))
            resp = Response("Yoohoo")
            resp.headers["imgname"] = filename
            return resp, 200
        else:
            return make_response(jsonify({"message": "File not found"})), 400

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
