"""
Made by YbicG (@ybicg)
©️ 2024 All Rights Reserved. Unauthorized redistribution or modification of this program is illegal and can have legal consequences.
"""
import petsim.api as api
import definitions as macro
import keyboard
import threading
import os
from config import *
from time import sleep as wait
from definitions import Input, Keybind, HomeUICordinates, BottomBarInventoryCords, SideBarInventoryCords, InventoryCords, TeleportCords, HatchingCords, PotionCords
from petsim.api import Clan, ActiveClanBattle
from petsim.api.subclasses import BattleGoal

# You can use Ctrl+Alt+P to stop the program.

RUNNING = True
AUTOFARM_ENABLED = False

CURRENT_GOAL = 4

LAST_AREA = "Dominus Vault"
FIRST_AREA = "Tech Spawn"

QUESTS = {
    "7": "Earn Diamonds",
    "9": "Break Diamond Breakables",
    "12": "Craft Tier 3 Potions",
    "13": "Craft Tier III Enchants",
    "20": "Hatch Best Eggs",
    "21": "Break Breakables in Best Area",
    "25": "Find chests in the Digsite",
    "26": "Catch fish in the Fishing Minigame",
    "27": "Ice Obby Completions",
    "28": "Complete the Pyramid Obby",
    "29": "Complete the Jungle Obby",
    "34": "Use Tier 4 Potions",
    "35": "Use Fruits",
    "36": "Complete the Sled Race",
    "37": "Break Coin Jars in Best Area",
    "38": "Break Comets in Best Area",
    "39": "Break Mini-Chests in Best Area",
    "40": "Make Golden Pets from Best Egg",
    "41": "Make Rainbow Pets from Best Egg",
    "42": "Hatch Rare \"??\" Pets",
    "43": "Break Piñatas in Best Area",
    "44": "Break Lucky Blocks in Best Area",
    "45": "Find Chests in Advanced Digsite",
    "46": "Catch Fish in Advanced Fishing",
    "73": "Break breakables in Treasure Hideout",
    "74": "Consume XP Potions"
}

MACROABLE = [
    "7",    # Earn Diamonds - Done
    "9",    # Break Diamond Breakables - Done
    "20",   # Hatch Best Eggs - Done
    "21",   # Break Breakables in Best Area - Done
    "34",   # Use Tier 4 Potions - Done
    "35",   # Use Fruits - Done
    "39",   # Break Mini-Chests in Best Area - Done
    "37",   # Break Coin Jars in Best Area - Done
    "38",   # Break Comets in Best Area - Done
    "43",   # Break Piñatas in Best Area - Done
    "44",   # Break Lucky Blocks in Best Area - Done
    "42",   # Hatch Rare "???" Pets - Done
    "74"    # Consume XP Potions -
]

# Helper Functions
def on_key_event(event):
    global RUNNING
    if event.name == 'p' and keyboard.is_pressed('ctrl') and keyboard.is_pressed('alt'):
        RUNNING = False
        print("Exiting the macro...")
        keyboard.unhook_all()
        os._exit(os.EX_OK)

def Goal3() -> BattleGoal:
    clan = Clan("EXP")
    goal = clan.CurrentBattle.Goal3
    
    return goal

def Goal4() -> BattleGoal:
    clan = Clan("EXP")
    goal = clan.CurrentBattle.Goal4
    
    return goal

def quest_name(goal: BattleGoal) -> str:
        if str(goal.TypeID) in QUESTS:
            return QUESTS[str(goal.TypeID)]
        else:
            return None

def is_macroable(goal: BattleGoal) -> bool:
    if not quest_name(goal):
        return False
    
    return True if str(goal.TypeID) in MACROABLE else False

def teleport(area: str):
    Input.click(HomeUICordinates.Teleport)
    wait(1)
    Input.click(TeleportCords.SearchBar, clicks=2)
    wait(.5)
    Input.typewrite(area)
    wait(1)
    Input.click((100, 100))
    wait(.5)
    Input.click(TeleportCords.FirstItem, clicks=3) # Clicking more than once in case it doesn't register
    wait(.5)
    Input.click(TeleportCords.Ok)
    wait(.5)
    Input.click(TeleportCords.Ok)
    wait(.5)
    Input.click(TeleportCords.Exit)

ACTIVE_ITEMS = {
    "Basic Coin Jar": False,
    "Comet": False,
    "Lucky Block": False,
    "ata": False,
}

