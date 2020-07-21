# SceneTextRecognition
<img src="https://www.sla.gov.sg/qql/slot/u143/Newsroom/Press%20Releases/2019/SGW2019/GeoWorks.png" style="width:90px;height:41px;margin: 0 0 30px 0;">
Done for <b>GeoAI Internship</b> at GeoWorks, Singapore Land Authority. 

<h2> Three different ways to Detect, Recognize or Spot Scene Text. </h2>
Three Models used: 
<ol>
  <li><a href: "https://www.pyimagesearch.com/2018/09/17/opencv-ocr-and-text-recognition-with-tesseract/" target="_blank">OpenCV OCR</a></li>
  <li>EAST (Tensorflow Implementation)</li>
  <li>FOTS - Fast Oriented Text Spotting with a Unified Network</li>
</ol>

<h3> Usage of OpenCV OCR (Test)</h3>

<h3> Usage of EAST (Test)</h3>

<h3> Usage of FOTS (Test)</h3>

<h2>Final Deliverable: Flask Application </h2>
Features of Flask Application:
<ul>
  <li>FOTS: Spot Scene Text in the picture</li>
  <li>Extract GeoTAGS (GPS Info/Coordinates) of the picture</li>
  <li>OneMAP API: Reverse Geocoding to get Address of the picture</li>
  <li>OneMAP API: Static Map of the Address of the picture</li>
</ul>
In the process of choosing the scene text recognition/spotting model (FOTS), I have chosen some criteria such as:
<ul>
  <li>Implementation uses Tensorflow and Python (familiarity)</li>
  <li>Able to produce rotated bounding boxes</li>
  <li>Able to SPOT scene text, meaning both detect and recognize scene text </li>
  <li>Model able to be trained using ICDAR Datasets</li>
</ul>
