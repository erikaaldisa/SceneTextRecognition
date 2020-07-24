from flask import Flask, flash, request, render_template, url_for, redirect, send_file, send_from_directory
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
from werkzeug.utils import secure_filename
import requests
import os

app = Flask(__name__) #, template_folder='templates', static_folder='static')

#configurations
UPLOAD_FOLDER = "./app_storage"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# OneMap API access token expires every 3 days, so ensure you register for a new one with your email
access_token= "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjUxOTMsInVzZXJfaWQiOjUxOTMsImVtYWlsIjoiZXJpa2FhbGRpc2EuMjAxOEBzaXMuc211LmVkdS5zZyIsImZvcmV2ZXIiOmZhbHNlLCJpc3MiOiJodHRwOlwvXC9vbTIuZGZlLm9uZW1hcC5zZ1wvYXBpXC92MlwvdXNlclwvc2Vzc2lvbiIsImlhdCI6MTU5NTQzOTYxNiwiZXhwIjoxNTk1ODcxNjE2LCJuYmYiOjE1OTU0Mzk2MTYsImp0aSI6ImM4YmI0NGI3YWEwNmYwZGFlMDEyOThmOTJlMjEzODc0In0.f2Kb-OZAgXbTqrvQSS0JyGO4w17F-K1NZa0heXSpd7Q"
base_url = 'https://developers.onemap.sg/privateapi/commonsvc/revgeocode'
staticmap_url = 'https://developers.onemap.sg/commonapi/staticmap/getStaticImage'

def revgeocode(location, token):
	param ={'location':location, 'token':access_token}
	r= requests.get(base_url,params= param)
	if r.status_code == 200: 
		return r.json()
	else:
		return None 

def staticmap(layerchosen, lat, lng, postal, zoom, width, height, points):
	layerchosen = 'night'
	param ={'layerchosen': layerchosen, 'lat':lat, 'lng':lng, 'postal': postal, 'zoom':zoom, 'width': width, 'height':height}
	param_string = "&".join("%s=%s" % (k,v) for k,v in param.items())
	url = staticmap_url+'?'+ param_string 
	r= requests.get(url)
	if r.status_code == 200: 
		print(r.url +'&points=' + points)
		# https://developers.onemap.sg/commonapi/staticmap/getStaticImage?
		# layerchosen=night&lat=1.286&lng=103.860&postal=018972&zoom=17&width=400&height=400&points=[1.286,103.860,"255,255,5","A"]
		return (r.url +'&points=' + points)
	else:
		return None 



def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_coordinates(photo):
	image = Image.open(photo)
	#print(photo.filename) iphone2.JPG
	image.verify()
	if not image._getexif():
		return (ValueError("No EXIF metadata found"))
		# raise ValueError("No EXIF metadata found")

	exif = image._getexif()
	#print(exif)
	geotags = {}
	for (idx, tag) in TAGS.items():
		if tag == 'GPSInfo':
			if idx not in exif:
				return (ValueError("No EXIF geotagging found"))
				# raise ValueError("No EXIF geotagging found")

			for (key, val) in GPSTAGS.items():
				if key in exif[idx]:
					geotags[val] = exif[idx][key]
	coordinates=[]

	for i in [[geotags['GPSLatitude'],geotags['GPSLatitudeRef']],[geotags['GPSLongitude'],geotags['GPSLongitudeRef']]]:
		degrees = i[0][0][0] / i[0][0][1]
		minutes = i[0][1][0] / i[0][1][1] / 60.0
		seconds = i[0][2][0] / i[0][2][1] / 3600.0

		if i[1] in ['S', 'W']:
			degrees = -degrees
			minutes = -minutes
			seconds = -seconds

		coordinates.append(round(degrees + minutes + seconds, 3))
	return tuple(coordinates)


@app.route('/')
def home():
#    return ('Home page')
   return render_template('new_home.html')


@app.route('/spottext/', methods=['POST','GET'])
def uploader():
	if request.method == 'GET':
   		return render_template('new_uploader.html')
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		os.makedirs('app_storage', exist_ok=True)
		photo = request.files['file']
		# print('photo', photo)  #photo <FileStorage: 'iphone4.JPG' ('image/jpeg')>
		if photo.filename == '':
			flash('No selected file')
			return redirect(request.url)
		# print(type(photo)) --> <class 'werkzeug.datastructures.FileStorage'>
		 
		
		# CALLS THE FUNCTION FOR EXTRACTING COORDINATES + FUNCTION FOR TEXT SPOTTING
		if photo and allowed_file(photo.filename): 
			result ={}
			try:
				import app_fots
				text = app_fots.main(photo) #will save photo in the app_storage folder and return detected text in list form 
				# photo.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(photo.filename)))
				#print(photo) <FileStorage: 'iphone2.JPG' ('image/jpeg')>

				img_path = secure_filename(photo.filename)
				# print('img_path', img_path)

				coordinates = str(get_coordinates(photo))	
				result['text'] = text
				result['coordinates'] = coordinates
				layerchosen = 'night'
				zoom = 17
				width = 400 
				height = 400
				
				location = (coordinates[1:-1].replace(" ", ""))
				# print(location, type(location))
				token = access_token
				# print(token, type(token))
				output = revgeocode(location, token) #gives r.json()
				print('output',output)

				if (output == None):
					result['address'] = 'Address Not Found, Please renew your OneMap API Token'
					global map
					map = None
						
				elif ("EXIF" not in coordinates) and (output['GeocodeInfo'] != []):
					lat = coordinates[1:-1].split(',')[0].strip()
					print('lat', lat)
					lng = coordinates[1:-1].split(',')[1].strip()
					print('lng', lng)
					result['address'] = output['GeocodeInfo'][0]['BUILDINGNAME'] + ', ' + output['GeocodeInfo'][0]['BLOCK'] + ' ' + output['GeocodeInfo'][0]['ROAD'] + ', Singapore ' + output['GeocodeInfo'][0]['POSTALCODE']
					result['address'] = result['address'].lower().title()
					postal = output['GeocodeInfo'][0]['POSTALCODE']
					print('postal', postal)
					points ='[{},{},"255,255,5","A"]'.format(lat,lng)
					print('point', points)
					map = staticmap(layerchosen, lat, lng, postal, zoom, width, height, points)
						

				else:
					result['address'] = 'Address Not Found'
					map = None

			except Exception as e:
				return ("error: " + str(e))


	return render_template('new_displayer.html', result=result, staticmap = map, img_path=img_path)

@app.route('/spottext/<filename>')
def download_file(filename):
	filename = filename
	# print('filename', filename)
	return send_from_directory(UPLOAD_FOLDER, filename)#, as_attachment=True)		


if __name__ == '__main__':
   app.run(debug = True)

