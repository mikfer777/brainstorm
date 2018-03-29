#!/bin/bash
#
set +xv

# ------------------------------------------------------------------------------
# Start cluster node
# ------------------------------------------------------------------------------
start_node()
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
          status2=$(/appli/projects/AMM/Oracle12C/ASGS-$1-DOMAIN/start$1-$2-ASGS.sh)
          if [[ ${status2} == *"RUNNING"* ]] ; then
            echo "RUNNING"
            return 0
          else
            echo "ERROR"
            return 1
          fi
    fi
}

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


status_admin=$(start_node $1 "admin")
echo "status_admin="  ${status_admin}
if [[ ${status_admin} == *"RUNNING"* ]] ; then
    status_managed1=$(start_node_background $1 "lan-a-1")
    echo $1 " status_managed1=" ${status_managed1}
    status_managed2=$(start_node_background $1 "lan-a-2")
    echo $1 " status_managed2=" ${status_managed2}
fi

# non blocking loop
while :; do sleep 2073600; done