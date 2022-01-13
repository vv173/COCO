__COCO-Dataset-Parsing__ 🥥

The code downloads a zip archive containing a COCO dataset. It will unpack the archive and use the pandas package to convert data to the data frame, additionally converting it to csv files. 
You can run this program by using docker clearlinux container with python.

To run the program:

1) Create a folder for python packages
  
  `mkdir wheelhouse/`

2) Download all required python packages, by running:

  `pip download -r requirements.txt -d wheelhouse/`

3) Now you need to build docker image from Dockerfile: 
  
  `docker build -t v17v3/cocoparsing:v3.3 .`

4) And run the docker container:

  `docker run -dt --env URL="http://images.cocodataset.org/annotations/annotations_trainval2017.zip" --env COCO_PATH="/home/coco/data/" v17v3/cocoparsing:v3.3`
