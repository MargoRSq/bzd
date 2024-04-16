import os
import sys

if getattr(sys, 'frozen', False):
    static_dir = os.path.join(sys._MEIPASS, 'src/static')
    data_dir = os.path.join(sys._MEIPASS, 'src/data')
else:
    static_dir = 'src/static'
    data_dir = 'src/data'
