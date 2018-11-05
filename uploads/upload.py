
###############
#Documentation#
###############
#pip install flask
#pip install flask_uploads
#how to start flask app.. 
#cd C:\Users\Administrator\Documents\flaskApp\uploads
# set FLASK_APP=upload.py
# flask run

from flask import Flask, render_template, request, jsonify #, Markup
from flask_uploads import UploadSet, configure_uploads, IMAGES
import boto3
import os #for file management
#from rekognitionLabels import labels #class for outputting json labels...
#import os.path # for filename splitting

#flask housekeeping
app = Flask(__name__)

#setting a place for 
photos = UploadSet('photos', IMAGES)

#connecting to s3
s3 = boto3.client('s3')


app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
	if request.method == 'POST' and 'photo' in request.files:

	
		fileRaw  = request.files['photo']		
		#fileRawNameString = os.path.splitext(fileRaw)[0]
		#fileRawExtension = request.files['photo'].split(".")[-1] #os.path.splitext(fileRaw)[1]		
			
		fileRaw.filename =  "upload.png" 
		filename = photos.save(fileRaw)				
		
		try:
		
			#sending the data to s3...	
			imageData = open('C:/Users/Administrator/Documents/flaskApp/uploads/static/img/' + "upload.png", 'rb') 
			s3.put_object(Bucket='rseg176harryben', Key="upload.png", Body=imageData) #Key='robotImg.png', Body=data)				
			
			##using the rekognition api...
			fileName='upload.png'
			bucket='rseg176harryben'
			client=boto3.client('rekognition')
			responseDict = client.detect_labels(Image={'S3Object':{
															'Bucket':bucket,
															'Name':fileName}
														})

			#passing the output of the rekognition API to a user readable list for ouput
			responseList = []
			
			for x in responseDict['Labels']:
				responseList.append("Object name:" + x['Name'] + " Confidence in name:" + str(x['Confidence']))

			#sanetizing the upload folder for future use...
			del(imageData)
			os.remove('C:/Users/Administrator/Documents/flaskApp/uploads/static/img/upload.png')
				
			return str("\n".join(responseList)) 
		
		except:
			return 'Error in processing image. Confirm that image is of .PNG and try again. If failure continues contact development team'
		
		return str("\n".join(responseList))			
	
	
	return render_template('upload.html')
	
if __name__ == '__main__':
	app.run(debug=True)
