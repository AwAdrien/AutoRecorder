# AutoRecorder
TM Interface and OBS plugin to auto records runs

## TMInterface

Simply load the `AutoRecorder.as` file as a TMI script.

## OBS

First modify the hardcoded `VIDEO_DIRECTORY` of the `autorecorder.py` script to whate ver directory OBS saves video to (that's for automatic renaming).
Then, in OBS, navigate to `Tools > Scripts > Add Scripts` and select `autorecorder.py`. Check script logs for any issues !

On windows you might need to download additional packages, please see [here](https://docs.obsproject.com/scripting). 

DM @iuadrien on discord for feedbacks / bugs

# Cycle Kacky Tracks

## Calibration

Use the `calibration.py` script **before anything else**. It will record you doing the clicks to play against a replay and exiting, to properly replay it later without issues.

You should start this script with TM open and at the correct position already, and in the play against replay tab. Then, click refresh, select the **first** replay, press launch then play and finaly click on the very bottom right for exiting (this button opens on the finish screen only).

Once this is done a `points.json` file should have been generated. You can redo the calibration at any moment.

## Cycling the tracks

First, edit the scrpt to modify the top 4 parameters:

- TM_FOLDER : full path to the folder that you navigated to in Trackmania. It should be **empty** (every other file there will be nuked)
- SCRIPTS_FOLDER : full path to your TMInterface script folder. That's where the `inputs.txt` file will be put. Don't forget to load it !
- REPLAYS_DIR : relative path to the folder where all replays containing timestamps are.
- INPUTS_DIR : relative path to the folder where all inputs files are. **DO NOT NEST**, they should all be here, no subdiretory (i'm lazy).

Once this is done, make sure that you loaded `inputs.txt` in TMI and run the script :) if new inputs don't load, you can do `bind r "load inputs.txt"`, and the file will be force-refreshed every new map.
