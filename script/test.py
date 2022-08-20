from builtins import str
import os
import subprocess
import re
import time

startTime = time.time()
cmd = "/Users/admin/Library/Android/sdk/build-tools/30.0.2/aapt dump badging /Users/admin/Downloads/yd_b__a1_6.0.1.0_a2db018ccc.apk"
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
outputRes = output.decode()
permissions = re.findall(re.compile("uses-permission: name='(\S+)'"), outputRes)
for p in permissions:
	print(p)
package = re.compile("package: name='(\S+)'").search(outputRes)
print(package.group(1))
sdkVersion = re.compile("sdkVersion:'(\S+)'").search(outputRes)
print(sdkVersion.group(1))
targetVersion = re.compile("targetSdkVersion:'(\S+)'").search(outputRes)
print(targetVersion.group(1))
versionName = re.compile("versionName='(\S+)'").search(outputRes)
print(versionName.group(1))
print(os.getcwd())

endTime = time.time() - startTime
print("共耗时：" + str(endTime))
        
# print(match.group())