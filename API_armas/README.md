Descargar carpetas de https://drive.google.com/open?id=1drjd9oQ6M821RRChrDPbz5KVHcOJPMmD
Colocar en capreta raíz (API-Armas)

Primero correr requirements.txt para tener los recursos necesarios desde la carpeta raíz:
pip install -r requirements.txt

Para correr API:
python app.py

El ejemplo es prueba.html

Todo está listo para correr la API, en caso de que se hagan cambios: 

Para convertir de yolo a Tensorflow:
python load_weights.py --num_classes 1 --weights ./weights/yolov3_custom_last.weights --output ./weights/yolov3.tf

Para correr modelo solo:
./darknet detector test data/obj.data cfg/yolov3_custom.cfg backup/yolov3_custom_last.weights 24.jpg -thresh 0.05



### Detections API (http://localhost:5000/detections)
While app.py is running the first available API is a POST routed to /detections on port 5000 of localhost. This endpoint takes in images as input and returns a JSON response with all the detections found within each image (classes found within the images and the associated confidence)

### Image API (http://localhost:5000/image)
While app.py is running the second available API is a POST routed to /image on port 5000 of localhost. This endpoint takes in a single image as input and returns a string encoded image as the response with all the detections now drawn on the image.

## Running just the TensorFlow model
The tensorflow model can also be run not using the APIs but through using `detect.py` script. 
Don't forget to set the IoU (Intersection over Union) and Confidence Thresholds within your yolov3-tf2/models.py file


## Command Line Args Reference

```bash
load_weights.py:
  --output: path to output
    (default: './weights/yolov3.tf')
  --[no]tiny: yolov3 or yolov3-tiny
    (default: 'false')
  --weights: path to weights file
    (default: './weights/yolov3.weights')
  --num_classes: number of classes in the model
    (default: '80')
    (an integer)

detect.py:
  --classes: path to classes file
    (default: './data/labels/coco.names')
  --images: path to input images as a string with images separated by ","
    (default: 'data/images/dog.jpg')
  --output: path to output folder
    (default: './detections/')
  --[no]tiny: yolov3 or yolov3-tiny
    (default: 'false')
  --weights: path to weights file
    (default: './weights/yolov3.tf')
  --num_classes: number of classes in the model
    (default: '80')
    (an integer)

```