def use_item(name):
    global ACTIVE_ITEMS
    
    ACTIVE_ITEMS[name] = True
    
    def execute():
        print(f"[{name if name != "ata" else "Piñata"}] Starting Thread...\n")
        while ACTIVE_ITEMS[name]:
            Input.click(HomeUICordinates.Inventory)
            wait(.5)
            Input.click(SideBarInventoryCords.Items)
            wait(.5)
            Input.click(InventoryCords.SeachBar)
            wait(.5)
            Input.typewrite(name)
            wait(.5)
            Input.click(InventoryCords.FirstItem)
            wait(.5)
            Input.click(InventoryCords.Ok)
            wait(.5)
            Input.click(InventoryCords.Exit)
            
            wait(ITEM_SPAWN_DELAY)
        
        print(f"[{name if name != "ata" else "Piñata"}] Exiting Thread...\n")
    
    thread = threading.Thread(name=name, target=execute)
    
    thread.start()
    
    return thread

ACTIVE_POTIONS = False

def use_potions():
    global ACTIVE_POTIONS
    
    ACTIVE_POTIONS = True
    
    def execute():
        print("[IV Potions] Starting Thread...\n")
    
        for i in range(10):
            if not ACTIVE_POTIONS:
                break
            
            Input.click(HomeUICordinates.Inventory)
            wait(.5)
            Input.click(SideBarInventoryCords.Potions)
            wait(.5)
            Input.click(InventoryCords.SeachBar)
            wait(.5)
            Input.typewrite(IV_POTION)
            wait(.5)
                    
            for potion in range(round(MAXIMUM_POTION_USAGE/10)):
                Input.click(PotionCords.FirstItem)
                wait(.03)   
                    
            wait(.5)
            Input.click(InventoryCords.Exit)
                
            wait(ITEM_SPAWN_DELAY) 
                
        
        print("[IV Potions] Exiting Thread...\n")
            
    thread = threading.Thread(name="Active Potions", target=execute)
        
    thread.start()
    
    return thread
        
# Main Loop
wait(2)

