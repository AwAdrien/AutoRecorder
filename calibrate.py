from pynput import mouse
import json

points = {}
labels = ["refresh", "select_replay", "launch", "play", "quit"]
current_index = 0

def on_click(x, y, button, pressed):
    global current_index
    if pressed:
        label = labels[current_index]
        points[label] = {"x": x, "y": y}
        print(f"Recorded {label}: ({x}, {y})")
        current_index += 1

        if current_index >= len(labels):
            print("Calibration complete.")
            with open("points.json", "w") as f:
                json.dump(points, f, indent=4)
            print("Saved to points.json")
            return False  # stop listener

print("Calibration started.")
print("Click REFRESH point, then SELECT_REPLAY, then LAUNCH, then PLAY, then QUIT (bottom right).")

with mouse.Listener(on_click=on_click) as listener:
    listener.join()
