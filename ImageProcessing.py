from deepface import DeepFace
import mediapipe as mp
import matplotlib.pyplot as plt
import numpy as np
import cv2
import math


HEIGHT = 480
WIDTH = 480

NOSE = 1
LEFT_CHEEK = 234
RIGHT_CHEEK = 454
RIGHT_EAR = 356
LEFT_EAR = 127
RIGHT_EYE = 130
LEFT_EYE = 359


def show_face(face, title=None):
    plt.imshow(face)
    plt.title(title)
    plt.axis('off')
    plt.show()


# TODO might be useless
# def resize_and_show(image):
#     h, w = image.shape[:2]
#     if h < w:
#         img = cv2.resize(image, (WIDTH, math.floor(h / (w / WIDTH))))
#     else:
#         img = cv2.resize(image, (math.floor(w / (h / HEIGHT)), HEIGHT))
#
#     cv2.imshow(winname="face after resizing", mat=img)


def detect_face(image, detector):
    print("In detect face, chosen detector:" + detector)
    try:
        face_objs = DeepFace.extract_faces(
            img_path=image,
            detector_backend=detector,
            enforce_detection=False,
            align=True,
        )

        # print(len(face_objs))
        # print(face_objs[0]["confidence"])
        # print(face_objs)

        if len(face_objs) > 1:
            raise ValueError("Too many faces detected")

        if face_objs[0]["confidence"] > 0.5:
            return face_objs[0]["face"]
        else:
            raise ValueError("No face detected")
    except TypeError as e:
        raise TypeError(e)
    except ValueError as e:
        raise ValueError(e)
    except Exception as e:
        raise ValueError(e)


def draw_mesh(face_image, options):
    print("In draw mesh")
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
        if results:
            face_landmarks = results.multi_face_landmarks[0]

            # for face_landmarks in results.multi_face_landmarks:
            #     print(is_face_facing_camera(face_image, face_landmarks))

            # resize_and_show(annotated_image)
            # show_face(annotated_image)
            return is_face_facing_camera(face_image, face_landmarks, options)


# def is_face_facing_camera(height, width, face_landmarks):
def is_face_facing_camera(face_image, face_landmarks, options):
    height, width, _ = face_image.shape

    nose = face_landmarks.landmark[NOSE]
    right_cheek = face_landmarks.landmark[RIGHT_CHEEK]
    left_cheek = face_landmarks.landmark[LEFT_CHEEK]
    right_ear = face_landmarks.landmark[RIGHT_EAR]
    left_ear = face_landmarks.landmark[LEFT_EAR]
    right_eye = face_landmarks.landmark[RIGHT_EYE]
    left_eye = face_landmarks.landmark[LEFT_EYE]

    # nose_tip_coords = (int(nose.x * width), int(nose.y * height))
    # right_eye_coords = (int(right_eye.x * width), int(right_eye.y * height))
    # left_eye_coords = (int(left_eye.x * width), int(left_eye.y * height))
    # right_ear_coords = (int(right_ear.x * width), int(right_ear.y * height))
    # left_ear_coords = (int(left_ear.x * width), int(left_ear.y * height))

    # 1. Eye-ear ratio
    # eye_distance = abs(left_eye.x - right_eye.x)
    # ear_distance = abs(left_ear.x - right_ear.x)
    # eye_ear_ratio = eye_distance / ear_distance if ear_distance > 0 else 0

    # # 2. Nose position relative to face center
    # face_center_x = (left_ear.x + right_ear.x) / 2
    # nose_offset = abs(nose.x - face_center_x)
    #
    # # 3. Nose between eyes (horizontally)
    # # nose_between_eyes = left_eye.x > nose.x > right_eye.x
    # eye_center_x = (left_eye.x + right_eye.x) / 2
    # nose_offset = abs(nose.x - eye_center_x)
    #
    # # 4. Face width symmetry (cheeks)
    # cheek_diff = abs((right_cheek.x - nose.x) - (nose.x - left_cheek.x))

    # 1. Nose between eyes (symmetry around nose)
    eye_center = (left_eye.x + right_eye.x) / 2
    nose_eye_offset = abs(nose.x - eye_center)

    # TODO to zamiwnić na coś innego?
    # 2. nose symmetry
    cheek_symmetry = abs((right_cheek.x - nose.x) - (nose.x - left_cheek.x))

    # 3. Ear height alignment
    ear_diff = abs(left_ear.y - right_ear.y)

    nose_eye_threshold = float(options[0])
    cheek_threshold = float(options[1])
    ear_high_difference_threshold = float(options[2])

    print(nose_eye_offset)
    print(cheek_symmetry)
    print(ear_diff)

    is_facing = (
        nose_eye_offset < nose_eye_threshold and
        cheek_symmetry < cheek_threshold and
        ear_diff < ear_high_difference_threshold
    )

    # # Draw landmarks on face image
    # cv2.circle(face_image, (int(right_eye.x * width), int(right_eye.y * height)), 2, (0, 255, 255), -1)
    # cv2.circle(face_image, (int(left_eye.x * width), int(left_eye.y * height)), 2, (0, 255, 255), -1)
    # cv2.circle(face_image, (int(nose.x * width), int(nose.y * height)), 2, (0, 0, 255), -1)
    # cv2.circle(face_image, (int(right_ear.x * width), int(right_ear.y * height)), 2, (255, 0, 255), -1)
    # cv2.circle(face_image, (int(left_ear.x * width), int(left_ear.y * height)), 2, (255, 0, 255), -1)
    #
    # # Convert face image from BGR to RGB for display
    # face_image_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
    #
    # # Display the image with landmarks
    # plt.imshow(face_image_rgb)
    # plt.title(f"Final")
    # plt.axis('off')
    # plt.show()

    return is_facing

