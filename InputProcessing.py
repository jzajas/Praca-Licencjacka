from ImageProcessing import *
import requests
import numpy as np
import cv2
import os

EXTENSIONS =["png", "jpg", "jpeg", "raw", "tif", "tiff", "bmp", "avif", "webp"]


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

    face_quality = process_image(image, file_path)
    return face_quality


def process_folder(folder_path):
    results = []

    files = os.listdir(folder_path)
    all_files = [file for file in files if os.path.isfile(os.path.join(folder_path, file))]

    for file in all_files:
        path = os.path.join(folder_path, file)
        file_extension = file.split(".")[-1]
        if file_extension in EXTENSIONS:
            try:
                face_quality = process_file(path)
                results.append((path, face_quality))
            except ValueError as e:
                message, path_in_error = e.args
                results.append((path_in_error, message))
        else:
            results.append((path, "Incorrect file extension"))

    return results


def process_image(image, path):
    if image is None:
        raise ValueError("No image behind the url", path)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face = detect_face(image)

        if face is not None:
            landmarks_present = draw_mesh(face)
            if landmarks_present:
                return True
            else:
                raise ValueError("Face in incorrect position", path)
        else:
            raise ValueError("Face not found", path)
