from ImageProcessing import *
import requests
import numpy as np
import cv2


def process_url(url, detector, options):
    response = requests.get(url)
    if response.status_code == 200:
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        face_quality = process_image(image, detector, options)
        return face_quality
    else:
        raise ConnectionError("Problem with url")


def process_file(file_path, detector, options):
    try:
        image = cv2.imread(file_path)
        face_quality = process_image(image, detector, options)
        return face_quality
    except TypeError as e:
        raise TypeError(e)
    except ValueError as e:
        raise ValueError(e)


def process_image(image, detector, options):
    print("In process image")
    if image is None:
        raise ValueError("Could not find image behind provided source")
    else:
        try:
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            face = detect_face(image, detector)
            if face is not None:
                landmarks_present = draw_mesh(image, options)
                if landmarks_present:
                    return True
                else:
                    raise ValueError("Face in incorrect position")
            else:
                raise ValueError("Face not found")
        except TypeError as e:
            raise TypeError(e)
        except ValueError as e:
            raise ValueError(e)