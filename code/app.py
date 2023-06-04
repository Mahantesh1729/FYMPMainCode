from face_landmark_detection import generate_face_correspondences
from delaunay_triangulation import make_delaunay
from face_morph import generate_morph_sequence
from flask import Flask, jsonify, request
from flask import send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin


import subprocess
import argparse
import shutil
import os
import cv2

UPLOAD_FOLDER = 'code/upload_folder'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
# @app.route('/', methods = ['GET', 'POST'])
# def home():
# 	if(request.method == 'GET'):

# 		data = "hello world"
# 		return jsonify({'data': data})


# A simple function to calculate the square of a number
# the number to be squared is sent in the URL when we use GET
# on the terminal type: curl http://127.0.0.1:5000 / home / 10
# this returns 100 (square of 10)
# @app.route('/home/<int:num>', methods = ['GET'])
# def disp(num):

# 	return jsonify({'data': num**2})


@app.route('/input/image', methods = ['POST'])

def getImage():
	
	if 'file1' not in request.files:
		return 'there is no sketch1 in form!'
	
	if 'file2' not in request.files:
		return 'there is no sketch2 in form!'

	files = request.files
	flag = 0
	confResult = 0
	path = 0
	resultPath = 0
	file1 = 0
	file2 = 0
	tempConf = 0	
	for i in range(2, len(files) + 1):
		
		if not flag:
			print("in first flag")
			file1 = request.files['file' + str(i - 1)]
		file2 = request.files['file' + str(i)]

		# duration = int(request.form['duration'])
		# frameRate = int(request.form['frameRate'])
		print(file1)
		if not flag:
			path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
			file1.save(path)
		else:
			path = resultPath
		# path='images/aligned_images/jennie.png'
		image1 = cv2.imread(path)
		print(path)
		path = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)
		file2.save(path)
		# path = 'images/aligned_images/rih.png'
		print(path)
		image2 = cv2.imread(path)
		doMorphing(image1, image2, 20,10,'output.mp4')
		path='/home/mahantesh/Mahantesh/notes/sem8/MajorPWP2/MainCode/output.mp4'

		cap = cv2.VideoCapture(path)


		# print("total_frames= ", total_frames)

		confd1 = 0
		confd2 = 0
		
		if not flag:
			confd1 = float(request.form['conf' + str(i - 1)])
			flag = 1
		else:
			confd1 = tempConf
		
		tempConf = confd1 + confd2
		confd2 = float(request.form['conf' + str(i)])

		print("conf1= ", confd1, "conf2= ", confd2)

		confResult = confd2 / (confd1 + confd2)

		print("confResult= ", confResult)

		req_frame = int(confResult * 200)

		print("req_frame= ", req_frame)

		if req_frame == 0 : req_frame = 1

		if req_frame == 200: req_frame = req_frame - 1

		cap.set(cv2.CAP_PROP_POS_FRAMES, req_frame)

		ret, frame = cap.read()
		print(ret)
		cv2.imwrite('/home/mahantesh/Mahantesh/notes/sem8/MajorPWP2/MainCode/middle_frame.jpg', frame)

		path = '/home/mahantesh/Mahantesh/notes/sem8/MajorPWP2/MainCode/middle_frame.jpg'
		resultPath = path
		cap.release()

	return send_file(path, as_attachment=True)

def doMorphing(img1, img2, duration, frame_rate, output):

		[size, img1, img2, points1, points2, list3] = generate_face_correspondences(img1, img2)

		print()
		print("In doMorphing function img1 is ", type(img1))
		print()

		tri = make_delaunay(size[1], size[0], list3, img1, img2)

		generate_morph_sequence(duration, frame_rate, img1, img2, points1, points2, tri, size, output)



def perform():
	def doMorphing(img1, img2, duration, frame_rate, output):

		[size, img1, img2, points1, points2, list3] = generate_face_correspondences(img1, img2)

		tri = make_delaunay(size[1], size[0], list3, img1, img2)

		generate_morph_sequence(duration, frame_rate, img1, img2, points1, points2, tri, size, output)

	if __name__ == "__main__":

		parser = argparse.ArgumentParser()
		parser.add_argument("--img1", required=True, help="The First Image")
		parser.add_argument("--img2", required=True, help="The Second Image")
		parser.add_argument("--duration", type=int, default=5, help="The duration")
		parser.add_argument("--frame", type=int, default=20, help="The frameame Rate")
		parser.add_argument("--output", help="Output Video Path")
		args = parser.parse_args()

		image1 = cv2.imread(args.img1)
		image2 = cv2.imread(args.img2)

		doMorphing(image1, image2, args.duration, args.frame, args.output)
	
#driver function
if __name__ == '__main__':

	cors = CORS(app)
	app.config['CORS_HEADERS'] = 'Content-Type'
	app.run(debug = True)
