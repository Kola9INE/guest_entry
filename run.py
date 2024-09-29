"""
This is an optional python file to run the streamlit app automatically.
However to enjoy same on your system, you should change the bash.exe path
in this script to the bash.exe path on your system.
"""

import subprocess
from pathlib import Path

if __name__ == '__main__':
    wdd = Path.cwd()
    new_dir = Path(wdd/'entry.sh')
    pathsh = new_dir
    exec = r'C:\git\Git\bin\bash.exe'
    subprocess.run([exec, pathsh])