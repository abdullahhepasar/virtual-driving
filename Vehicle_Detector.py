# coding: utf-8
# # Object Detection Demo
# License: Apache License 2.0 (https://github.com/tensorflow/models/blob/master/LICENSE)
# source: https://github.com/tensorflow/models
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
from grabscreen import grab_screen
import cv2
import keys as k
import time
from ctypes import windll, Structure, c_long, byref

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return { "x": pt.x, "y": pt.y}

keys = k.Keys({})

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("C:/../models/research/object_detection/")


# ## Object detection imports
# Here are the imports from the object detection module.

from utils import label_map_util
from utils import visualization_utils as vis_util


# # Model preparation 
# What model to download.
MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'C:/../models/research/object_detection/data/mscoco_label_map.pbtxt')

NUM_CLASSES = 90

# ## Download Model
##opener = urllib.request.URLopener()
##opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
try:
  tar_file = tarfile.open("C:/../models/research/object_detection/ssd_mobilenet_v1_coco_11_06_2017.tar.gz")
  for file in tar_file.getmembers():
    file_name = os.path.basename(file.name)
    print(file_name)
    if 'frozen_inference_graph.pb' in file_name:
      tar_file.extract(file, os.getcwd())
except ExceptionI as e:
  print("got it :-) ", e)
  pass

# ## Load a (frozen) Tensorflow model into memory.
try:
  detection_graph = tf.Graph()
  with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    print(od_graph_def)
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
      serialized_graph = fid.read()
      od_graph_def.ParseFromString(serialized_graph)
      tf.import_graph_def(od_graph_def, name='')
except ExceptionI as e:
  print("got it :-) ", e)
  pass

# ## Loading label map
# Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


def determine_movement(mid_x, mid_y,width=1024, height=768):
  x_move = 0.5-mid_x
  y_move = 1-mid_y
  hm_x = x_move/0.5
  hm_y = y_move/20
  #mouse position
  pos = queryMousePosition()
  print("mouse position--> ", pos)
  
  print('Calcu width --> ',width-1*int(hm_x*width))
  print('Calcu height --> ',height-1*int(hm_y*height))
  keys.keys_worker.SendInput(keys.keys_worker.Mouse(0x0001, -1*int(hm_x*width), -1*int(hm_y*height)))

def fire(mid_x, mid_y,width=1024, height=768):
  x_move = 0.5-mid_x
  y_move = 0.5-mid_y
  hm_x = x_move/0.5
  hm_y = y_move/0.5
  print('fire-->hm_x--> ',hm_x)
  print('fire-->hm_y--> ',hm_y)
  keys.keys_worker.SendInput(keys.keys_worker.Mouse(0x0002, -1*int(hm_x*width), -1*int(hm_y*height)))

# ## Helper code
def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)

with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:
    stolen = False
    hma_x = 0
    while True:
      #screen = cv2.resize(grab_screen(region=(0,40,1280,745)), (WIDTH,HEIGHT))
      screen = cv2.resize(grab_screen(region=(0,40,1024,768)), (350,350))
      image_np = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
      # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
      image_np_expanded = np.expand_dims(image_np, axis=0)
      image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
      # Each box represents a part of the image where a particular object was detected.
      boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
      # Each score represent how level of confidence for each of the objects.
      # Score is shown on the result image, together with the class label.
      scores = detection_graph.get_tensor_by_name('detection_scores:0')
      classes = detection_graph.get_tensor_by_name('detection_classes:0')
      num_detections = detection_graph.get_tensor_by_name('num_detections:0')
      # Actual detection.
      (boxes, scores, classes, num_detections) = sess.run(
          [boxes, scores, classes, num_detections],
          feed_dict={image_tensor: image_np_expanded})
      # Visualization of the results of a detection.
      vis_util.visualize_boxes_and_labels_on_image_array(
          image_np,
          np.squeeze(boxes),
          np.squeeze(classes).astype(np.int32),
          np.squeeze(scores),
          category_index,
          use_normalized_coordinates=True,
          line_thickness=8)

      vehicle_dict = {}

      for i,b in enumerate(boxes[0]):
        #car=3      bus= 6  truck=8 => "or classes[0][i] == 6 or classes[0][i] == 8"
        #airplan = 5, kite=38, bird=16
        #person  = 1
        #and more Abdullah ;) --> https://github.com/tensorflow/models/blob/f87a58cd96d45de73c9a8330a06b2ab56749a7fa/research/object_detection/data/mscoco_label_map.pbtxt
        if classes[0][i] == 5 or classes[0][i] == 38 or classes[0][i] == 16:
          if scores[0][i] >= 0.5:
            mid_x = (boxes[0][i][1]+boxes[0][i][3])/2
            mid_y = (boxes[0][i][0]+boxes[0][i][2])/2
            hma_x = mid_x
            apx_distance = round(((1 - (boxes[0][i][3] - boxes[0][i][1]))**4),1)
            print("apx_distance")
            print(apx_distance)
            cv2.putText(image_np, '{}'.format(apx_distance), (int(mid_x*350),int(mid_y*350)), cv2.FONT_HERSHEY_SIMPLEX, 0.1, (255,255,255), 1)

            if apx_distance <=1:
              if mid_x > 0.70 or mid_x < 0.43 and mid_x < 2:
                print("mid_x()WARN--> ", mid_x)
                cv2.putText(image_np, 'WARNING!!!', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 3)

            vehicle_dict[apx_distance] = [mid_x, mid_y, scores[0][i]]
            print('vehicle_dict--> ',vehicle_dict)
            print('vehicle_LEN--> ',len(vehicle_dict))
            print('hma_x--> ',hma_x)
          if len(vehicle_dict) > 0 and hma_x > 0.60 and hma_x < 2:
##            print('stolen--> ',stolen)
##            if not stolen:
            closest = sorted(vehicle_dict.keys())[0]
            print('closest--> ',closest)
            vehicle_choice = vehicle_dict[closest]
            print('vehicle_choice[0]--> ',vehicle_choice[0])
            print('vehicle_choice[1]--> ',vehicle_choice[1])
            determine_movement(mid_x = vehicle_choice[0], mid_y = vehicle_choice[1], width=1024, height=768)
            if closest < 1.0:
              print('closest and w', closest)
              keys.directKey("w")
##              fire(mid_x = vehicle_choice[0], mid_y = vehicle_choice[1], width=1024, height=768)
##              time.sleep(0.05)          
##              fire(mid_x = vehicle_choice[0], mid_y = vehicle_choice[1], width=1024, height=768)
##              stolen = True
            else:
              print('W')
              keys.directKey("w")

##        else:
##          print('W AND vehicle_LEN--> ',len(vehicle_dict))
##          keys.directKey("w")


      cv2.imshow('window',image_np)
      if cv2.waitKey(25) & 0xFF == ord('q'):
          cv2.destroyAllWindows()
          break
