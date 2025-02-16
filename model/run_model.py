import tensorflow as tf
import numpy as np
import cv2
import mediapipe as mp
import matplotlib.pyplot as plt

# Load Model
model = tf.keras.models.load_model("converted_model/model.h5")

# 🔥 Check Expected Input Shape
EXPECTED_FEATURES = model.input_shape[-1]
print(f"🔍 Model Expects Input Shape: {EXPECTED_FEATURES} features")

# 🔹 Labels (Match them to Teachable Machine)
LABELS = ["Walking", "Shooting", "Knife Attack", "Stealing"]

# Check if labels match model output
num_classes = model.output_shape[-1]
if len(LABELS) != num_classes:
    raise ValueError(f"🚨 ERROR: Model has {num_classes} outputs, but {len(LABELS)} labels were provided!")

# Confidence Threshold
ALERT_THRESHOLD = 0.6  

# Initialize Mediapipe Pose Detector
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Open Webcam
cap = cv2.VideoCapture(0)

# 🔥 Setup Matplotlib Figure for Live Confidence Bar Chart
plt.ion()
fig, ax = plt.subplots()
bars = ax.bar(LABELS, np.zeros(num_classes), color=["orange", "red", "purple", "blue"])
ax.set_ylim(0, 1)
ax.set_title("Live Action Probabilities")
ax.set_ylabel("Confidence Score")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process frame with PoseNet (Mediapipe)
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        # 🔹 Extract only the first 33 keypoints (if TM expects 99 features)
        keypoints = []
        for landmark in results.pose_landmarks.landmark[:33]:  # Take only 33 keypoints
            keypoints.extend([landmark.x, landmark.y, landmark.z])  # Flatten (x, y, z)

        keypoints = np.array(keypoints, dtype=np.float32)

        # 🔹 Ensure input shape matches Teachable Machine expectations
        if len(keypoints) < EXPECTED_FEATURES:
            keypoints = np.pad(keypoints, (0, EXPECTED_FEATURES - len(keypoints)), 'constant')
        elif len(keypoints) > EXPECTED_FEATURES:
            keypoints = keypoints[:EXPECTED_FEATURES]

        # 🔹 Normalize the keypoints
        keypoints = (keypoints - np.mean(keypoints)) / (np.std(keypoints) + 1e-6)

        # 🔹 Reshape for model input
        keypoints_array = keypoints.reshape(1, -1)

        # Make Prediction
        prediction = model.predict(keypoints_array)
        confidence_scores = prediction[0]

        # 🔹 Print All Confidence Scores
        print("\n🔍 Action Probabilities:")
        for i in range(num_classes):
            print(f"{LABELS[i]}: {confidence_scores[i]:.2f}")

        # Update the Matplotlib Live Chart
        for i, bar in enumerate(bars):
            bar.set_height(confidence_scores[i])

        plt.pause(0.05)

        # Get most probable action
        class_index = np.argmax(confidence_scores)
        detected_activity = LABELS[class_index]
        confidence = confidence_scores[class_index]

        # 🚨 Trigger alerts if confidence is high
        if confidence >= ALERT_THRESHOLD:
            print(f"\n⚠️ HIGH CONFIDENCE: {detected_activity} (Confidence: {confidence:.2f})")

            if detected_activity == "Shooting":
                print("🚨 ALERT: Possible Gun Violence Detected! 🔫🚨")
            elif detected_activity == "Knife Attack":
                print("🚨 ALERT: Possible Knife Attack Detected! 🔪🚨")
            elif detected_activity == "Stealing":
                print("🚨 ALERT: Theft in Progress! 🛍️🚨")

        # Draw Pose Skeleton
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Show Live Camera Feed
    cv2.imshow("Live Pose Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()