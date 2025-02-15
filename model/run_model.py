import tensorflow as tf
import numpy as np
import cv2
import mediapipe as mp

# Load the converted model
model = tf.keras.models.load_model("converted_model/model.h5")

# Initialize Mediapipe Pose Detector (equivalent to tmPose)
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Open MacBook Camera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert frame to RGB (Mediapipe requires RGB input)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process frame with PoseNet (like `model.estimatePose(webcam.canvas)` in JS)
    results = pose.process(rgb_frame)
    
    if results.pose_landmarks:
        # Extract keypoints as [x1, y1, z1, x2, y2, z2, ...]
        keypoints = []
        for landmark in results.pose_landmarks.landmark:
            keypoints.append(landmark.x)  # Normalize X
            keypoints.append(landmark.y)  # Normalize Y
            keypoints.append(landmark.z)  # Normalize Z

        # 🔹 Convert keypoints to numpy array
        keypoints = np.array(keypoints, dtype=np.float32)

        # 🔹 Standardize keypoints (just like Teachable Machine does)
        keypoints = (keypoints - np.mean(keypoints)) / (np.std(keypoints) + 1e-6)

        # 🔹 Ensure input has exactly 14,739 features (Teachable Machine style)
        while len(keypoints) < 14739:
            keypoints = np.append(keypoints, 0)  # Zero-padding
        keypoints = keypoints[:14739]  # Trim if too many

        # Reshape to match model input shape
        keypoints_array = keypoints.reshape(1, -1)  # Shape (1, 14739)

        # 🔹 Make a prediction (same as `model.predict(posenetOutput)` in JS)
        prediction = model.predict(keypoints_array)
        confidence_scores = prediction[0]  # Get probabilities
        class_index = np.argmax(confidence_scores)

        # 🔹 Print confidence scores for debugging
        print(f"Walking: {confidence_scores[0]:.2f}, Standing: {confidence_scores[1]:.2f}, Fighting: {confidence_scores[2]:.2f}")

        # 🔹 Adjust classification threshold for better accuracy
        if confidence_scores[2] > 0.5:  # 50% confidence for fighting detection
            print("⚠️ Fighting Detected (High Confidence)")
        elif class_index == 2:
            print("⚠️ Possible Fighting Detected (Low Confidence)")

        # Draw Pose Skeleton
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Show Live Camera Feed
    cv2.imshow("Live Camera Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()