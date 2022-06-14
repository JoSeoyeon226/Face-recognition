import os
import pickle

from flask_socketio import emit

from . import IOBlueprint
from .. import custom_face_model_dir, face_names_dir

ws_blueprint = IOBlueprint("/ws")


@ws_blueprint.on("say")
def say():
    emit("flash", "Server says...", namespace="/")


@ws_blueprint.on("echo")
def echo(msg):
    emit("flash", msg.get("data"), namespace="/")


@ws_blueprint.on("my event")
def handle_my_custom_event(json):
    emit("connect response", "hello client", namespace="/ws")
    print("received json: " + str(json))
    

@ws_blueprint.on("train face")
def train_face(json):
    emit("train face", "얼굴 학습 시작", namespace="/ws")

    if not os.path.exists(custom_face_model_dir):
        os.makedirs(custom_face_model_dir)

    model_file = os.path.join(custom_face_model_dir, "encodings.pickle")
    if os.path.exists(model_file):
        os.remove(model_file)

    known_face_names = []
    known_face_encodings = []
    known_images_dirs = os.listdir(face_names_dir)
    print(known_images_dirs)

    for known_images_dir in known_images_dirs:
        emit("train face", f"얼굴 학습 시작 - {known_images_dir}", namespace="/ws")
        known_file_path = os.path.join(face_names_dir, known_images_dir)
        known_files = os.listdir(known_file_path)

        for known_file in known_files:

            # 파일명, 확장자
            known_face_names.append(known_images_dir)

            # 인코딩
            import face_recognition
            known_image_path = os.path.join(known_file_path, known_file)
            known_image = face_recognition.load_image_file(known_image_path)
            known_face_encoding = face_recognition.face_encodings(known_image)[0]
            known_face_encodings.append(known_face_encoding)

            emit("train face", f"인코딩 완료 - {known_images_dir} - {known_file}", namespace="/ws")

    # 인코딩 데이터 저장
    data = {"encodings": known_face_encodings, "names": known_face_names}
    f = open(model_file, "wb")
    f.write(pickle.dumps(data))
    f.close()

    emit("train face", "얼굴 학습 완료", namespace="/ws")
