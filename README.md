# 🎶 Hand Music Changer ✋👈✊
Hand Music Changer is a tool for changing the music with your hands trough your camera. It uses a CNN to detect your hand and change the music.

- [🎶 Hand Music Changer ✋👈✊](#-hand-music-changer-)
  - [Download](#download)
  - [How to use it?](#how-to-use-it)
    - [Hide/Show GUI](#hideshow-gui)
  - [Hand signs](#hand-signs)
  - [Configuration](#configuration)
    - [Tolerances](#tolerances)
    - [Selected camera](#selected-camera)
    - [Time gap](#time-gap)
  - [Build an executable](#build-an-executable)

## Download

You can download the latest version of Hand Music Changer from [GitHub](https://github.com/crixodia/hmc/releases)

## How to use it?

You must use **Python 3** for the entire project.

There are a lot of requirements to use it due to there is no executable file created yet. Those requierements can be installed with pip as follows:

```shell
python -m pip install imutils keyboard numpy opencv-python pillow pyautogui tensorflow
```

Or just install the [requirements.txt](https://github.com/crixodia/hmc/blob/main/hmc/requirements.txt) file.

```shell
python -m pip install -r requirements.txt
```

Then, execute the following command to start the app:

```shell
python ./hmc.py
```

### Hide/Show GUI

There is a button to hide the camera feed. You must use `Ctrl+Alt+Shift+D` to show/hide the GUI. So it will not distract you.

## Hand signs

|         Play/Pause ✋         |     Next song 👈      |     Previous song ✊      |
| :--------------------------: | :------------------: | :----------------------: |
| ![](./assets/play_pause.jpg) | ![](assets/next.jpg) | ![](assets/previous.jpg) |

It is worth say that it does not matter if you flip the gesture, it will work because of the data augmentation during training.

## Configuration
Certainly there are a variety of environments to use the app. That is why there are some configuration options.

<img src="./assets/preview.gif" style="display:block; margin:auto; width:400px;">

### Tolerances
You can adjust the tolerances and the time gap to make the app more accurate. For instance, if `play/pause` does not work properly, you can try decreasing the tolerance for this hand sign, so it will be triggered with less confidence score. But, if the app suddenly changes or pauses the song you should increase the required confidence score to trigger the action.

### Selected camera
You are able to change the camera that is used to capture the video. The default camera is the first one. With this option you can use other camera for other purposes and other one dedicated to the app.

### Time gap
Finally, you can change the time between actions. This is useful whether you want to trigger the action too often or not.

## Build an executable
It is a official release coming soon. Meanwhile you can create an executable using [pyinstaller](https://pyinstaller.org/en/stable/). The [specs](https://github.com/crixodia/hmc/blob/main/hmc/HandMusicChanger.spec) are already defined, just execute the following command:

```shell
pyinstaller HandMusicChanger.spec hmc.py
```
