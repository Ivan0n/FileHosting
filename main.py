from flask import Flask, request, jsonify, send_from_directory, render_template
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'public'
ALLOWED_EXTENSIONS = {'html', 'css', 'js', 'png', 'jpg', 'jpeg', 'gif', 'ico', 'svg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            return jsonify(success=False, error='Нет файлов в запросе'), 400

        files = request.files.getlist('files[]')
        if not files:
            return jsonify(success=False, error='Файлы не выбраны'), 400

        saved_files = []

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(save_path)
                saved_files.append(filename)
            else:
                return jsonify(success=False, error=f'Файл "{file.filename}" имеет недопустимый формат'), 400

        return jsonify(success=True, files=saved_files), 200

    return render_template('index.html')

@app.route('/public/<path:filename>')
def serve_public_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=5555, debug=True)
