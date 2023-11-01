import ctypes
import time
import cv2
import mouse
import keyboard
import pyautogui
import numpy as np
from typing import Union
from lib763.fs import save_str_to_file, rmrf


## CONST
# constant for display size
DISPLAY_SIZE = pyautogui.size()

# constant for display scale
# this is like 1.5, which means "150%" in windows settings
DISPLAY_SCALE = None
try:
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    DISPLAY_SCALE = user32.GetDpiForSystem() / 96.0
except Exception:
    print("Be careful. DISPLAY_SCALE is not set.")
    pass


def screen_shot(save_path=None):
    return pyautogui.screenshot(save_path)


def alert_box(text):
    pyautogui.alert(text)


def type_write(words):
    pyautogui.typewrite(words)


def hotkey(*button, interval=0.1):
    pyautogui.hotkey(button, interval=interval)


def scroll(amount):
    pyautogui.scroll(amount)


def keep_clicking(button="left"):
    mouse.press(button)


def release_clicking(button="left"):
    mouse.release(button)


def move_mouse(coordinate):
    try:
        x, y = coordinate
    except:
        return False
    pyautogui.moveTo(x=x, y=y)


def __validate_coordinate(coordinate):
    try:
        x, y = coordinate
        if not (type(x) == int and type(y) == int):
            raise TypeError(f"coordinate must be (int,int), got ({type(x)},{type(y)})")
        if not (pyautogui.onScreen(x, y)):
            raise ValueError(f"given coordinate is not on screen")
    except:
        raise InvalidCoordinateError("coordinate is invalid")
    return x, y


def image_range_to_coordinate(img_range):
    return (
        (img_range[0] + img_range[2]) / 2,
        (img_range[1] + img_range[3]) / 2,
    )


def click_coordinate(coordinate, count=1):
    x, y = __validate_coordinate(coordinate)
    pyautogui.click(x=x, y=y, clicks=count)


def click_image(img_path, count=1):
    coordinate = get_image_coordinate_on_screen(img_path)
    if coordinate is None:
        return False
    click_coordinate(coordinate, count=count)
    return True


def drag(
    coordinate_ls,
    duration: float = 1,
    left_click: bool = False,
    start_coordinate=None,
) -> None:
    # validate coordinate
    coordinate_ls_mod = []
    if start_coordinate == None:
        # Perform a drag operation on the coordinates given in coordinate_ls.
        start_x, start_y = __validate_coordinate(coordinate_ls[0])
        coordinate_ls_mod = [__validate_coordinate(c) for c in coordinate_ls[1:]]
    else:
        # Perform a drag operation on the coordinates given in coordinate_ls,
        # relative to the start point given in start_coordinate.
        start_x, start_y = __validate_coordinate(start_coordinate)
        before_x, before_y = __validate_coordinate(coordinate_ls[0])
        for c in coordinate_ls[1:]:
            x, y = __validate_coordinate(c)
            coordinate_ls_mod.append((x - before_x, y - before_y))
            before_x, before_y = x, y

    # move mouse to start coordinate
    move_mouse(x=start_x, y=start_y)
    # press and hold the left-click button.
    if left_click:
        keep_clicking(button="left")

    # start to drag
    for x, y in coordinate_ls_mod:
        if start_coordinate == None:
            move_mouse(x=x, y=y, duration=duration)
        else:
            pyautogui.moveRel(x=x, y=y, duration=duration)
    # release the right-click button
    if left_click:
        release_clicking(button="left")


def __read_image(path: str):
    """指定されたパスから画像を読み込む"""
    img = cv2.imread(path)
    if img is None:
        raise ImageReadError(f"Error reading image from path: {path}")
    return img


def image_contains(all_picture_path: str, target_picture_path: str) -> bool:
    template = __read_image(all_picture_path)
    image = __read_image(target_picture_path)
    result = cv2.matchTemplate(image, template, cv2.TM_CCORR_NORMED)
    _, maxVal, _, _ = cv2.minMaxLoc(result)
    return maxVal > 0.99


def is_image_on_screen(target_picture_path):
    screen_shot_path = "./screenshot.png"
    screen_shot(screen_shot_path)
    ret = image_contains(screen_shot_path, target_picture_path)
    rmrf(screen_shot_path)
    return ret


def get_image_coordinate(
    all_picture_path: str, target_picture_path: str
) -> Union[tuple, None]:
    image_range = get_image_range(all_picture_path, target_picture_path)
    if image_range is None:
        return None
    return image_range_to_coordinate(image_range)


def get_image_range(
    all_picture_path: str, target_picture_path: str
) -> Union[tuple, None]:
    template = __read_image(all_picture_path)
    image = __read_image(target_picture_path)
    result = cv2.matchTemplate(image, template, cv2.TM_CCORR_NORMED)
    _, maxVal, _, maxLoc = cv2.minMaxLoc(result)
    if maxVal > 0.99:
        return (
            maxLoc[0],
            maxLoc[1],
            maxLoc[0] + image.shape[1],
            maxLoc[1] + image.shape[0],
        )
    return None


def get_image_coordinate_on_screen(target_picture_path):
    screen_shot_path = "./screenshot.png"
    screen_shot(screen_shot_path)
    ret = get_image_coordinate(screen_shot_path, target_picture_path)
    rmrf(screen_shot_path)
    return ret


def get_all_coordinate_on_screen(target_picture_path):
    ret_ls = []
    screen_shot_path = "./screenshot.png"
    screen_shot(screen_shot_path)
    while True:
        img_range = get_image_range(screen_shot_path, target_picture_path)
        if img_range is None:
            rmrf(screen_shot_path)
            return ret_ls
        ret_ls.append(image_range_to_coordinate(img_range))
        __mask_img(screen_shot_path, img_range)


def __mask_img(target_picture_path, mask_range):
    try:
        x1, y1, x2, y2 = mask_range
    except:
        return False
    img = __read_image(target_picture_path)
    img[x1:x2, y1:y2] = 0
    cv2.imwrite(target_picture_path, img)
    return True


class ImageReadError(Exception):
    """Exception raised for errors in the image reading process."""

    pass


class ImageNotFoundError(Exception):
    """Exception raised when an image is not found within another image."""

    pass


class InvalidCoordinateError(Exception):
    """An exception raised when an invalid coordinate is given."""

    pass


class RecordDrag:
    def __init__(self):
        self.drag_record = []
        self.start_time = 0

    def record_drag_operation(self, save_path: str):
        self.drag_record = []
        self.start_time = time.time()
        mouse.hook(self._record_mouse)

        print("Recording started. Press 'f' to stop recording.")
        keyboard.wait("f")
        mouse.unhook(self._record_mouse)

        save_str_to_file(
            "\n".join([f"{x},{y},{t}" for x, y, t in self.drag_record]), save_path
        )
        print(f"Recording stopped. Saved file: {save_path}")

    def _record_mouse(self, event) -> None:
        self.drag_record.append(
            (event.x, event.y, round(time.time() - self.start_time, 5))
        )
