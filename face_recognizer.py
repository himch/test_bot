import cv2
import numpy as np
from PIL import Image

# Для детектирования лиц используем каскады Хаара
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# Для распознавания используем локальные бинарные шаблоны
recognizer = cv2.face.LBPHFaceRecognizer_create(1,8,8,8,123)


async def get_faces_images(image_path):
    faces_images = []
    # Переводим изображение в черно-белый формат и приводим его к формату массива
    gray = Image.open(image_path).convert('L')
    image = np.array(gray, 'uint8')

    # Определяем области где есть лица
    faces = faceCascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    # Если лицо нашлось добавляем его в список faces_images
    for (x, y, w, h) in faces:
        faces_images.append(image[y: y + h, x: x + w])
    return faces_images

