
###############
#Documentation#
###############
#pip install flask
#pip install flask_uploads
#how to start flask app.. 
#cd C:\Users\Administrator\Documents\flaskApp\uploads
# set FLASK_APP=upload.py
# flask run

from flask import Flask, render_template, request, Markup
from flask_uploads import UploadSet, configure_uploads, IMAGES
import boto3
#import os.path # for filename splitting

app = Flask(__name__)

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
			
		fileRaw.filename =  "upload.png" #+ fileRawExtension
		filename = photos.save(fileRaw)		
		return filename			
	
	#sending the data to s3...	
	data = open('C:/Users/Administrator/Documents/flaskApp/uploads/static/img/' + "upload.png", 'rb') 
	s3 = boto3.client('s3')
	s3.put_object(Bucket='rseg176harryben', Key="upload.png", Body=data) #Key='robotImg.png', Body=data)				
	
	##using the rekognition api...
	fileName='upload.png'
	bucket='rseg176harryben'
	client=boto3.client('rekognition')
	response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':fileName}})
	message = Markup("<h1>Voila! Platform is ready to used</h1>")
	flask(message)
	# print('Detected labels for ' + fileName)    
	#	for label in response['Labels']:
	#		print (label['Name'] + ' : ' + str(label['Confidence']))
	
	##delete the file from s3 so the bucket doesn't fill up 	
	#https://stackoverflow.com/questions/3140779/how-to-delete-files-from-amazon-s3-bucket/38883182
	#s3.Object(Bucket='rseg176harryben', Key="upload.png").delete()
	#s3.delete_object.(Bucket='rseg176harryben', Key="upload.png")
	
	return render_template('upload.html')
	
if __name__ == '__main__':
	app.run(debug=True)
	
	

#send to bucket
#this is it...
#	data = open('robotImg.png', 'rb')
#	s3 = boto3.client('s3')
#	s3.put_object(Bucket='rseg176harryben', Key='robotImg.png', Body=data)
	
#use rekognition	
'''
fileName='robotImg.png'
bucket='rseg176harryben'
client=boto3.client('rekognition')
response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':fileName}})
 print('Detected labels for ' + fileName)    
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))
'''	