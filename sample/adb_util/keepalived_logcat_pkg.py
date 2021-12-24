# !/usr/bin/env python3
# coding:utf-8
import os
import sys

print("Usage\n: python3 keepalived_logcat_pkg.py com.tal.genie.voice")
# (venv) larryzhu@LarrydeMacBook-Pro adb_util % adb shell ps |grep com.tal.genie
# system        1081   452  955260 118768 0                   0 S com.tal.genie.rtc
# system        1086   452  965252 152876 0                   0 S com.tal.genie.push
# u0_a39        1092   452 1135420 242032 0                   0 S com.tal.genie.voice
# u0_a19        1143   452  977472 170612 0                   0 S com.tal.genie.launcher
# system        1321   452  964792 114164 0                   0 S com.tal.genie.rtc:core
# u0_a22        1688   452  945884 134564 0                   0 S com.tal.genie.lockscreen
# system        2122   452  928992 103036 0                   0 S com.tal.genie.setting


def keep_logcat_per_pkg():
    packageName = str(sys.argv[1])
    command = "adb shell ps | grep %s | awk '{print $2}'" % (packageName)
    p = os.popen(command)
    ##for some applications,there are multiple processes,so we should get all the process id
    pid = p.readline().strip()
    filters = pid
    while (pid != ""):
        pid = p.readline().strip()
        if (pid != ''):
            filters = filters + "|" + pid
        print('command = %s;filters=%s' % (command, filters))
    if (filters != ''):
        cmd = 'adb logcat | grep --color=always -E "%s" ' % (filters)
        print('cmd = %s' % cmd)
    os.system(cmd)

if __name__ == '__main__':
    keep_logcat_per_pkg()