# TODO every function has some overlaps (move it to separate function)
# TODO Remove image showing
from ImageProcessing import *
import requests
import numpy as np
import cv2


def process_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        good_face_quality = process_image(image)
        return good_face_quality
    else:
        raise ConnectionError("Problem with url")


def process_file(file_path):
    image = cv2.imread(file_path)

    good_face_quality = process_image(image)
    return good_face_quality


def process_image(image):
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
