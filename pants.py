import cv2
import mediapipe as mp
import numpy as np

# Load the virtual pant image with alpha channel
pant_img = cv2.imread('C:/Users/ragha/PycharmProjects/Trial/Resources/Pants/P1-removebg-preview.png', cv2.IMREAD_UNCHANGED)

# Check if the image was loaded successfully
if pant_img is None:
    print("Error: Unable to load the virtual pant image.")
    exit()

pant_rgb = pant_img[:, :, :3]
pant_alpha = pant_img[:, :, 3] / 255.0

# Initialize Mediapipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Open the webcam
cap = cv2.VideoCapture("C:/Users/ragha/PycharmProjects/Trial/Videos/qw.mp4")

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform pose estimation
    results = pose.process(rgb_frame)
    try:
        if results.pose_landmarks:
            # Extract keypoints for the legs
            left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP.value]
            left_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE.value]
            right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP.value]
            right_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE.value]

            # Check if any pose landmark is missing
            if None in (left_hip, left_knee, right_hip, right_knee):
                continue

            # Get the bounding box for the legs
            x_min = int(min(left_hip.x, left_knee.x, right_hip.x, right_knee.x) * frame.shape[1])
            y_min = int(min(left_hip.y, left_knee.y, right_hip.y, right_knee.y) * frame.shape[0])
            x_max = int(max(left_hip.x, left_knee.x, right_hip.x, right_knee.x) * frame.shape[1])
            y_max = int(max(left_hip.y, left_knee.y, right_hip.y, right_knee.y) * frame.shape[0])

            # Increase the size of the virtual pant image height by 100 pixels
            resize_increase_height = 100
            height, width = y_max - y_min + resize_increase_height, x_max - x_min

            # Increase the size of the virtual pant image width by 150 pixels
            resize_increase_width = 150
            width += 2 * resize_increase_width

            # Calculate the new position of the pant exactly over the hip line
            new_y_min = y_min - resize_increase_height
            new_y_max = new_y_min + height

            resized_pant_rgb = cv2.resize(pant_rgb, (width, height))
            resized_pant_alpha = cv2.resize(pant_alpha, (width, height))

            # Create a mask from the alpha channel
            mask = resized_pant_alpha[:, :, np.newaxis]

            # Ensure mask has the same number of channels as the frame
            if mask.shape[2] != frame.shape[2]:
                mask = np.repeat(mask, frame.shape[2], axis=2)

            # Blend the virtual pant with the adjusted legs using the mask
            roi_color = frame[new_y_min:new_y_max, x_min - resize_increase_width:x_max + resize_increase_width, :3]

            frame[new_y_min:new_y_max, x_min - resize_increase_width:x_max + resize_increase_width, :3] = (
                    (1 - mask) * roi_color + mask * resized_pant_rgb
            )

    except:
        pass
    # Display the frame
    cv2.imshow('Virtual Pant Try-On', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.getWindowProperty('Virtual Pant Try-On', cv2.WND_PROP_VISIBLE) < 1:
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
