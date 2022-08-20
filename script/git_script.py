from builtins import str
import os
import sys

if len(sys.argv) < 2:
	print("请使用 python3 git_script.py xxx.git")
	print("xxx.git: 为需要下载项目的仓库地址，仅支持 HTTPS 方式 clone。")
	sys.exit(0)
# git path for clone 
print("prepare to start clone")
gitPath = sys.argv[1]
destPath = ""
if len(sys.argv) == 3: 
	destPath = sys.argv[2]
print("start to clone main Repo")
# Split git path to get Repo name
preStaff = gitPath.rfind("/") + 1
subStaff = gitPath.find(".git")
childName = gitPath[preStaff:subStaff]
# Generate git command
if len(destPath) == 0:
	destPath = os.getcwd() 
cmd = "git clone " + gitPath + " " + destPath + "/" +childName
print("cmd: ", cmd)
# Execute the git command
result = os.popen(cmd)
print ("result" , result.read()) 
print("main Repo completed, then start clone submodule")
print("prepare start clone submodule")
# The current path, used to store the contents of the remote repo
# work_dir = os.getcwd() 
repo_path = os.path.join(destPath, childName)
print("repo_path: ", repo_path)
# enter the Repo
os.chdir(repo_path)
print("start to clone submodule")
# Generate git submodule command
cmd = "git submodule update --init --recursive --remote"
print(cmd)
# Execute the submodule command
result = os.popen(cmd)
print ("result" , result.read()) 
print("submodule clone completed")
print("Repo clone finished")