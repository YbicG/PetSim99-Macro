import pyautogui
import keyboard
import autoit_custom as autoit # Have to use this to compile
from config import X_OFFSET, Y_OFFSET
from collections.abc import Callable, Iterable, Sequence
from typing import Final, NamedTuple, SupportsIndex, SupportsInt, TypeVar
from screeninfo import get_monitors
from time import sleep as wait

def auto_resize(cords: tuple):
    def get_monitor_resolution():
        monitor = get_monitors()[0]
        return (monitor.width, monitor.height)

    original_x, original_y = 2560, 1440
    monitor_resolution = get_monitor_resolution()
    monitor_x, monitor_y = monitor_resolution

    if monitor_x != original_x:
        
        ratio_x = monitor_x / original_x
        ratio_y = monitor_y / original_y
        resized_x = int((cords[0]+X_OFFSET) * ratio_x)
        resized_y = int((cords[1]+Y_OFFSET) * ratio_y)
        return (resized_x, resized_y)
    else:
        ratio_x = monitor_x / original_x
        ratio_y = monitor_y / original_y
        resized_x = int(cords[0] * ratio_x)
        resized_y = int(cords[1] * ratio_y)
        return (resized_x, resized_y)

def down(key: str, duration: int):
    time = 0
    
    while time < duration:
        autoit.send(key)
        time += 0.1
    
class Keybind():
    @staticmethod
    def add(keybind, callback, args=(), suppress=False, timeout=1, trigger_on_release=False):
        keyboard.add_hotkey(keybind, callback, args, suppress, timeout, trigger_on_release)
    
    @staticmethod   
    def remove(keybind):
        keyboard.remove_hotkey(keybind)
        
class Input():
    @staticmethod
    def click(cords=(None, None), button="left", clicks=1, speed=-1) -> None:
        autoit.mouse_click(button, cords[0], cords[1], clicks, speed)
    
    @staticmethod
    def send(send_text: str) -> None:
        autoit.send(send_text)
    
    @staticmethod
    def press(
        keys: str | Iterable[str],
        presses: SupportsIndex = 1,
        interval: float = 0.0,
        logScreenshot: bool | None = None,
        _pause: bool = True,
    ) -> None:
        pyautogui.press(keys, presses, interval, logScreenshot, _pause)
        
    @staticmethod   
    def scroll(clicks, x=None, y=None, logScreenshot=None, _pause=True):
        pyautogui.scroll(clicks, x, y, logScreenshot, _pause)
    
    @staticmethod
    def walk(studs: int, direction: str) -> None:
        conversion = {
            "left": "a", 
            "right": "d", 
            "forward": "w", 
            "backward": "s"
        }
        
        if direction.lower() not in conversion:
            print("Direction isn't left, right, forward, or backward!")
            return None

        key = conversion[direction.lower()]
        
        down(key, studs)
    
    @staticmethod
    def typewrite(
        message: str,
        interval: float = 0.0,
        logScreenshot: bool | None = None,
        _pause: bool = True,
    ) -> None:
        pyautogui.typewrite(message, interval, logScreenshot, _pause)
        
class HomeUICordinates():
    Inventory = auto_resize((1286, 1292))
    AutoFarm = auto_resize((219, 647))
    AutoHatch = auto_resize((81, 636))
    AutoTap = auto_resize((347, 645))
    Hoverboard = auto_resize((341, 506))
    Teleport = auto_resize((215, 515))
    FreeGift = auto_resize((80, 501))
    RankRewards = auto_resize((2374, 996))
    SpecialAbility = auto_resize((772, 1290))
    Exit = auto_resize((1942, 378))

class BottomBarInventoryCords():
    Pets = auto_resize((857, 1292))
    ExclusiveShop = auto_resize((999, 1289))
    Achievements = auto_resize((1145, 1288))
    Trading = auto_resize((1283, 1288))
    Clans = auto_resize((1430, 1291))
    Mastery = auto_resize((1583, 1302))
    Settings = auto_resize((1716, 1291))

class SideBarInventoryCords():
    Pets = auto_resize((566, 480))
    Items = auto_resize((566, 555))
    Potions = auto_resize((566, 640))
    Enchants = auto_resize((566, 706))
    Ultimates = auto_resize((566, 786))
    Hoverboards = auto_resize((563, 868))
    Eggs = auto_resize((561, 944))
    Booths = auto_resize((565, 1019))

class InventoryCords():
    SeachBar = auto_resize((1777, 373))
    FirstItem = auto_resize((695, 530))
    Ok = auto_resize((1277, 966))
    Exit = auto_resize((1942, 378))
    
class PotionCords():
    FirstItem = auto_resize((704, 473))
    
class TeleportCords():
    SearchBar = auto_resize((1757, 372))
    FirstItem = auto_resize((1275, 491))
    Ok = auto_resize((1281, 968))
    Exit = auto_resize((1943, 375))
    
class HatchingCords():
    BuyMost = auto_resize((1566, 981))