# Android 自动化打包

工具：Jenkins， python， gralde， git

Jenkins 部署，以此为媒介触发 shell 命令

Jenkisn 参数化构建，




python：

class BuildParams(object):
    def __init__(self, params):
        self.platfrom = params[1]
        self.branch = prams[2]
        xxx
        xxx
        xxx
        xxx


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='xxxxxxx')
    parser.add_agrument("--platform", "-p", help="build platform", type=str, required=True)
    parser.add_agrument("--parmas1", "-p", help="build platform", type=str, required=True)
    parser.add_agrument("--params2", "-p", help="build platform", type=str, required=True)
    parser.add_agrument("--params3", "-p", help="build platform", type=str, required=True)
    
    config = parser.parse_args()


class Builder:
    def __init__(self, params1: str, params2: str, params3: str):
        self.params1 = params1
        self.params2 = params2
        self.params3 = params3
    
    def __call__(self):
        self.initRepo()
        self.upgradeVersion()
        self.configBuildParams()
        self.upload()

python mode:
    gitpython
    jenkins-python
    

