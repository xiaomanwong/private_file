from builtins import str
import os
import sys
name = sys.argv[1]
cmd = "adb shell screencap -p /sdcard/" + name + ".png"
print(cmd)
os.popen(cmd)
path  = os.getcwd()
print(path)
cmd2 = "adb pull /sdcard/" + name + ".png /Users/admin/Downloads/"
os.popen(cmd2)
print("report: /Users/admin/Downloads/" + name + ".png success")