# PyFileCopy
Copies files and checks if they are copied completely

Tested with python 3.9

Parameters required are -s "/path/to/source/folder" -d "/path/to/destination/folder" 
Optional parameters are [-f "file extension filter"] only copies files with file extention. Example would be -f ".mp4"
and [-m "move"] deletes files after hash of source and destination file is the same
