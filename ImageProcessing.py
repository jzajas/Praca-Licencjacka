from deepface import DeepFace
import mediapipe as mp
import numpy as np


HEIGHT = 480
WIDTH = 480

NOSE = 1
LEFT_CHEEK = 234
RIGHT_CHEEK = 454
RIGHT_EAR = 356
LEFT_EAR = 127
RIGHT_EYE = 130
LEFT_EYE = 359


def detect_face(image, detector):
    try:
        face_objs = DeepFace.extract_faces(
            img_path=image,
            detector_backend=detector,
            enforce_detection=False,
            align=True,
        )

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
            return is_face_facing_camera(face_image, face_landmarks, options)


def is_face_facing_camera(face_image, face_landmarks, options):
    height, width, _ = face_image.shape

    nose = face_landmarks.landmark[NOSE]
    right_cheek = face_landmarks.landmark[RIGHT_CHEEK]
    left_cheek = face_landmarks.landmark[LEFT_CHEEK]
    right_ear = face_landmarks.landmark[RIGHT_EAR]
    left_ear = face_landmarks.landmark[LEFT_EAR]
    right_eye = face_landmarks.landmark[RIGHT_EYE]
    left_eye = face_landmarks.landmark[LEFT_EYE]

    # 1. Nose between eyes (symmetry around nose)
    eye_center = (left_eye.x + right_eye.x) / 2
    nose_eye_offset = abs(nose.x - eye_center)

    # 2. nose symmetry
    cheek_symmetry = abs((right_cheek.x - nose.x) - (nose.x - left_cheek.x))

    # 3. Ear height alignment
    ear_diff = abs(left_ear.y - right_ear.y)

    nose_eye_threshold = float(options[0])
    cheek_threshold = float(options[1])
    ear_high_difference_threshold = float(options[2])

    is_facing = (
            nose_eye_offset < nose_eye_threshold and
            cheek_symmetry < cheek_threshold and
            ear_diff < ear_high_difference_threshold
    )

    return is_facing

