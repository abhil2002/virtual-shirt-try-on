import cv2
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Load your watch image with an alpha channel (transparency)
watch_img = cv2.imread("watch.png", cv2.IMREAD_UNCHANGED)

# Initialize Pygame and OpenGL
pygame.init()
width, height = 800, 600
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

# Set up the 3D space
gluPerspective(45, (width / height), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Set up blending for transparency
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# Webcam setup
cap = cv2.VideoCapture(0)

# Main loop
while True:
    ret, frame = cap.read()

    # Detect face using a face detection algorithm (e.g., Haarcascades)
    # Replace this with your preferred face detection method
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    for (x, y, w, h) in faces:
        # Calculate the position and size for rendering the watch on the face
        face_center = np.array([(x + x + w) / 2, (y + y + h) / 2])
        watch_size = max(w, h) * 1.5

        # Render the watch on the face
        glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, watch_img.shape[1], watch_img.shape[0], 0, GL_RGBA, GL_UNSIGNED_BYTE, watch_img.tobytes())

        glEnable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(face_center[0] - watch_size / 2, face_center[1] - watch_size / 2, 0)
        glTexCoord2f(1, 0)
        glVertex3f(face_center[0] + watch_size / 2, face_center[1] - watch_size / 2, 0)
        glTexCoord2f(1, 1)
        glVertex3f(face_center[0] + watch_size / 2, face_center[1] + watch_size / 2, 0)
        glTexCoord2f(0, 1)
        glVertex3f(face_center[0] - watch_size / 2, face_center[1] + watch_size / 2, 0)
        glEnd()
        glDisable(GL_TEXTURE_2D)

    pygame.display.flip()
    pygame.time.wait(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            cap.release()
            cv2.destroyAllWindows()
            quit()
