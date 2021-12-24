#!/bin/bash

#usage
#activity_name=$1
#interval_seconds=$2
#start_time=$3  #optional
#end_time=$4  #optional
#perfmon_via_top.sh  com.android.mms 3


#Tasks: 573 total,   1 running, 529 sleeping,   0 stopped,   0 zombie
#Mem:   3798236k total,  3700064k used,    98172k free,    10756k buffers
#Swap:  2293756k total,     2732k used,  2291024k free,  1949924k cached
#800%cpu   1%user   0%nice   3%sys 794%idle   0%iow   1%irq   0%sirq   0%host
#  PID USER         PR  NI VIRT  RES  SHR S[%CPU] %MEM     TIME+ ARGS
# 5926 shell        20   0  12M 2.9M 1.6M R  3.3   0.0   0:00.25 top -m 10
# 2005 system       20   0 4.0G  73M  47M S  0.3   1.9   0:03.68 com.huawei.powe+
# 1091 system       20   0  13M 1.8M 1.2M S  0.3   0.0   0:00.14 chargelogcat-c

echo -----------------------------------------------------------------
echo "start here, `date +%H:%M:%S`"
long_date_time=$(date "+%Y%m%d_%H%M%S")
# console
while true;  do echo `date`","`top -b -n 1 |grep 'com.android.mms'|grep -v 'grep'`; sleep 3; done
#while true;  do echo `date`","`top -b -n 1 |grep 'com.android.mms'|grep -v grep|cut -c 31-34`","`top -b -n 1 |grep 'com.android.mms'|grep -v grep|cut -c 43-48` ; sleep 3; done

# writeToFile 持续输出某个package信息
#Sun Oct 10 08:45:56 CST 2021, 84, 0.0
#while true;  do echo `date`","`top -b -n 1 |grep 'com.android.mms'|grep -v grep|cut -c 31-34`"",""`top -b -n 1 |grep 'com.android.mms'|grep -v grep|cut -c 43-48`>>/sdcard/cpu_${long_date_time}.log ; sleep 3; done
#Sun Oct 10 08:44:13 CST 2021, 84M , 0.0
#while true;  do echo `date`","`top -b -n 1 |grep 'com.android.mms'|grep -v grep|cut -c 31-35`"",""`top -b -n 1 |grep 'com.android.mms'|grep -v grep|cut -c 43-48` ; sleep 3; done

echo -----------------------------------------------------------------
echo "`done, date +%H:%M:%S`"