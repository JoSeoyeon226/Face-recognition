import base64
import json
import os
import pickle
import uuid
import logging

import cv2

import face_recognition

import numpy as np
from flask import render_template, request, jsonify, url_for, redirect, flash
from flask_login import login_required

from apps import upload_dir, models_dir, face_names_dir, fonts_dir, custom_face_model_dir
from apps.Capture import blueprint
from .forms import FileForm

# 분류기
detector = cv2.CascadeClassifier(os.path.join(models_dir, "haarcascades", "haarcascade_frontalface_default.xml"))


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def on_json_loading_failed_return_dict(e):
    return {}


# 얼굴인식
@blueprint.route("/Capture", methods=["GET"])
# @login_required
def recognize():
    return render_template("home/Capture.html")


# 얼굴 인식(backend)
@blueprint.route("/Capture", methods=["POST"])
# @login_required
def recognize_post():
    request.on_json_loading_failed = on_json_loading_failed_return_dict

    if request.get_json()["imageData"]:
        # 인코딩 모델 불러오기
        model_file = os.path.join(custom_face_model_dir, "encodings.pickle")
        data = pickle.loads(open(model_file, "rb").read())

        # base64 데이터를 OpenCV 이미지 데이터로 변환하기
        im_bytes = base64.b64decode(request.get_json()["imageData"])
        img_arr = np.frombuffer(im_bytes, dtype=np.uint8)
        img_bgr = cv2.imdecode(img_arr, flags=cv2.IMREAD_COLOR)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

        # 얼굴 찾기
        boxes = face_recognition.face_locations(img_rgb)
        encodings = face_recognition.face_encodings(img_rgb, boxes)

        # 얼굴 인식
        who_names = []

        for encoding in encodings:
            distances = face_recognition.face_distance(data["encodings"], encoding)

            name = "unknown"
            print(f"name 1: {name}")
            if min(distances) < 0.4:
                index = np.argmin(distances)
                name = data["names"][index]
                print(f"name 2: {name}")
            who_names.append(name)
            print(f"name 3: {name}")
        # 얼굴 표시
        for (top, right, bottom, left), name in zip(boxes, who_names):
            cv2.rectangle(img_bgr, (left, top), (right, bottom), (0, 0, 255), 1)
            cv2.rectangle(img_bgr, (left, bottom), (right, bottom + 25), (0, 0, 255), -1)
            print(f"name 4: {who_names[0]}")
        # 이름 표시
        from PIL import ImageFont, ImageDraw, Image
        img_pillow = Image.fromarray(img_bgr)
        draw = ImageDraw.Draw(img_pillow)
        font = ImageFont.truetype(os.path.join(fonts_dir, "gulim.ttc"), 14)
        for (top, right, bottom, left), name in zip(boxes, who_names):
            draw.text((left + 10, bottom + 5), name, font=font, fill=(255, 255, 255))

        img_bgr = np.array(img_pillow)

        # 이미지 파일을 base64로 인코딩
        img_jpg = cv2.imencode(".jpg", img_bgr)
        image_base64 = base64.b64encode(img_jpg[1]).decode("utf-8")
        #select_name = who_names[0]


        #return jsonify(image_base64=image_base64)
        #return jsonify(zname = f'{select_name}')  #seccess
        return jsonify(image_base64=image_base64, zname=f'{who_names[0]}')  #final
        #return render_template('home/Capture.html', jsonify(image_base64=image_base64), name=who_names[0])
    return jsonify()
