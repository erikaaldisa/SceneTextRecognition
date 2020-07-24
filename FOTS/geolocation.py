from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS

# def get_exif(filename):
#     image = Image.open(filename)
#     image.verify()
#     return image._getexif()

# def get_geotagging(exif):
#     if not exif:
#         raise ValueError("No EXIF metadata found")

#     geotagging = {}
#     for (idx, tag) in TAGS.items():
#         if tag == 'GPSInfo':
#             if idx not in exif:
#                 raise ValueError("No EXIF geotagging found")

#             for (key, val) in GPSTAGS.items():
#                 if key in exif[idx]:
#                     geotagging[val] = exif[idx][key]

#     return geotagging


# def get_decimal_from_dms(dms, ref):

#     degrees = dms[0][0] / dms[0][1]
#     minutes = dms[1][0] / dms[1][1] / 60.0
#     seconds = dms[2][0] / dms[2][1] / 3600.0

#     if ref in ['S', 'W']:
#         degrees = -degrees
#         minutes = -minutes
#         seconds = -seconds

#     return round(degrees + minutes + seconds, 5)

# def get_coordinates(geotags):
#     lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

#     lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

#     return (lat,lon)


# exif = get_exif('iphone2.jpg')
# print(exif)
# geotags = get_geotagging(exif)
# print(get_coordinates(geotags))

def get_coordinates(photo):
	image = Image.open(photo)
	image.verify()
	if not image._getexif():
		raise ValueError("No EXIF metadata found")
	
	exif = image._getexif()
	#print(exif)
	geotags = {}
	for (idx, tag) in TAGS.items():
		if tag == 'GPSInfo':
			if idx not in exif:
				raise ValueError("No EXIF geotagging found")

			for (key, val) in GPSTAGS.items():
				if key in exif[idx]:
					geotags[val] = exif[idx][key]
	#print(geotags)
	coordinates=[]

	for i in [[geotags['GPSLatitude'],geotags['GPSLatitudeRef']],[geotags['GPSLongitude'],geotags['GPSLongitudeRef']]]:
		degrees = i[0][0][0] / i[0][0][1]
		minutes = i[0][1][0] / i[0][1][1] / 60.0
		seconds = i[0][2][0] / i[0][2][1] / 3600.0

		if i[1] in ['S', 'W']:
			degrees = -degrees
			minutes = -minutes
			seconds = -seconds

		coordinates.append(round(degrees + minutes + seconds, 5))
	
	return tuple(coordinates)


photo = 'iphone2.JPG'
print(get_coordinates(photo))
print(type(get_coordinates(photo)))