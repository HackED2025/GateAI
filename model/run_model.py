import tensorflow as tf
import numpy as np
import cv2

# Load the converted model
model = tf.keras.models.load_model("converted_model/model.h5")
# Open MacBook Camera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Resize frame to match model input
    frame_resized = cv2.resize(frame, (224, 224))
    frame_array = np.expand_dims(frame_resized, axis=0) / 255.0

    # Make a prediction
    prediction = model.predict(frame_array)
    class_index = np.argmax(prediction)

    if class_index == 0:
        print("🚶 Walking Toward Detected")
    elif class_index == 1:
        print("🧍 Standing Detected")
    elif class_index == 2:
        print("⚠️ Fighting Detected")

    cv2.imshow("Live Camera Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()