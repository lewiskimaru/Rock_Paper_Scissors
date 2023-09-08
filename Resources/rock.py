from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
from PIL import Image
import streamlit as st
import cv2
import mediapipe as mp
import time
import numpy as np
import requests
import cvzone
import random

# Rock paper scissors configuration
st.set_page_config(page_title="RPS", page_icon="🤖")
st.title("Rock Paper Scissors Game")
col1, col2 = st.columns(2)
######################################Helper functions ######################################################
timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [AI, Player]
font = 1


def fingerStats(hand_landmarks, finger_name):
    finger_map = {'INDEX': 6, 'MIDDLE': 10, 'RING': 14, 'PINKY': 18}

    fingerPip = hand_landmarks.landmark[finger_map[finger_name]].y
    fingerTip = hand_landmarks.landmark[finger_map[finger_name] + 2].y

    return fingerPip > fingerTip


def userMove(curr_state):
    if curr_state == "0000":
        user_move = 1
    elif curr_state == "1111":
        user_move = 2
    elif curr_state == "1100":
        user_move = 3
    else:
        user_move = 0
    return user_move


def compMove():
    options = [1, 2, 3]
    computer_move = random.choice(options)
    return computer_move


def getWinner(user, comp):
    if user != 0:
        # Determine the winner
        champ = (user - comp) % 3
        # print(winner)
        if champ == 1:
            scores[1] += 1
            result = "You win"
        elif champ == 2:
            scores[0] += 1
            result = "AI wins"
        else:
            result = "Draw"
    else:
        result = "User move Unknown"
    return result


mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

trig = 0

######################################Play the game ######################################################
def main(image):
    img = image

    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    results = hands.process(imgScaled)
    # print(results.multi_hand_landmarks)

    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), font, 6, (34, 139, 34), 4)

            if timer > 3:
                stateResult = True
                timer = 1

                if results.multi_hand_landmarks:
                    current_state = ""
                    for handLms in results.multi_hand_landmarks:
                        # mpDraw.draw_landmarks(imgScaled, handLms, mpHands.HAND_CONNECTIONS)

                        index_status = fingerStats(handLms, 'INDEX')
                        current_state += "1" if index_status else "0"

                        middle_status = fingerStats(handLms, 'MIDDLE')
                        current_state += "1" if middle_status else "0"

                        ring_status = fingerStats(handLms, 'RING')
                        current_state += "1" if ring_status else "0"

                        pinky_status = fingerStats(handLms, 'PINKY')
                        current_state += "1" if pinky_status else "0"

                    # Get user choice
                    user_choice = userMove(current_state)
                    if user_choice == 0:
                        x = 542
                    else:
                        x = 600

                    # computer choice
                    computer_choice = compMove()

                    # Get the winner
                    winner = getWinner(user_choice, computer_choice)

                    # Print choices
                    choices = ["Unknown", "Rock", "Paper", "Scissors"]
                    print(f'\nYou choose {choices[user_choice]}')
                    print(f'Computer choose {choices[computer_choice]}')
                    # print(current_state)
                    print(winner)

                    # Get Computer choice images
                    imgAI = cv2.imread(f'Resources/{computer_choice}.png', cv2.IMREAD_UNCHANGED)

                else:
                    imgAI = cv2.imread(f'Resources/4.png', cv2.IMREAD_UNCHANGED)
                    winner = "No Hand Detected, Try Again"
                    x = 525
                    startGame = False
                    initialTime = time.time()
                    stateResult = True

    if stateResult:
        with col2:
            st.info(str(winner))
            st.image(imgAI, caption="Comp choice", use_column_width=True)

    else:
        if trig == 0:
            st.info("Ready to play?")

    st.info(str(scores[0]))
    st.info(str(scores[1]))

    key = cv2.waitKey(1)
    # Start Game
    if key == 32:
        startGame = True
        initialTime = time.time()
        stateResult = False
        trig += 1
    # Refresh Game
    if key == 8:
        startGame = False
        initialTime = time.time()
        stateResult = False
        scores = [0, 0]
        trig = 0
    # End game
    if key == 27:
        trig = 0

######################################Get video feed######################################################

class VideoProcessor:
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        img = process(img)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

with col1:
    st.header('Column 1')
    webrtc_ctx = webrtc_streamer(
    key="WYH",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True, "audio": False},
    video_processor_factory=VideoProcessor,
    async_processing=True,
)
