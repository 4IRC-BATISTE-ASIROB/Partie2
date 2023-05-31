import cv2
import socket
import struct
import pickle

# Création du socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5000))
connection = client_socket.makefile('wb')

# Création de la caméra
cam = cv2.VideoCapture(0)

# Envoi des données
img_counter = 0
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
while True:
    ret, frame = cam.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    data = pickle.dumps(frame, 0)
    size = len(data)

    # Envoi de la taille de l'image
    print("{}: {}".format(img_counter, size))
    client_socket.sendall(struct.pack(">I", size) + data)
    img_counter += 1


cam.release()
