import os
import argparse
import sys

import cv2 as cv
import numpy as np
import pandas as pd
import tensorflow as tf
import keras
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from flask import Flask, request, send_file, jsonify
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
app = Flask(__name__)

model = None
car_names = None

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)

model = InceptionResNetV2(weights = None, 
    include_top = True, 
    input_shape = (299, 299, 3), 
    classes = 196 )
model._make_predict_function()
model.load_weights('/resource/model.hdf5')


temp = pd.read_csv('cars_name_label.csv')
car_names = temp['names_label'].tolist()
if not os.path.exists('./images'):
    os.mkdir('./images')


@app.route('/')
def index():
    return 'Hello World'

@app.route('/predict', methods=['POST'])
def predict():
    input_file = request.files.get('file')
    if not input_file:
        return BadRequest("File not present in request")
    
    filename = secure_filename(input_file.filename)
    if filename == '':
        return BadRequest("File name is not present in request")
    if not allowed_file(filename):
        return BadRequest("Invalid file type")

    input_filepath = os.path.join('./images/', filename)
    input_file.save(input_filepath)
    pred = _inference(input_filepath)
    return jsonify({
        'prediction': pred
    })


def _inference(imgpath):
    bgr_img = cv.imread(imgpath)
    rgb_img = cv.cvtColor(bgr_img, cv.COLOR_BGR2RGB)
    rgb_img = cv.resize(rgb_img, (299, 299))
    rgb_img = np.expand_dims(rgb_img, 0)
    preds = model.predict(rgb_img) # attention before load model
    prob = np.argmax(preds)
    return car_names[int(prob)]


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run()
