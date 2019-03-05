import os
from flask import Flask, request, make_response, jsonify, send_file
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

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            objdec.get_result(app.config['UPLOAD_FOLDER'], filename)
            img = open(os.path.join(SEND_FOLDER, filename), 'rb')
            # os.remove(os.path.join(SEND_FOLDER, filename))
            return send_file(img, mimetype='image/jpg', as_attachment=True, attachment_filename=filename + '_.jpg')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
