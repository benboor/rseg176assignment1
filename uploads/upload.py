
from flask import Flask, render_template, request, jsonify #, Markup
from flask_uploads import UploadSet, configure_uploads, IMAGES
import boto3
import os

#flask housekeeping
app = Flask(__name__)

#setting a place for 
photos = UploadSet('photos', IMAGES)

#connecting to s3
s3 = boto3.client('s3')

#some housekeeping...
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
	if request.method == 'POST' and 'photo' in request.files:

		#the famous person to look for
		personNameRaw = request.form['personName']
		personName = personNameRaw.upper() 
	
		#the user provided phot
		fileRaw  = request.files['photo']					
		fileRaw.filename =  "upload.png" 
		filename = photos.save(fileRaw)				
		
		#Handling errors with a try
		try:
		
			#sending the data to s3...	
			imageData = open('C:/Users/Administrator/Documents/assignment1/rseg176assignment1/uploads/static/img/' + "upload.png", 'rb') 
			s3.put_object(Bucket='resg176harrybenbucket', Key="upload.png", Body=imageData) #Key='robotImg.png', Body=data)				
			
			##using the rekognition api...
			fileName='upload.png'
			bucket='resg176harrybenbucket'
			client=boto3.client('rekognition')
			
			#for objects
			objectResponseDict = client.detect_labels(Image={'S3Object':{
															'Bucket':bucket,
															'Name':fileName}
														})

			#for facial emotions											
			facialEmotionResponseDict = client.detect_faces(Image={'S3Object':{
															'Bucket':bucket,
															'Name':fileName}
														})									
									
									
														
			#passing the output of the rekognition API to a user readable list for ouput
			objectResponseList = []
			facialEmotionResponseList = []
			
			
			for x in objectResponseDict['Labels']:
				objectResponseList.append("Object name:" + x['Name'] + " Confidence in name:" + str(x['Confidence']))

			facialEmotionResponseList.append("facial details are :" + str(facialEmotionResponseDict['FaceDetails']))

			#casting strings to lists for output
			prePersonTestOutput = str(objectResponseList)
			preEmotionTestOutput = str(facialEmotionResponseList)
				
				
			#sanetizing the upload folder for future use...
			del(imageData)
			os.remove('C:/Users/Administrator/Documents/assignment1/rseg176assignment1/uploads/static/img/upload.png')
			
			
			#testing for person name in objects...
			if personName in prePersonTestOutput :
				output = str(personName) + " was present in the image along with " + prePersonTestOutput + "\n they are" + preEmotionTestOutput

			if personName not in prePersonTestOutput :
				output = str(personName) + " was not present in the image. But, " + prePersonTestOutput + " was. They are" + preEmotionTestOutput

				
			
			return output
		
		except:
			return 'Error in processing image. Confirm that image is of .PNG and try again. If failure continues contact development team'
		
		return  output 		
	
	
	return render_template('upload.html')
	
if __name__ == '__main__':
	app.run(debug=True)