def switch(name, goal: BattleGoal, current_goal_id):
    global ACTIVE_ITEMS, ACTIVE_POTIONS, AUTOFARM_ENABLED
    
    print("Current Quest: "+name)
    
    match name:
        case "Break Diamond Breakables":
            if not EARN_DIAMOND_BREAKABLES_ENABLED:
                return
            
            teleport(LAST_AREA)
            wait(TELEPORT_DELAY)
            teleport(FIRST_AREA)
            wait(TELEPORT_DELAY)
            Input.click(HomeUICordinates.Hoverboard)
            wait(1)
            
            Input.walk(35, "left")
            Input.walk(8, "forward")
            Input.walk(21, "left")
            wait(.5)
            
            Input.click(HomeUICordinates.Exit) # Just in case it goes over the gold maker by accident
            wait(.5)
            
            if AUTOFARM_ENABLED:
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = False
                wait(1)
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = True
            else:
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = True
            
            active = True
                        
            while active:
                try:
                    if current_goal_id == 3:
                        goal = Goal3()
                    else:
                        goal = Goal4()
                        
                    if quest_name(goal) == name:
                        print(f"[{name}] Quest is active! ({goal.Progress}/{goal.Amount})")
                        wait(ACTIVE_CHECK_INTERVAL)
                    else:
                        print(f"[{name}] Quest isn't active!")
                        active = False
                except:
                    print(f"[{name}] Error connecting to the server!")
                    wait(ACTIVE_CHECK_INTERVAL)
                    
        case "Use Tier 4 Potions":
            if not USE_IV_POTIONS_ENABLED:
                return
            
            active = True
            
            potion_thread = use_potions()
                        
            while active:
                try:
                    if current_goal_id == 3:
                        goal = Goal3()
                    else:
                        goal = Goal4()
                        
                    if quest_name(goal) == name:
                        print(f"[{name}] Quest is active! ({goal.Progress}/{goal.Amount})")
                        wait(ACTIVE_CHECK_INTERVAL)
                    else:
                        print(f"[{name}] Quest isn't active!")
                        ACTIVE_POTIONS = False
                        active = False
                        
                        potion_thread.join()
                except:
                    print(f"[{name}] Error connecting to the server!")
                    wait(ACTIVE_CHECK_INTERVAL)

        case "Use Fruits":
            if not USE_FRUITS_ENABLED:
                return
            
            active = True
            
            for fruit in FRUITS:
                Input.click(HomeUICordinates.Inventory)
                wait(.5)
                Input.click(SideBarInventoryCords.Items)
                wait(.5)
                Input.click(InventoryCords.SeachBar)
                wait(.5)
                Input.typewrite(fruit)
                wait(.5)
                
                for fruit in range(MAXIMUM_FRUIT_USAGE_EACH):
                    Input.click(InventoryCords.FirstItem)
                    wait(.05)
                    
                wait(1)
                Input.click(InventoryCords.Ok)
                wait(.5)
                Input.click(InventoryCords.Exit)
                wait(1)
                        
            while active:
                try:
                    if current_goal_id == 3:
                        goal = Goal3()
                    else:
                        goal = Goal4()
                        
                    if quest_name(goal) == name:
                        print(f"[{name}] Quest is active! ({goal.Progress}/{goal.Amount})")
                        wait(ACTIVE_CHECK_INTERVAL)
                    else:
                        print(f"[{name}] Quest isn't active!")
                        active = False
                except:
                    print(f"[{name}] Error connecting to the server!")
                    wait(ACTIVE_CHECK_INTERVAL)
                    
        case "Break Lucky Blocks in Best Area":
            if not BREAK_LUCKY_BLOCKS_ENABLED:
                return
            
            teleport(FIRST_AREA)
            wait(TELEPORT_DELAY)
            teleport(LAST_AREA)
            wait(TELEPORT_DELAY)
            Input.walk(25, "right")
            wait(.5)
            
            if AUTOFARM_ENABLED:
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = False
                wait(1)
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = True
            else:
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = True
            
            active = True
            
            item = "Lucky Block"
            
            item_thread = use_item(item)
                        
            while active:
                try:
                    if current_goal_id == 3:
                        goal = Goal3()
                    else:
                        goal = Goal4()
                        
                    if quest_name(goal) == name:
                        print(f"[{name}] Quest is active! ({goal.Progress}/{goal.Amount})")
                        wait(ACTIVE_CHECK_INTERVAL)
                    else:
                        print(f"[{name}] Quest isn't active!")
                        
                        ACTIVE_ITEMS[item] = False
                        active = False
                        
                        item_thread.join()
                except:
                    print(f"[{name}] Error connecting to the server!")
                    wait(ACTIVE_CHECK_INTERVAL)
                    
        case "Break Piñatas in Best Area":
            if not BREAK_PINATAS_ENABLED:
                return
            
            teleport(FIRST_AREA)
            wait(TELEPORT_DELAY)
            teleport(LAST_AREA)
            wait(TELEPORT_DELAY)
            Input.walk(25, "right")
            wait(.5)
            
            if AUTOFARM_ENABLED:
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = False
                wait(1)
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = True
            else:
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = True
            
            active = True
            
            item = "ata" # Can't use Piñata because the ene doesn't show up
            
            item_thread = use_item(item)
                        
            while active:
                try:
                    if current_goal_id == 3:
                        goal = Goal3()
                    else:
                        goal = Goal4()
                        
                    if quest_name(goal) == name:
                        print(f"[{name}] Quest is active! ({goal.Progress}/{goal.Amount})")
                        wait(ACTIVE_CHECK_INTERVAL)
                    else:
                        print(f"[{name}] Quest isn't active!")
                        
                        ACTIVE_ITEMS[item] = False
                        active = False
                        
                        item_thread.join()
                except:
                    print(f"[{name}] Error connecting to the server!")
                    wait(ACTIVE_CHECK_INTERVAL)
                    
        case "Break Comets in Best Area":
            if not BREAK_COMETS_ENABLED:
                return
            
            teleport(FIRST_AREA)
            wait(TELEPORT_DELAY)
            teleport(LAST_AREA)
            wait(TELEPORT_DELAY)
            Input.walk(25, "right")
            wait(.5)
            
            if AUTOFARM_ENABLED:
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = False
                wait(1)
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = True
            else:
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = True
            
            active = True
            
            item = "Comet"
            
            item_thread = use_item(item)
                        
            while active:
                try:
                    if current_goal_id == 3:
                        goal = Goal3()
                    else:
                        goal = Goal4()

                    if quest_name(goal) == name:
                        print(f"[{name}] Quest is active! ({goal.Progress}/{goal.Amount})")
                        wait(ACTIVE_CHECK_INTERVAL)
                    else:
                        print(f"[{name}] Quest isn't active!")
                        
                        ACTIVE_ITEMS[item] = False
                        active = False
                        
                        item_thread.join()
                except:
                    print(f"[{name}] Error connecting to the server!")
                    wait(ACTIVE_CHECK_INTERVAL)
                
        case "Break Coin Jars in Best Area":
            if not BREAK_COIN_JARS_ENABLED:
                return
            
            teleport(FIRST_AREA)
            wait(TELEPORT_DELAY)
            teleport(LAST_AREA)
            wait(TELEPORT_DELAY)
            Input.walk(25, "right")
            wait(.5)

            if AUTOFARM_ENABLED:
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = False
                wait(1)
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = True
            else:
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = True
            
            active = True
            
            item = "Basic Coin Jar"
            
            item_thread = use_item(item)
                        
            while active:
                try:
                    if current_goal_id == 3:
                        goal = Goal3()
                    else:
                        goal = Goal4()

                    if quest_name(goal) == name:
                        print(f"[{name}] Quest is active! ({goal.Progress}/{goal.Amount})")
                        wait(ACTIVE_CHECK_INTERVAL)
                    else:
                        print(f"[{name}] Quest isn't active!")
                        
                        ACTIVE_ITEMS[item] = False
                        active = False
                        
                        item_thread.join()
                except:
                    print(f"[{name}] Error connecting to the server!")
                    wait(ACTIVE_CHECK_INTERVAL)
                    
                
        case "Break Mini-Chests in Best Area":
            if not BREAK_MINI_CHESTS_ENABLED:
                return

            teleport(FIRST_AREA)
            wait(TELEPORT_DELAY)
            teleport(LAST_AREA)
            wait(TELEPORT_DELAY)
            Input.walk(25, "right")
            wait(.5)
            
            if AUTOFARM_ENABLED:
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = False
                wait(1)
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = True
            else:
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = True
            
            active = True
                        
            while active:
                try:
                    if current_goal_id == 3:
                        goal = Goal3()
                    else:
                        goal = Goal4()
                        
                    if quest_name(goal) == name:
                        print(f"[{name}] Quest is active! ({goal.Progress}/{goal.Amount})")
                        wait(ACTIVE_CHECK_INTERVAL)
                    else:
                        print(f"[{name}] Quest isn't active!")
                        active = False
                except:
                    print(f"[{name}] Error connecting to the server!")
                    wait(ACTIVE_CHECK_INTERVAL)
                
        case "Earn Diamonds":
            if not EARN_DIAMONDS_ENABLED:
                return
            
            teleport(FIRST_AREA)
            wait(TELEPORT_DELAY)
            teleport(LAST_AREA)
            wait(TELEPORT_DELAY)
            Input.walk(25, "right")
            wait(.5)
            
            if AUTOFARM_ENABLED:
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = False
                wait(1)
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = True
            else:
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = True
            
            active = True
                        
            while active:
                try:
                    if current_goal_id == 3:
                        goal = Goal3()
                    else:
                        goal = Goal4()
                        
                    if quest_name(goal) == name:
                        print(f"[{name}] Quest is active! ({goal.Progress}/{goal.Amount})")
                        wait(ACTIVE_CHECK_INTERVAL)
                    else:
                        print(f"[{name}] Quest isn't active!")
                        active = False
                except:
                    print(f"[{name}] Error connecting to the server!")
                    wait(ACTIVE_CHECK_INTERVAL)
                
        case "Break Breakables in Best Area":
            if not BREAK_BREAKABLES_BEST_AREA_ENABLED:
                return
            
            teleport(FIRST_AREA)
            wait(TELEPORT_DELAY)
            teleport(LAST_AREA)
            wait(TELEPORT_DELAY)
            Input.walk(25, "right")
            wait(.5)
            
            if AUTOFARM_ENABLED:
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = False
                wait(1)
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = True
            else:
                Input.click(HomeUICordinates.AutoFarm)
                AUTOFARM_ENABLED = True
            
            active = True
                        
            while active:
                try:
                    if current_goal_id == 3:
                        goal = Goal3()
                    else:
                        goal = Goal4()

                    if quest_name(goal) == name:
                        print(f"[{name}] Quest is active! ({goal.Progress}/{goal.Amount})")
                        wait(ACTIVE_CHECK_INTERVAL)
                    else:
                        print(f"[{name}] Quest isn't active!")
                        active = False
                except:
                    print(f"[{name}] Error connecting to the server!")
                    wait(ACTIVE_CHECK_INTERVAL)
            
        case "Hatch Best Eggs":
            if not HATCH_BEST_EGGS_ENABLED:
                return

            teleport(LAST_AREA)
            wait(TELEPORT_DELAY)
            teleport(FIRST_AREA)
            wait(TELEPORT_DELAY)
            Input.click(HomeUICordinates.Hoverboard)
            wait(1)
            Input.walk(14, "right")
            Input.walk(26, "backward")
            Input.walk(16.5, "left")
            wait(.5)
            Input.send("e")
            Input.click(HatchingCords.BuyMost)
                        
            active = True
                        
            while active:
                try:
                    if current_goal_id == 3:
                        goal = Goal3()
                    else:
                        goal = Goal4()
                        
                    if quest_name(goal) == name:
                        print(f"[{name}] Quest is active! ({goal.Progress}/{goal.Amount})")
                        wait(ACTIVE_CHECK_INTERVAL)
                    else:
                        print(f"[{name}] Quest isn't active!")
                        Input.walk(27, "forward")
                        active = False
                except:
                    print(f"[{name}] Error connecting to the server!")
                    wait(ACTIVE_CHECK_INTERVAL)
                
        case "Hatch Rare \"??\" Pets":
            if not HATCH_RARE_PETS_ENABLED:
                return
            
            teleport(LAST_AREA)
            wait(TELEPORT_DELAY)
            teleport(FIRST_AREA)
            wait(TELEPORT_DELAY)
            Input.click(HomeUICordinates.Hoverboard)
            wait(1)
            Input.walk(14, "right")
            Input.walk(26, "backward")
            Input.walk(16.5, "left")
            wait(.5)
            Input.send("e")
            Input.click(HatchingCords.BuyMost)
                        
            active = True
                        
            while active:
                try:
                    if current_goal_id == 3:
                        goal = Goal3()
                    else:
                        goal = Goal4()
                        
                    if quest_name(goal) == name:
                        print(f"[{name}] Quest is active! ({goal.Progress}/{goal.Amount})")
                        wait(ACTIVE_CHECK_INTERVAL)
                    else:
                        print(f"[{name}] Quest isn't active!")
                        Input.walk(27, "forward")
                        active = False
                except:
                    print(f"[{name}] Error connecting to the server!")
                    wait(ACTIVE_CHECK_INTERVAL)

