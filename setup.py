from setuptools import setup, find_packages

setup(
    name="lib763",
    version="0.4.12",
    description="naru's library",
    author="naru",
    license="MIT",
    install_requires=[
        "paramiko",
        "scp",
        "chardet",
        "opencv-python",  # cv2 is provided by opencv-python
        "keyboard",
        "mouse",
        "pyperclip",
        "pyautogui",
    ],
)
