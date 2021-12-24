#!/bin/bash
echo ==========log抓取==========
date_time=$(date "+%Y%m%d_%H%M%S")
echo current time:$date_time
log_dir=logs_$date_time
echo logdir:$log_dir
mkdir $log_dir

#echo 获取root权限，下面pull一些隐私目录的数据需要root权限
#adb remount
#adb root
adb remount
echo 获取系统的所有app服务
adb shell ps -A > $log_dir/ps.txt
echo 获取系统的cup等占用情况
adb shell top -b -n 1 > $log_dir/top.txt

#获取系统的当前界面截图
adb shell screencap /mnt/sdcard/Pictures/capture.png
adb pull /mnt/sdcard/Pictures/capture.png $log_dir/capture.png
#echo 获取系统的cup前十个占用最多的进程信息
#adb shell top -b -n 1 -H -m 10 -s 6 -o pid,tid,user,pr,ni,%%cpu,s,virt,res,pcy,cmd,name > $log_dir/top10.txt

# echo 获取系统的进程内核信息
if [[ ! -d  ./sys ]]; then
	mkdir ./sys
fi
echo 获取系统的进程内存占用信息
adb shell cat /proc/meminfo > $log_dir/sys/meminfo.txt
echo 获取系统的cup信息
adb shell cat /proc/cpuinfo > $log_dir/sys/cpuinfo.txt
echo 获取系统的prop属性信息
adb shell getprop > $log_dir/sys/getprop.txt
echo 获取系统的disk大小信息
adb shell df -h > $log_dir/sys/df.txt

#获取系统的dumpsys信息，包含dumpsys package XXX的信息
mkdir $log_dir/dumpsys
adb shell dumpsys > $log_dir/dumpsys/dumpsys.txt
#adb shell dumpsys meminfo <package_name> or <package_id>

#获取系统的缓存日志
adb shell  logcat -v threadtime -d > $log_dir/logcat_threadtime.log
adb shell  logcat -v time -d > $log_dir/logcat.log
#系统ANR异常日志
adb pull   /data/anr                    $log_dir/anr
#系统settings下的system、secure、global等属性
adb pull /data/system/users/0           $log_dir/settings

echo.
echo ==========log抓取完成==========
pause