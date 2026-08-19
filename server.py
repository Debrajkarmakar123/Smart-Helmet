from flask import Flask, Response
from flask_cors import CORS
import cv2
import datetime
import os

app = Flask(__name__)
CORS(app)

camera = cv2.VideoCapture(0)

# Recordings save karne ke liye folder banana
SAVE_DIR = "recordings"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# Automatic Recording Setup (Server start hote hi recording chalu)
filename = datetime.datetime.now().strftime("auto_rec_%Y-%m-%d_%H-%M-%S.mp4")
filepath = os.path.join(SAVE_DIR, filename)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 20.0
width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

# File writer active kar diya
out = cv2.VideoWriter(filepath, fourcc, fps, (width, height))
print(f"🔴 Automatic Recording Started: {filename}")

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Har ek live frame ko chupchaap file mein save karte jao
            out.write(frame)

            # Browser ke liye frame bhejna
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("🚀 Server chal raha hai aur background mein recording on hai!")
    app.run(host='0.0.0.0', port=5000, debug=False)