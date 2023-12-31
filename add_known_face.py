# -*- coding: utf-8 -*-
"""add_known_face.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Bn8kE-5vsVUjvW7qm8avcHVDG-E5_sIh
"""

known_face_encodings = []
known_face_names = []

def draw_label(input_image, coordinates, label):
    image = input_image.copy()
    (top, right, bottom, left) = coordinates
    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 5)
    cv2.putText(image, label, (left - 10, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    return image

def add_known_face(face_image_path, name):
    face_image = cv2.imread(face_image_path)
    dets_locations = face_locations(face_image, 1)
    face_encoding = face_recognition.face_encodings(face_image, dets_locations)[0]

    detected_face_image = draw_label(face_image, dets_locations[0], name)

    known_face_encodings.append(face_encoding)
    known_face_names.append(name)

    plt_imshow(["Input Image", "Detected Face"], [face_image, detected_face_image])


def name_labeling(input_image, size=None):
    image = input_image.copy()

    if size:
        image = imutils.resize(image, width=size)


    dets_locations = face_locations(image)
    face_encodings = face_recognition.face_encodings(image, dets_locations)

    face_names = []

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.4)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

    for (top, right, bottom, left), name in zip(dets_locations, face_names):
        if name != "Unknown":
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)

        cv2.rectangle(image, (left, top), (right, bottom), color, 1)
        cv2.rectangle(image, (left, bottom - 10), (right, bottom), color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(image, name, (left + 3, bottom - 3), font, 0.2, (0, 0, 0), 1)

    plt_imshow("Output", image, figsize=(24, 15))