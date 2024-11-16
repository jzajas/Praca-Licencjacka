# TODO input processing (URL, File, Folder) (separately)
# TODO Img processing (separate file?)
import requests
from deepface import DeepFace
import mediapipe as mp
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox

HEIGHT = 480
WIDTH = 480


def process_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        # TODO check if not passing an image will produce an error (url to article or sth)
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        print(type(image))
        if image is None:
            messagebox.showinfo(title="Bad URL",
                                message="Error: Image not loaded properly. Check the URL or the response."
                                )
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            plt.imshow(image)
            plt.title(f"Extracted Face")
            plt.axis('off')
            plt.show()

            face = detect_face(image)

            # plt.imshow(face)
            # plt.title(f"Extracted Face")
            # plt.axis('off')
            # plt.show()
            print("Face detected")

            draw_mesh(face)

            return True
    else:
        print()


# TODO Retinaface / Mtcnn for quality
# TODO OpenCv / ssd for speed
# TODO Add clause for not detecting face and error handling
def detect_face(image):
    face_objs = DeepFace.extract_faces(
        img_path=image,
        detector_backend="opencv",
        enforce_detection=False,
        align=True,
    )

    return face_objs[0]["face"]


def resize_and_show(image):
    h, w = image.shape[:2]
    if h < w:
        img = cv2.resize(image, (WIDTH, math.floor(h / (w / WIDTH))))
    else:
        img = cv2.resize(image, (math.floor(w / (h / HEIGHT)), HEIGHT))

    cv2.imshow(winname="face after resizing", mat=img)


def draw_mesh(face_image):
    cv2.imshow(winname="face before resizing", mat=face_image)
    resize_and_show(face_image)

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_face_mesh = mp.solutions.face_mesh

    with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            refine_landmarks=True,
            max_num_faces=1,
            min_detection_confidence=0.5,
    ) as face_mesh:

        if face_image.dtype == np.float64:
            face_image = (face_image * 255).astype(np.uint8)

        results = face_mesh.process(face_image)
        # Draw face landmarks of each face.
        print(f'Face landmarks')
        annotated_image = face_image.copy()
        if results:
            print(type(results.multi_face_landmarks))
            print(results)
            try:
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

            except TypeError:
                # TODO return false i pokazać użytkownikowi graficznie

                return False

        resize_and_show(annotated_image)
