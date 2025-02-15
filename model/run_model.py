import tensorflow as tf
import numpy as np
import cv2
import mediapipe as mp

# Load the converted model
model = tf.keras.models.load_model("converted_model/model.h5")

# Initialize Mediapipe Pose Detector
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Open MacBook Camera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process frame with PoseNet
    results = pose.process(rgb_frame)
    
    if results.pose_landmarks:
        # Extract keypoints (x, y, z for each of 33 landmarks)
        keypoints = []
        for landmark in results.pose_landmarks.landmark:
            keypoints.extend([landmark.x, landmark.y, landmark.z])

        # 🔹 Ensure the input has exactly 14,739 features
        while len(keypoints) < 14739:
            keypoints.append(0)  # Pad with zeros if too few
        keypoints = np.array(keypoints[:14739])  # Trim if too many

        # Reshape to match model input shape
        keypoints_array = keypoints.reshape(1, -1)  # Shape (1, 14739)

        # Make a prediction
        prediction = model.predict(keypoints_array)
        class_index = np.argmax(prediction)

        if class_index == 0:
            print("🚶 Walking Toward Detected")
        elif class_index == 1:
            print("🧍 Standing Detected")
        elif class_index == 2:
            print("⚠️ Fighting Detected")

        # Draw Pose Skeleton
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Show Live Camera Feed
    cv2.imshow("Live Camera Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()