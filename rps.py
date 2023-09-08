from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import streamlit as st
import cv2
import numpy as np
import av
import mediapipe as mp
import base64


###################################### Helper functions ##############################
# Read the image file and encode it as base64

with open('/mount/src/rock_paper_scissors/Resources/ai_face.jpg', 'rb') as aiface:
    image_data = base64.b64encode(aiface.read()).decode('utf-8') 

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
scores = [0, 0] # [AI, Player]
    
st.set_page_config(page_title="RPS", page_icon="🤖", layout="wide",)

col1, col2 = st.columns(2)

# Define a custom CSS style to create the curved border
custom_css = """
<style>
    .curved-border {
        border: 2px solid green;
        border-radius: 15px;
        padding: 10px;
    }
</style>
"""

# Display the custom CSS style
st.markdown(custom_css, unsafe_allow_html=True)

# Add content to the right column (video stream)
with col1:
    st.info(f"Player{scores[1]}")
    # Define a video processor class
    class VideoProcessor:
        def recv(self, frame):
            img = frame.to_ndarray(format="bgr24")
            img = process(img)
            return av.VideoFrame.from_ndarray(img, format="bgr24")
    
    # Create the WebRTC streamer
    # Display the WebRTC component within a curved-border <div>
    with st.markdown('<div class="curved-border">', unsafe_allow_html=True):
     webrtc_ctx = webrtc_streamer(
        key="hand-tracking",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": True, "audio": False},
        video_processor_factory=VideoProcessor,
        async_processing=True,
        container: Optional[DeltaGenerator]=container
    )

# Add content to the left column (app description)
with col2:
    st.info(f"AI {scores[0]}")
    img_tag = f'<img src="data:image/png;base64,{image_data}" style="border: 2px solid green; border-radius: 15px;">'
    # Create a Streamlit component to render the HTML
    st.components.v1.html(img_tag, height=400)
