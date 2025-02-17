from flask import Flask, Response
from facial_recognition import facial_recognition

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
        <div id="metadata"></div>
      </body>
    </html>
    '''

@app.route('/video_feed')
def video_feed():
    try:
        return Response(facial_recognition(), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    print("🚀 Starting Flask server...")
    app.run(debug=True)
