from flask import Flask, Response
from facial_recognition import facial_recognition  # Import from the separate file

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!doctype html>
    <html lang="en">
      <head><title>Live Camera Feed</title></head>
      <body>
        <h1>Live Camera Feed with Facial and Gesture Recognition</h1>
        <img src="/video_feed" alt="Video Feed">
      </body>
    </html>
    '''

@app.route('/video_feed')
def video_feed():
    return Response(facial_recognition(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True)
