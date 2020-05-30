from django.shortcuts import render
from django.http.response import StreamingHttpResponse
import cv2
import os


def home(request):
    return render(request, "index.html")


def cam(request):
    return render(request, "1.html")


classifier = cv2.CascadeClassifier(
    "C:\\Users\\vidya_murali\\projects\\button_test\\btadmin\\CAM_FILES\\haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(r'C:\\Users\\vidya_murali\\projects\\button_test\\btadmin\\CAM_FILES\\haarcascade_eye_tree_eyeglasses.xml')


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = classifier.detectMultiScale(gray,1.3,5)
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255,255,255), 3)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = image[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        frame_flip = cv2.flip(image, 1)
        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
