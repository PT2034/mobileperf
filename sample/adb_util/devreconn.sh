#!/bin/bash
echo -----------------------------------------------------------------
while true; do
    if [ $(adb devices -l | wc -l) -eq 3 ];then
##列出所有设备，由于第一行是提示，最后一行是空白，所以通过awk只显示除第一行和最后一行的输出。
##  awk 'NR>2{print p}{p=$0}'  ##这句逻辑通过百度是意思NR>2及当当前行大于2时，即第三行开始满足条件，打印前一行的信息，这逻辑就是为了过滤第一行和最后一行。
        echo "device has connected"
        adb devices -l | awk 'NR>2{print p}{p=$0}' | while read id num
        do
            echo "sn:"$id "; " $num
        done
        break
##无用逻辑，只是打印出当前连接的设备信息，可省略
    elif [ $(adb devices -l | wc -l) -eq 2 ];then
        echo "wait for devices"
    else
        echo "more then one devices"
    fi
    sleep 1
done
echo -----------------------------------------------------------------
echo "`date +%H:%M:%S`"
# adb forward tcp:8000 tcp:9000
# echo "`date +%H:%M:%S`"