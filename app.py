import os
import shutil
from path import Path
from zipfile import ZipFile
from flask import Flask, render_template, request, flash, send_from_directory, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from chardet import detect

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_PATH'] = 'uploads/'
project_dir = os.path.dirname(os.path.abspath(__file__))

''' Routes/views | Main Application Stuff '''

vidFiles = []


@app.route('/download')
def download():
	return send_from_directory(app.config['UPLOAD_PATH'], 'subtitles_renamed.zip', as_attachment=True, attachment_filename='subtitles_renamed.zip')


@app.route('/receiver', methods=['POST'])  # AJAX receiver route
def get_data():
	data = request.get_json()
	global vidFiles
	vidFiles = data['data']
	return jsonify({'status': 'okay'}), 200


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'subFiles' not in request.files:
			flash('No file part', 'danger')
			return redirect(request.url)
		subFiles = []
		for f in request.files.getlist('subFiles'):
			filename = secure_filename(f.filename.split('/')[1])
			f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
			subFiles.append(filename)
		sub_language = '.ar'
		sub_format = os.path.splitext(subFiles[0])[1]
		global vidFiles
		rename_files(vidFiles, subFiles, sub_language, sub_format)
		return render_template('home2.html', subFiles=subFiles, sub_language=sub_language, vidFiles=vidFiles)
	try:
		os.mkdir(app.config['UPLOAD_PATH'])
	except FileExistsError:
		shutil.rmtree(app.config['UPLOAD_PATH'], ignore_errors=True)
		os.mkdir(app.config['UPLOAD_PATH'])
	return render_template('home.html')


def get_encoding_type(file):
	with open(file, 'rb') as f:
		raw_data = f.read()
	return detect(raw_data)['encoding']


def rename_files(vidFiles, subFiles, sub_language, sub_format):
	vidFiles.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
	subFiles.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
	with Path(os.path.join(project_dir, app.config['UPLOAD_PATH'])):
		for i, vname in enumerate(vidFiles):
			os.rename(subFiles[i], os.path.splitext(vname)[0] + sub_language + sub_format)
		files = os.listdir('.')
		with ZipFile('subtitles_renamed.zip', 'w') as zip:
			for file in files:
				fileCodec = get_encoding_type(file)
				try:
					with open(file, 'r', encoding=fileCodec) as f, open("utf8" + file, 'w', encoding='utf-8') as e:
						text = f.read()
						e.write(text)
					zip.write("utf8" + file, file)
				except UnicodeDecodeError:
					print('Decode Error')
		for file in files:
			os.remove("utf8" + file)
			os.remove(file)
	return redirect(url_for('download'))


if __name__ == "__main__":
	app.run(debug=False)
