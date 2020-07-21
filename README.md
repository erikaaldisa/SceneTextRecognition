# SceneTextRecognition
<img src="https://www.sla.gov.sg/qql/slot/u143/Newsroom/Press%20Releases/2019/SGW2019/GeoWorks.png" style="width:90px;height:41px;margin: 0 0 30px 0;">
Done for **GeoAI Internship** at GeoWorks, Singapore Land Authority. 
## Three different ways to Detect, Recognize or Spot Scene Text.
<br>
Three Models used: 

1. [OpenCV OCR]
2. [EAST (Tensorflow Implementation)]
3. [FOTS - Fast Oriented Text Spotting with a Unified Network]

##### Please check the links for original repository/code. <br> I have made little modifications to all to suit my needs, especially for the FOTS code since it's used for my final deliverable

[OpenCV OCR]: https://www.pyimagesearch.com/2018/09/17/opencv-ocr-and-text-recognition-with-tesseract/
[EAST (Tensorflow Implementation)]: https://github.com/argman/EAST
[FOTS - Fast Oriented Text Spotting with a Unified Network]: https://github.com/Pay20Y/FOTS_TF/tree/dev

### Usage of OpenCV OCR (Test)

### Usage of EAST (Test)

### Usage of FOTS (Test)

## Final Deliverable: Flask Application 
Features of Flask Application:

* FOTS: Spot Scene Text in the picture
* Extract GeoTAGS (GPS Info/Coordinates) of the picture
* OneMAP API: Reverse Geocoding to get Address of the picture
* OneMAP API: Static Map of the Address of the picture

In the process of choosing the scene text recognition/spotting model (FOTS), I have chosen some criteria such as:

* Implementation uses Tensorflow and Python (familiarity)
* Able to produce rotated bounding boxes
* Able to SPOT scene text, meaning both detect and recognize scene text
* Model able to be trained using ICDAR Datasets
