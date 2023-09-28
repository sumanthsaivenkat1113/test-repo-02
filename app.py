
from flask import Flask, render_template, request
import os
from PIL import Image
import numpy as np
import cv2 
import MySQLdb



app = Flask(__name__)

db = MySQLdb.connect(host="localhost", user="root", passwd="Password", db="object_detection_tests")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST','GET'])
def upload():
    # get the uploaded file from the form
    file = request.files['file']

    # save the file to a directory on the server
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # delete all images in the directory except for the last one
    file_list = os.listdir(app.config['UPLOAD_FOLDER'])
    file_list.sort(key=lambda x: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], x)))
    for i in range(len(file_list) - 1):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file_list[i]))

    # process the image if necessary using Pillow
    img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    img = img.resize((128, 128))
    img.save(os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnail_' + filename))

    # delete the thumbnail image if it exists
    thumbnail_filename = 'thumbnail_' + filename
    thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], thumbnail_filename)
    if os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)

    # load the image using OpenCV
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # set up the object detection model using the SSD MobileNet V3 model
    classNames = []
    with open('coco.names','r') as f:
        classNames = f.read().splitlines()

    weightsPath = "frozen_inference_graph.pb"
    configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
    net = cv2.dnn_DetectionModel(weightsPath, configPath)
    net.setInputSize(320, 320)
    net.setInputScale(1.0/127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)

    # perform object detection on the image
    classIds, confs, bbox = net.detect(img, confThreshold=0.58)
    print(classIds)

    # draw rectangles and labels for each detected object
    bbox = list(bbox)
    confs = list(np.array(confs).reshape(1, -1)[0])
    confs = list(map(float, confs))
    for classId, conf, box in zip(classIds.flatten(), confs, bbox):
        cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
        cv2.putText(img, classNames[classId-1].upper(), (box[0]+10, box[1]+30), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
        var= classNames[classId-1]

    # save the image with the object detection results
    result_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result_' + filename)
    cv2.imwrite(result_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    print(var)
    

    cur = db.cursor()
    # cur.execute("SELECT * FROM object_detection_test_one WHERE Product_Name = %s")
    Product_Name = var
    sql = "SELECT * FROM object_detection_test_one WHERE Product_Name = %s"
    cur.execute(sql, (Product_Name,))
    data = cur.fetchall()
    cur.close()
    return render_template('Result_page.html', data=data)


if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.run(debug=True)


