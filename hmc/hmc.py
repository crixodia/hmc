"""
Author: Cristian Bastidas

Date: 2020-03-01
"""

from ast import Try
from json import dump, load
from os import _exit
from sys import exit
from time import sleep, time
from tkinter import HORIZONTAL, Button, Label, Scale, Tk

from cv2 import (
    COLOR_BGR2RGB,
    FONT_HERSHEY_SIMPLEX,
    INTER_NEAREST,
    VideoCapture,
    cvtColor,
    putText
)

from cv2 import resize as cv2_resize
from imutils import resize
from imutils.video import VideoStream
from keyboard import is_pressed
from numpy import argmax, array, float32, interp, ndarray, set_printoptions
from PIL import Image, ImageTk
from pyautogui import press

import tensorflow as tf

set_printoptions(suppress=True)

# BASIC VARIABLES
interpreter = tf.lite.Interpreter(model_path="models/hmc.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


CLASS_NAMES = ["nexttrack", "none", "playpause", "prevtrack"]
TOLERANCES = [0.93, 0.0, 0.91, 0.91]
TIME_GAP = 0.6
CAMERA = 0
VERBOSE = True
DISPLAY = True

# MAIN WINDOW
win = Tk()
win.title("Hand Music Controller")
win.iconbitmap('icon.ico')
win.geometry("504x550")
win.resizable(False, False)


label = Label(win)
next_slider = Scale(
    win, from_=70, to=99, orient=HORIZONTAL, label="Next Track [%]", length=220)
none_slider = Scale(
    win, from_=0, to=99, orient=HORIZONTAL, label="None [%]", length=220
)
play_slider = Scale(
    win, from_=70, to=99, orient=HORIZONTAL, label="Play/Pause [%]", length=220
)
prev_slider = Scale(
    win, from_=70, to=99, orient=HORIZONTAL, label="Previous Track [%]", length=220
)
time_slider = Scale(
    win, from_=1, to=10, orient=HORIZONTAL, label="Time Gap [ds]", length=220
)

label.place(x=0, y=0)
next_slider.place(x=10, y=300)
none_slider.place(x=266, y=300)
play_slider.place(x=10, y=370)
prev_slider.place(x=266, y=370)
time_slider.place(x=10, y=440)

cap = VideoStream(src=CAMERA)


def list_cameras():
    """
    Lists the available cameras
    """
    index = 0
    arr = []
    while True:
        cap = VideoCapture(index)
        if not cap.read()[0]:
            break
        arr.append(index)
        cap.release()
        index += 1
    return arr


def reload_camera(var=None):
    """
    Reloads the camera
    """
    global CAMERA, cap
    cap.stop()
    try:
        CAMERA = camera_select.get()
        print(CAMERA)
    except:
        CAMERA = 0
    cap = VideoStream(src=CAMERA).start()


def save_config():
    """
    Saves the configuration file
    """
    print("Saving configuration")
    data = {
        "tolerances": {
            "nexttrack": next_slider.get()/100,
            "none": none_slider.get()/100,
            "playpause": play_slider.get()/100,
            "prevtrack": prev_slider.get()/100
        },
        "time_gap": time_slider.get()/10,
        "verbose": VERBOSE,
        "camera": CAMERA,
        "display": DISPLAY
    }
    with open('config.json', 'w') as outfile:
        dump(data, outfile)
    print("Done!")


def set_sliders():
    """
    Sets the sliders to the loaded values
    """
    next_slider.set(TOLERANCES[0]*100)
    none_slider.set(TOLERANCES[1]*100)
    play_slider.set(TOLERANCES[2]*100)
    prev_slider.set(TOLERANCES[3]*100)
    time_slider.set(TIME_GAP*10)


def load_config():
    """
    Loads the configuration file
    """
    global TOLERANCES, TIME_GAP, VERBOSE, CAMERA, DISPLAY
    print("Loading configuration")
    data = None
    try:
        f = open('config.json')
        data = load(f)
        f.close()

        TOLERANCES = list(data["tolerances"].values())
        TIME_GAP = data["time_gap"]
        VERBOSE = data["verbose"]
        CAMERA = data["camera"]
        DISPLAY = data["display"]

        set_sliders()
        reload_camera()

        print("Done!")
    except:
        print('config.json was not found')


def save_and_load():
    """
    Saves and reloads the configuration file
    """
    save_config()
    load_config()


def hide_window():
    """
    Hides the window
    """
    win.withdraw()


camera_select = Scale(
    win, from_=0, to=len(list_cameras()), orient=HORIZONTAL, label="Camera", length=220, command=reload_camera
)

apply_button = Button(win, text="Apply", command=save_and_load)
hide_button = Button(win, text="Hide", command=hide_window)
exit_button = Button(win, text="Exit", command=exit)

camera_select.place(x=266, y=440)
apply_button.place(x=10, y=510)
hide_button.place(x=70, y=510)
exit_button.place(x=125, y=510)


def main():
    """
    Main function
    """
    data = ndarray(shape=(1, 224, 224, 3), dtype=float32)
    size = (224, 224)  # Size of the image
    font_color = (0, 0, 255)

    start = time()
    img = resize(cap.read(), width=500)

    height, width, _ = img.shape
    scale_value = width/height

    # Resize the image
    img_resized = cv2_resize(
        img,
        size,
        fx=scale_value,
        fy=1,
        interpolation=INTER_NEAREST
    )

    img_array = array(img_resized)

    normalized_img_array = (img_array.astype(float32) / 127.0) - 1

    data[0] = normalized_img_array
    interpreter.set_tensor(input_details[0]['index'], data)
    interpreter.invoke()

    prediction = interpreter.get_tensor(output_details[0]['index'])

    index = argmax(prediction)
    class_name = CLASS_NAMES[index]
    confidence_score = prediction[0][index]

    # Confidence score
    if class_name != "none" and confidence_score > TOLERANCES[index]:
        print(class_name, confidence_score)
        press(class_name)
        sleep(TIME_GAP)  # Wait for the hand to be released
        # Green if the prediction was correct based on the confidence score
        font_color = (0, 255, 0)

    end = time()
    fps = 0
    if end - start == 0:
        raise Exception("ZeroFPS: The camera is not working fine")
    else:
        fps = 1/(end - start)

    # FPS
    putText(
        img, f"FPS: {int(fps)}", (10, 30),
        FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2
    )

    # Prediction
    putText(
        img, f"Class: {class_name} {index}", (10, 60),
        FONT_HERSHEY_SIMPLEX, 0.5, font_color, 2
    )

    # Confidence score
    putText(
        img, f"Confidence: {int(confidence_score*100)}%", (10, 90),
        FONT_HERSHEY_SIMPLEX, 0.5, font_color, 2
    )

    # Processed image
    img = Image.fromarray(cvtColor(img, COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)

    # If Shift + Alt + D is pressed, the window will be hidden or shown
    if is_pressed('shift') and is_pressed('alt') and is_pressed('d'):
        if win.winfo_viewable():
            win.withdraw()
        else:
            win.deiconify()

    # Sets the image to the label
    label.imgtk = imgtk
    label.configure(image=imgtk)

    # Updates the window
    label.after(20, main)


if __name__ == "__main__":
    try:
        load_config()
        main()
        win.mainloop()
    except:
        print("Interrupted")
        try:
            exit(0)
        except SystemExit:
            _exit(0)
