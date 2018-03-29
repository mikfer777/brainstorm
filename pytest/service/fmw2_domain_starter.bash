#!/bin/bash
#
set +xv



# ------------------------------------------------------------------------------
# Start fmw managed node without waiting (background)
# ------------------------------------------------------------------------------
# thecommand &>/dev/null &
start_node_background()
{
    #status=$(/appli/projects/AMM/Oracle12C/ASGS-M2MFMW-DOMAIN/statusM2MFMW-$1-ASGS.sh)
    #status=$(echo ${status} | sed 's/ //g')
    status="UNKNOWN"
    # double check on jvm running...
    dstatus=$(ps -eaf |  grep /bin/java | grep $1-$2  | grep -v grep | wc -l)
    if [[ ${status} == *"RUNNING"* || ${dstatus} == *"1"* ]] ; then
        echo "RUNNING"
        return 0
    elif [[ ${status} == *"SHUTDOWN"* || ${status} == *"UNKNOWN"* || ${status} == *"Thereisnoserverrunning"* ]] ; then
        nohup /appli/projects/AMM/Oracle12C/ASGS-$1-DOMAIN/start$1-$2-ASGS.sh &>/dev/null &
        if [ $? -eq 0 ] ; then
            echo "RUNNING"
            return 0
        else
            echo "ERROR"
            return 1
        fi
    fi
}


status_managed1=$(start_node_background $1 "lan-b-1")
echo $1 " status_managed1=" ${status_managed1}
status_managed2=$(start_node_background $1 "lan-b-2")
echo $1 " status_managed2=" ${status_managed2}


# non blocking loop
while :; do sleep 2073600; done