def main():
    global CURRENT_GOAL
    
    keyboard.on_press(on_key_event)
    # Click in case not tabbed in
    Input.click((100, 100))
    
    teleport(LAST_AREA)
    wait(TELEPORT_DELAY)
    teleport(FIRST_AREA)
    wait(TELEPORT_DELAY)
    Input.click(HomeUICordinates.Hoverboard)
    
    while RUNNING == True:
        try:
            main_goal = Goal4()
            secondary_goal = Goal3()
            
            # Alternate between Goal 3 and 4 so there is nice variety
            if CURRENT_GOAL == 4:
                if is_macroable(main_goal):
                    CURRENT_GOAL = 3
                    name = quest_name(main_goal)
        
                    switch(name, main_goal, 4)
                        
                else:
                    print("Couldn't find a valid quest in Goal 4. Current Type: ", main_goal.TypeID)
                    CURRENT_GOAL = 3
                        
            elif CURRENT_GOAL == 3:
                if is_macroable(secondary_goal):    
                    CURRENT_GOAL = 4
                    name = quest_name(secondary_goal) 
    
                    switch(name, secondary_goal, 3)
            
                else:
                    print("Couldn't find a valid quest in Goal 3. Current Type: ", secondary_goal.TypeID)
                    CURRENT_GOAL = 4
            else:
                print("Couldn't find a valid goal.")
                
            wait(5)
        except:
            print(f"[{name}] Error connecting to the server! Retrying in 5s...")
            wait(5)

if __name__ == "__main__":
    main()

print("Exiting the macro...")
keyboard.unhook_all()

"""
©️ 2024 All Rights Reserved. Unauthorized redistribution or modification of this program is illegal and can have legal consequences.
"""