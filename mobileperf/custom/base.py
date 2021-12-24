import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
mobilePerfPath = os.path.abspath(os.path.dirname(curPath) + os.path.sep + ".")
rootPath = os.path.abspath(os.path.join(mobilePerfPath, '../..'))

# sys.path.append(rootPath)

if __name__ == '__main__':
    print('curPath = ' +curPath)
    print('rootPath = ' +rootPath)