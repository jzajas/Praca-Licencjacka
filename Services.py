# TODO input processing (URL, File, Folder) (separately)
# TODO Img processing (separate file?)
import requests
from deepface import DeepFace
import mediapipe as mp
import cv2
import numpy as np

import matplotlib.pyplot as plt
import math


HEIGHT = 480
WIDTH = 480


# TODO might be useless
def resize_and_show(image):
    h, w = image.shape[:2]
    if h < w:
        img = cv2.resize(image, (WIDTH, math.floor(h / (w / WIDTH))))
    else:
        img = cv2.resize(image, (math.floor(w / (h / HEIGHT)), HEIGHT))

    cv2.imshow(winname="face after resizing", mat=img)


def show_face(face, title=None):
    plt.imshow(face)
    plt.title(title)
    plt.axis('off')
    plt.show()


def process_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError("No image behind the url")
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            face = detect_face(image)

            if face is not None:
                print(f"face detected: {type(face)}")
                landmarks_present = draw_mesh(face)
                if landmarks_present:
                    return True
                else:
                    raise ValueError("Face in incorrect position")
            else:
                raise ValueError("Face not found")
    else:
        raise ConnectionError("Problem with url")


# retinaface / mtcnn for quality
# opencv / ssd for speed
# TODO Add clause for not detecting face and error handling
def detect_face(image):
    print("looking for face")
    face_objs = DeepFace.extract_faces(
        img_path=image,
        detector_backend="retinaface",
        enforce_detection=False,
        align=True,
    )
    print(face_objs[0]["confidence"])
    if face_objs[0]["confidence"] > 0:

        show_face(face_objs[0]["face"])

        return face_objs[0]["face"]


def draw_mesh(face_image):
    print("drawing mesh")
    # cv2.imshow(winname="face before resizing", mat=face_image)
    # resize_and_show(face_image)

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_face_mesh = mp.solutions.face_mesh

    with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            refine_landmarks=True,
            max_num_faces=1,
            min_detection_confidence=0.1,
    ) as face_mesh:

        if face_image.dtype == np.float64:
            face_image = (face_image * 255).astype(np.uint8)

        results = face_mesh.process(face_image)
        # Draw face landmarks of each face.
        print(f'Processing Face landmarks')
        annotated_image = face_image.copy()
        if results:
            print(type(results.multi_face_landmarks))
            for face_landmarks in results.multi_face_landmarks:
                # TODO these landmarks will most likely change
                # TODO move it to different function
                mp_drawing.draw_landmarks(
                    image=annotated_image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_tesselation_style())
                mp_drawing.draw_landmarks(
                    image=annotated_image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_contours_style())
                mp_drawing.draw_landmarks(
                    image=annotated_image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_iris_connections_style())

            # resize_and_show(annotated_image)
            show_face(annotated_image)
            return True
