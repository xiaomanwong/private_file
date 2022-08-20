from builtins import str
import os
import sys
name = sys.argv[1]
platform = sys.argv[2]

if platform == "a":
	cmd = "adb shell screencap -p /sdcard/" + name + ".png"
	print(cmd)
	cmd2 = "adb pull /sdcard/" + name + ".png /Users/admin/Downloads/"
elif platform == "h":
	cmd = "hdc shell screencap -p /sdcard/" + name + ".png"
	print(cmd)
	cmd2 = "hdc file recv /sdcard/" + name + ".png /Users/admin/Downloads/"
os.popen(cmd)
os.popen(cmd2)
print("report: /Users/admin/Downloads/" + name + ".png success")