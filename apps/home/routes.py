# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import base64
import os
import pickle
import uuid

import face_recognition

from apps import upload_dir, face_names_dir, custom_face_model_dir, allowed_image_file
from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.home import blueprint
from .forms import FileForm


@blueprint.route('/')
def route_default():
    return render_template('home/choice.html', segment='choice')


@blueprint.route('/Capture')
def capture():
    return render_template('home/Capture.html', segment='choice')


@blueprint.route('/index')
@login_required
def index():
    return render_template('home/AdminMain.html', segment='index')


@blueprint.route("/StudentList", methods=["GET", "POST"])
@login_required
def student_list():
    face_names = os.path.join(upload_dir, "face_names")
    if not os.path.exists(face_names):
        os.makedirs(face_names)

    form = FileForm(request.form)
    name = form.name.data
    messages = []

    if request.method == "POST":
        if name:
            # 디렉터리 생성
            name_dir = os.path.join(upload_dir, "face_names", name)
            if not os.path.exists(name_dir):
                os.makedirs(name_dir)
            messages.append("데이터가 등록되었습니다.")

    # 사용자 이름 불러오기
    names = os.listdir(face_names)

    name_list = []
    for name in names:
        name_path = os.path.join(upload_dir, "face_names", name)
        files = os.listdir(name_path)
        count = len(files)
        data = {"name": name, "count": count}
        name_list.append(data)

    return render_template('home/StudentList.html', name_list=name_list, messages=messages, form=form)


# 얼굴 인식(이름 목록) - 학생 등록
@blueprint.route("/name_list", methods=["GET", "POST"])
@login_required
def name_list():
    # 사용자 이름 디렉터리 확인 후 없으면 생성
    face_names = os.path.join(upload_dir, "face_names")
    if not os.path.exists(face_names):
        os.makedirs(face_names)

    form = FileForm(request.form)
    name = form.name.data
    messages = []

    if request.method == "POST":
        if name:
            # 디렉터리 생성
            name_dir = os.path.join(upload_dir, "face_names", name)
            if not os.path.exists(name_dir):
                os.makedirs(name_dir)
            messages.append("데이터가 등록되었습니다.")

    return render_template("home/name_list.html", messages=messages, form=form)


# 이름 삭제
@blueprint.route("/name_delete/<string:name>")
@login_required
def name_delete(name):
    name_path = os.path.join(upload_dir, "face_names", name)
    if os.path.exists(name_path):
        import shutil
        shutil.rmtree(name_path)
    flash("데이터가 삭제되었습니다.")
    return redirect(url_for("home_blueprint.student_list"))


# 사진 등록
@blueprint.route("/face_upload", methods=["POST"])
@login_required
def face_upload():
    form = FileForm(request.form)

    file = request.files["file"]
    name = form.data["name"]

    # 저장 위치
    name_path = os.path.join(upload_dir, "face_names", name)

    # 파일 저장
    new_filename = str(uuid.uuid4()) + ".png"
    file.save(os.path.join(name_path, new_filename))

    return jsonify(result="ok")


# 사진 삭제
@blueprint.route("/face_delete/<string:name>/<string:file_name>")
@login_required
def face_delete(name, file_name):
    file_path = os.path.join(upload_dir, "face_names", name, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
    flash("데이터가 삭제되었습니다.")
    return redirect(url_for("face_blueprint.face_list", name=name))


# 사진 학습
@blueprint.route("/train_face", methods=["POST"])
@login_required
def train_face():
    if not os.path.exists(custom_face_model_dir):
        os.makedirs(custom_face_model_dir)

    model_file = os.path.join(custom_face_model_dir, "encodings.pickle")
    if os.path.exists(model_file):
        os.remove(model_file)

    known_face_names = []
    known_face_encodings = []
    known_images_dirs = os.listdir(face_names_dir)

    for known_images_dir in known_images_dirs:
        known_file_path = os.path.join(face_names_dir, known_images_dir)
        known_files = os.listdir(known_file_path)

        for known_file in known_files:
            # 파일명, 확장자
            known_face_names.append(known_images_dir)

            # 인코딩
            known_image_path = os.path.join(known_file_path, known_file)
            known_image = face_recognition.load_image_file(known_image_path)
            known_face_encoding = face_recognition.face_encodings(known_image)[0]
            known_face_encodings.append(known_face_encoding)

    # 인코딩 데이터 저장
    data = {"encodings": known_face_encodings, "names": known_face_names}
    f = open(model_file, "wb")
    f.write(pickle.dumps(data))
    f.close()

    return jsonify(result="ok")


# 얼굴 인식(이름에 해당하는 사진 목록)
@blueprint.route("/face_list/<string:name>", methods=["GET", "POST"])
@login_required
def face_list(name):
    form = FileForm(request.form)
    messages = []
    errors = []

    # 사진 등록
    if request.method == "POST":
        file = request.files["file"]
        if file and allowed_image_file(file.filename):
            # 확장자
            file_extension = file.filename.split(".")[-1]

            # 파일 저장
            new_filename = str(uuid.uuid4()) + "." + file_extension
            file.save(os.path.join(upload_dir, "face_names", name, new_filename))
            messages.append("데이터가 등록되었습니다.")

    # 사진 파일 불러오기
    faces = os.listdir(os.path.join(upload_dir, "face_names", name))

    face_list = []
    for face in faces:
        face_path = os.path.join(upload_dir, "face_names", name, face)

        # 이미지 파일을 base64로 인코딩
        with open(face_path, "rb") as img_file:
            image_base64 = base64.b64encode(img_file.read()).decode('utf-8')

        # 확장자
        file_extension = face.split(".")[-1]

        # 파일 생성 시간
        from datetime import datetime
        create_unixtime = os.path.getctime(face_path)
        create_timestamp = datetime.fromtimestamp(create_unixtime)
        create_datetime = datetime.strftime(create_timestamp, '%Y-%m-%d %H:%M:%S')

        # 파일 크기
        file_size = os.path.getsize(face_path)

        data = {"name": name, "image_base64": image_base64, "file_extension": file_extension, "file_name": face,
                "create_datetime": create_datetime, "file_size": file_size}
        face_list.append(data)

    return render_template("home/face_list.html", face_list=face_list, name=name, messages=messages, form=form)


@blueprint.route("/SubjectList")
@login_required
def SubjectList():
    return render_template("home/SubjectList.html", segment='subject')


@blueprint.route("/subject_list")
@login_required
def subject_list():
    return render_template("home/subject_list.html", segment='subject_list')


# 수업주차관리
@blueprint.route("/Week_subject")
@login_required
def Week_subject():
    return render_template("home/Week_subject.html", segment='Week_subject')


# 수업주차관리 - 수업등록
@blueprint.route("/Week_registration")
@login_required
def Week_registration():
    return render_template("home/Week_registration.html", segment='Week_registration')


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
