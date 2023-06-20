import time
import keyboard as kb
import mouse
import pyperclip
from PIL import ImageGrab
import ctypes

class mouse_keyboard:
    def __init__(self, wait_time=0.5) -> None:
        """
        コンストラクタ
        @param:
            wait_time: (float) 待機時間
        """
        self.wait_time = wait_time
        self.display_scale = self.__get_display_scale()

    def __get_display_scale(self) -> float:
        """
        ディスプレイのスケールを取得する
        @return:
            (float): ディスプレイのスケール値
        """
        try:
            user32 = ctypes.windll.user32
            user32.SetProcessDPIAware()
            return user32.GetDpiForSystem() / 96.0
        except Exception as e:
            print("Error:", e)
            return None

    def __adjust_coordinate(self, coordinate: tuple) -> tuple:
        """
        座標をディスプレイスケールに合わせて調整する
        @param:
            coordinate: (tuple) 入力座標 (x, y)
        @return:
            (tuple): 調整された座標 (x, y)
        """
        return coordinate[0] // self.display_scale, coordinate[1] // self.display_scale

    def kb_input(self, input_str: str) -> None:
        """
        キーボード入力をシミュレートする
        @param:
            input_str: (str) 入力文字列
        """
        kb.press_and_release(input_str)
        time.sleep(self.wait_time)

    def write_word(self, word: str) -> None:
        """
        クリップボードに文字列をコピーして貼り付ける
        @param:
            word: (str) 貼り付ける文字列
        """
        self.copy_to_clipboard(word)
        self.kb_input("ctrl+v")
        time.sleep(self.wait_time)

    def backspace(self, times: int):
        """
        バックスペースキーを指定回数押す
        @param:
            times: (int) バックスペースキーを押す回数
        """
        for _ in range(times):
            kb.press_and_release("backspace")
        time.sleep(self.wait_time)

    def __move_mouse(self, x: float, y: float) -> None:
        """
        マウスを指定座標に移動する
        @param:
            x: (float) x座標
            y: (float) y座標
        """
        mouse.move(x, y, absolute=True, duration=0)
        time.sleep(self.wait_time)

    def move_mouse(self, coordinate: tuple) -> None:
        """
        マウスを指定座標に移動する
        @param:
            coordinate: (tuple) 移動先座標 (x, y)
        """
        coord = self.__adjust_coordinate(coordinate)
        self.__move_mouse(float(coord[0]), float(coord[1]))

    def click(self) -> None:
        """
        マウス左ボタンをクリックする
        """
        mouse.click("left")
        time.sleep(self.wait_time)

    def click_coordinate(self, coordinate: tuple) -> None:
        """
        マウスを指定座標に移動してクリックする
        @param:
            coordinate: (tuple) クリック座標 (x, y)
        """
        self.move_mouse(coordinate)
        self.click()

    def scroll(self) -> None:
        """
        マウススクロールを行う
        """
        mouse.wheel(-1)
        time.sleep(self.wait_time)

    def get_screen_shot(self, path: str) -> None:
        """
        スクリーンショットを撮影して保存する
        @param:
            path: (str) 保存先のファイルパス
        """
        ImageGrab.grab().save(path)
        time.sleep(self.wait_time)

    def get_clipboard_str(self) -> None:
        """
        クリップボードから文字列を取得する
        @return:
            (str): クリップボードの文字列
        """
        return pyperclip.paste()

    def copy_to_clipboard(self, word: str) -> None:
        """
        文字列をクリップボードにコピーする
        @param:
            word: (str) コピーする文字列
        """
        return pyperclip.copy(word)
