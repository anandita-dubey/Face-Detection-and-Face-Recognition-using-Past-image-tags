from flask import Flask, render_template, url_for, request, jsonify, redirect
import json
import os
from os import path
import json
from PIL import Image
import datetime
import logging
from Model import *

logging.basicConfig(level=logging.NOTSET)


application = Flask(__name__)
UPLOAD_FOLDER = "static/uploads/uploaded"
application.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])
imagefilename = ""


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route("/")
def parent():
    for root, dirs, files in os.walk(application.config['UPLOAD_FOLDER']):
        for file in files:
            if file!='.keep':
                os.remove(os.path.join(root, file))
    return render_template("image_upload.html")


@application.route("/preview", methods=["POST"])
def preview():
    global imagefilename
    if request.method == "POST":
        file = request.files["file"]
        logging.info("###################### Image was Uploaded ######################")
        if allowed_file(file.filename):
            imagefilename = file.filename
            file.save(os.path.join(application.config["UPLOAD_FOLDER"], imagefilename))
        imageLoc = os.path.join(application.config["UPLOAD_FOLDER"], imagefilename)
        predicted_tags=predict(imageLoc)
        # print(predicted_tags)
        return render_template("preview.html", src=imageLoc,predicted=json.dumps(predicted_tags))

@application.route("/getdataJSON", methods=["POST"])
def getdataJSON():
    if request.method == "POST":
        dataJSON = request.form["jsonData"]
        logging.info(
            "###################### JSON data Receieved ######################"
        )
        extractFaces(dataJSON)
        return "Status:", 200


def extractFaces(pixelData):
    dataList = json.loads(pixelData)
    print(dataList)
    imagepath = os.path.join(application.config["UPLOAD_FOLDER"], imagefilename)
    resizedimage = Image.open(imagepath)
    for data in dataList:
        for key, value in data.items():
            width = value["ImageWidth"]
            height = value["ImageHeight"]
    resizedimage = resizedimage.resize((width, height))
    resizedimage.save(imagepath)
    for data in dataList:
        for key, value in data.items():
            name = key
            l = value["left"]
            t = value["top"]
            r = value["right"]
            b = value["bottom"]
            crop(imagepath, name, (l, t, r, b))
    os.remove(imagepath)
    logging.info(
        "###################### Faces Extracted:%(count)s ######################",
        {"count": len(dataList)},
    )


def crop(imagepath, tagname, coords):
    imagename = tagname + datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + ".PNG"
    image_obj = Image.open(imagepath)
    cropped_image = image_obj.crop(coords)
    pathname = os.path.join("static/uploads", tagname)
    if not os.path.isdir(pathname):
        os.mkdir(pathname)
        cropped_image.save(os.path.join(pathname, imagename), "PNG")
        encode_face(pathname)
    else:
        cropped_image.save(os.path.join(pathname, imagename), "PNG")


if __name__ == "__main__":
    application.run(debug="enable")
