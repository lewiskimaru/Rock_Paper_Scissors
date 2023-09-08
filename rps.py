from streamlit_webrtc import webrtc_streamer
import streamlit as st

# Create a container for the video element
container = st.container()

# Set the style of the container to have a curved border
container.markdown("""
<style>
div[role="figure"] {
    border: 5px solid black;
    border-radius: 25px;
}
</style>
""", unsafe_allow_html=True)

# Start the video streamer inside the container
webrtc_streamer(key="example", video_processor_factory=None, object_detection=True, container=container)
