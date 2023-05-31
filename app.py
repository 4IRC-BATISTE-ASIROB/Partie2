from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)


def generate_frames():
    print('Starting camera...')
    # Path : C:\Users\batis\Desktop\ASI-Robotique\Partie2\static\videos\voitures.mp4
    while True:
        # camera = cv2.VideoCapture(0)
        camera = cv2.VideoCapture('static/videos/voitures.mp4')
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        # Don't forget to release the video capture at the end of the video.
        camera.release()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/video')
def video():
    return render_template('video.html')


@app.route('/page2')
def page2():
    return render_template('page2.html')


@app.route('/video_stream')
def video_stream():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
