import streamlit as st
import cv2
import numpy as np
import av
import mediapipe as mp
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# Set up MediaPipe Hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Function to process video frames
def process(image):
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    
    # Draw hand landmarks on the image
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )
    
    return cv2.flip(image, 1)

# Define RTC Configuration
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# Create Streamlit web app
st.title('Hand Tracking App')

# Create two columns
col1, col2 = st.columns(2)

# Add content to the left column (app description)
with col1:
    st.header('App Description')
    st.write('This app uses MediaPipe to perform hand tracking and landmark detection in real-time.')
    st.write('Raise your hand in front of the camera to see hand landmarks on the right.')

# Add content to the right column (video stream)
with col2:
    st.header('Video Stream')
    
    # Define a video processor class
    class VideoProcessor:
        def recv(self, frame):
            img = frame.to_ndarray(format="bgr24")
            img = process(img)
            return av.VideoFrame.from_ndarray(img, format="bgr24")
    
    # Create the WebRTC streamer
    webrtc_ctx = webrtc_streamer(
        key="hand-tracking",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": True, "audio": False},
        video_processor_factory=VideoProcessor,
        async_processing=True,
    )
