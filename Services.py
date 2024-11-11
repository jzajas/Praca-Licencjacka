# TODO input processing (URL, File, Folder) (separately)
# TODO Img processing (separate file?)
import requests
import matplotlib.pyplot as plt
import cv2
import numpy as np


def process_input():
    return 0


def process_url(url):
    response = requests.get(url)
    image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    # Decode the image using OpenCV
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    # Convert the image from BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    plt.imshow(image_rgb)
    plt.title(f"Original Face")
    plt.axis('off')
    plt.show()


