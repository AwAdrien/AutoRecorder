# AutoRecorder
TM Interface and OBS plugin to auto records runs

## TMInterface

Simply load the `AutoRecorder.as` file as a TMI script.

## OBS

First modify the hardcoded `VIDEO_DIRECTORY` of the `autorecorder.py` script to whatever directory OBS saves video to (that's for automatic renaming).
Then, in OBS, navigate to `Tools > Scripts > Add Scripts` and select `autorecorder.py`. Check script logs for any issues !

On windows you might need to download additional packages, please see [here](https://docs.obsproject.com/scripting). 

DM @iuadrien on discord for feedbacks / bugs
