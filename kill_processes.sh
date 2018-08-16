#########################################################################
# File Name: kill_processes.sh
# Author: sgs
# mail: sgs921107@163.com
# Created Time: Wed 25 Jul 2018 03:25:26 PM CST
#########################################################################
#!/bin/bash

# 脚本功能：强制杀死进程 方式kill -9
    # 1通过ps查询进程的id
    # 2使用kill -9 强制终止进程
# 启动方式：/bin/bash kill_process.sh 进程名


# 如果参数个数不等于1  提示错误并退出程序
if [ $# -ne 1 ]
then
    echo "参数个数有误 请使用此方式运行：/bin/bash kill_process.sh 进程名"
    exit 1
fi
				
# 获取要被杀死的进程名
pName=$1
				
				
<<!
    函数功能：根据进程名杀死程序
    参数：进程名
    返回值：无
!
kill_processes(){
	# 获取进程id
    pIds=$(ps -ef | grep "$1" | grep -v grep | grep -v $0 | awk '{print $2}')
    for pId in $pIds
    do
	kill -9 $pId
    done
}
																
						
echo 将要被终止的进程有：
echo ------------------------------------------------------------------
# 根据进程名查询包含进程名的进程 并排除grep查询进程和此脚本进程
ps -ef | grep "$pName" | grep -v grep | grep -v $0
echo ------------------------------------------------------------------
# 确认是否杀死程序
read -t 10 -p "10秒后将自动杀死这些进程，请确认是否杀死这些进程（y/n）：" ipt

case $ipt in
    "n")
        echo "==我还不想干掉它们"
        exit 0;;
    "y")
	echo "是的，立即干掉它们"
        kill_processes $pName;;
    "")
	echo ""
        # 没有输入确认信息  默认杀死程序
	echo "开始自动杀死这些程序"
        kill_processes $pName;;
    *)
        echo "您的输入有误，将终止脚本"
        exit 1;;
esac
