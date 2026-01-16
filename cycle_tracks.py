import pyautogui
import json
import time
import os
import shutil
import re
import glob

TM_FOLDER = "/home/adrien/Documents/TmForever/Tracks/Replays/Kacky/"
SCRIPTS_FOLDER = "/home/adrien/Documents/TMInterface/Scripts/"

REPLAYS_DIR = "Replays"
INPUTS_DIR = "Inputs"

with open("points.json", "r") as f:
    points = json.load(f)

def press(key):
    x = points[key]["x"]
    y = points[key]["y"]
    pyautogui.moveTo(x, y, duration=0.02)
    time.sleep(0.1)
    pyautogui.press("enter")

def load_map():
    press("refresh")
    time.sleep(0.1)
    press("select_replay")
    time.sleep(0.1)
    press("launch")
    time.sleep(0.1)
    press("play")


# time.sleep(3)
# load_map()

# time.sleep(10)
# back_to_menu()

def clear_folder(folder):
    for name in os.listdir(folder):
        path = os.path.join(folder, name)
        os.remove(path)


time.sleep(3)

for map_name in sorted(os.listdir(REPLAYS_DIR)):
    print(f"Map : {map_name}")
    number = int(map_name[14:-11])

    # Load into Map
    clear_folder(TM_FOLDER)
    shutil.copy(os.path.join(REPLAYS_DIR, map_name), os.path.join(TM_FOLDER, map_name))
    time.sleep(1)
    load_map()

    pattern = os.path.join(INPUTS_DIR, f"kk{number}_*.txt")

    matches = glob.glob(pattern)

    if not matches:
        print(f"Can't find inputs for map {map_name} : no file matching {pattern}")
        exit(0)

    input_file = matches[0]

    filename = os.path.basename(input_file)
    replay_time = float(filename[len(f"kk{number}_"):-4])  # remove prefix and ".txt"

    # Load inputs
    input_file = os.path.join(INPUTS_DIR, f"kk{number}_{replay_time:.2f}.txt")
    print(input_file)
    if not os.path.isfile(input_file):
        print(f"Can't find inputs for map {map_name} : {input_file} doesn't exist")
        exit(0)

    shutil.copy(input_file, SCRIPTS_FOLDER + "inputs.txt")
    time.sleep(0.1)
    pyautogui.press("r")  # bind r "load inputs.txt"
    
    duration = replay_time + 10  # map load + 2.6 sec start start + 3 sec end + some wiggleroom
    end_time = time.monotonic() + duration

    while time.monotonic() < end_time:
        pyautogui.press("escape")  # Press random key to skip mediatracker / map intro
        time.sleep(0.1)

    press("quit")
    time.sleep(0.2)
    pyautogui.click()