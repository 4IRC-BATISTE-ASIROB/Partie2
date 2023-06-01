import cv2
import random
from flask import Flask, Response, render_template, request

num_leds = 5

led_states = [random.choice([True, False]) for _ in range(num_leds)]

app = Flask(__name__)

# TODO : Services indépendants : cam et vidéo / Faire les petits services / Faire un readme


def generate_frames(mode):
    print('Starting camera...')

    # Path : C:\Users\batis\Desktop\ASI-Robotique\Partie2\static\videos\voitures.mp4
    while True:
        if mode == "webcam":
            camera = cv2.VideoCapture(0)
        elif mode == "file":
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


@app.route('/toggle_led', methods=['POST'])
def toggle_led():
    led_id = int(request.form.get('led_id'))
    led_states[led_id] = not led_states[led_id]
    print(f"Toggle led {led_id} to {led_states[led_id]}")
    return {'new_state': led_states[led_id]}

@app.route('/get_temperature', methods=['GET'])
def get_temperature():
    # Here I'm generating a random temperature for the sake of the example,
    # but in a real scenario you would get this data from a real sensor.
    temp = random.uniform(18, 23)
    return {'temperature': temp}


@app.route('/')
def home():
    return render_template('index.html', num_leds=len(led_states), led_states=led_states)


@app.route('/video_webcam')
def video_webcam():
    return render_template('video_webcam.html')


@app.route('/video_file')
def video_file():
    return render_template('video_file.html')


@app.route('/video_stream_webcam')
def video_stream_webcam():
    return Response(generate_frames("webcam"), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_stream_file')
def video_stream_file():
    return Response(generate_frames("file"), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
