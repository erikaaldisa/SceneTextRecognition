# SceneTextRecognition
<img src="https://www.sla.gov.sg/qql/slot/u143/Newsroom/Press%20Releases/2019/SGW2019/GeoWorks.png" style="width:90px;height:41px;margin: 0 0 30px 0;">

Done for **GeoAI Internship** at [GeoWorks], Singapore Land Authority. 

[GeoWorks]: https://geoworks.sg/

## Three different ways to Detect, Recognize or Spot Scene Text.
Three Models used: 

1. [OpenCV OCR]
2. [EAST (Tensorflow Implementation)]
3. [FOTS - Fast Oriented Text Spotting with a Unified Network]

> ##### Please check the links for original repository/code. <br> I have made little modifications to all to suit my needs, especially for the FOTS code since it's used for my final deliverable

> ##### Please also check the links for training purposes, as the instructions below only cover testing. :relaxed::relaxed::relaxed:

> ##### Visual Studio Code and WSL Ubuntu were used for this Proof of Concept. :computer:



[OpenCV OCR]: https://www.pyimagesearch.com/2018/09/17/opencv-ocr-and-text-recognition-with-tesseract/
[EAST (Tensorflow Implementation)]: https://github.com/argman/EAST
[FOTS - Fast Oriented Text Spotting with a Unified Network]: https://github.com/Pay20Y/FOTS_TF/tree/dev

:computer::one::computer:

### Usage of OpenCV OCR (Test)
1. Clone GitHub Repository / Download & unzip ZIP file named ‘OpenCV OCR’
2. Activate Virtual Environment and go to the directory where the OpenCV OCR folder is
3. Install the required dependencies (requirements.txt)
<pre><code>pip install -r requirements.txt
</code></pre>

4. Download the EAST text detection pb file and put it in the same folder as the py file.
> Download the pb file from this [link]
5. Initiate [Xming] (to enable SSH X11 Forwarding), if you are using WSL Ubuntu also.
6. Run the command
<pre><code>python3 text_recognition_test.py --east frozen_east_text_detection.pb --image images/img6.jpg
</code></pre> 

[Xming]: https://microcollaborative.atlassian.net/wiki/spaces/DSC/pages/167084120/X11+with+Windows+Subsystem+for+Linux
[link]: https://www.pyimagesearch.com/2018/09/17/opencv-ocr-and-text-recognition-with-tesseract/

:computer::two::computer:

### Usage of EAST (Test)
1. Clone GitHub Repository / Download & unzip ZIP file named ‘EAST’
2. Activate Virtual Environment and go to the directory where the EAST is
3. Install the required dependencies (requirements_venv.txt)
<pre><code>pip install -r requirements_venv.txt
</code></pre>

4. Download the pre-trained models and put it into a folder with the name of the checkpoint_path
> * [Models trained on ICDAR 2013 + ICDAR 2015 training data]
> * [Resnet V1 50 provided by tensorflow slim]
5. Run the command
<pre><code>python eval.py --test_data_path=images_test/ --gpu_list=0 --checkpoint_path=east_icdar2015_resnet_v1_50_rbox/ \--output_dir=result/ 
</code></pre> 

[Models trained on ICDAR 2013 + ICDAR 2015 training data]: https://drive.google.com/file/d/0B3APw5BZJ67ETHNPaU9xUkVoV0U/view
[Resnet V1 50 provided by tensorflow slim]: http://download.tensorflow.org/models/resnet_v1_50_2016_08_28.tar.gz

:computer::three::computer:

### Usage of FOTS (Test)
1. Clone GitHub Repository / Download & unzip ZIP file named ‘FOTS’
2. Activate Virtual Environment and go to the directory where the FOTS is
3. Install the required dependencies (requirements_FOTS.txt)
<pre><code>pip install -r requirements_FOTS.txt
</code></pre>

4. Download the pre-trained model and put it into a folder with the name of the checkpoint_path
> * [SynthText 6-epochs pre-trained model]
5. Run the command
<pre><code>python3 main_test.py --gpu_list='0' --test_data_path=images_test/ --checkpoint_path=checkpoints/
</code></pre> 

[SynthText 6-epochs pre-trained model]: https://github.com/Pay20Y/FOTS_TF/releases/download/v2/SynthText_6_epochs.tar


## Final Deliverable: Flask Application 
Features of Flask Application:

* FOTS: Spot Scene Text in the picture
* Extract GeoTAGS (GPS Info/Coordinates) of the picture
* [OneMap API]: Reverse Geocoding to get Address of the picture
* [OneMap API]: Static Map of the Address of the picture

[OneMap API]: https://docs.onemap.sg/

In the process of choosing the scene text recognition/spotting model (FOTS), I have chosen some criteria such as:

* Implementation uses Tensorflow and Python (familiarity)
* Able to produce rotated bounding boxes
* Able to SPOT scene text, meaning both detect and recognize scene text
* Model able to be trained using ICDAR Datasets


### Usage 
1. Usage is the same as Usage of FOTS (Test)
2. Run the command
<pre><code>python3 app_geo.py
</code></pre> 

### Output

![FlaskApp](https://github.com/erikaaldisa/SceneTextRecognition/blob/master/FOTS/FlaskAppScreenshot.png?raw=true)


> Thank you to the team at GeoWorks!
