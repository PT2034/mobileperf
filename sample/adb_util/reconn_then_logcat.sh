#!/bin/bash

echo -----------------------------------------------------------------
echo "reoconnect device start here"


long_date=$(date "+%Y%m%d_%H%M%S")

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

#echo "`date +%H:%M:%S`"
# adb forward tcp:8000 tcp:9000
# echo "`date +%H:%M:%S`"
#echo ==========logcat start here==========
date_time=$(date "+%Y%m%d_%H%M%S")
# echo 当前时间是：$date_time
# echo 设置显示的文件夹名称
# log_dir=Logs_$date_time
# echo 日志文件夹：$log_dir
# mkdir $log_dir

#获取系统的缓存日志
# adb shell  logcat -v threadtime -d > $log_dir/logcat_threadtime.txt

echo ==========log catching...==========
echo "`date +%H:%M:%S` ""Logcat log will be saved to logcat_$date_time.log"
echo "If you think it is enough, please exit directly"
echo

#adb shell  logcat -v time  > logs/logcat_$date_time.log
# adb shell  logcat -v process
# adb shell  logcat -v threadtime


adb logcat -v time 2>&1 |
tee logs/logcat_${long_date}.log
#sh tee_adb.sh 2>&1 |tee logs/logcat_$date_time.log
#sh tee_adb.sh 2>&1 |tee logs/logcat_$date_time.log
#pause
#获取系统的当前界面截图
# adb shell screencap /mnt/sdcard/Pictures/capture.png
# adb pull /mnt/sdcard/Pictures/capture.png $log_dir/capture.png

echo ==========log done==========