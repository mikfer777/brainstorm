#!/bin/bash
#
set +xv


# ------------------------------------------------------------------------------
# Stop cluster node
# ------------------------------------------------------------------------------
stop_node_background()
{
    #status=$(/appli/projects/AMM/Oracle12C/ASGS-M2MFMW-DOMAIN/statusM2MFMW-$1-ASGS.sh)
    #status=$(echo ${status} | sed 's/ //g')
    status="UNKNOWN"
    # double check on jvm running yet...
    dstatus=$(ps -eaf |  grep /bin/java | grep $1-$2 | grep -v grep | wc -l)
    if [[ ${status} == *"RUNNING"* || ${dstatus} == *"1"* ]] ; then
        pidnode=$(ps -eaf |  grep /bin/java | grep $1-$2 | grep -v grep | awk '{print $2}')
        echo ${pidnode}
        #nohup /appli/projects/AMM/Oracle12C/ASGS-M2MFMW-DOMAIN/stopM2MFMW-$1-ASGS.sh &>/dev/null &
        kill ${pidnode}
        if [ $? -eq 0 ] ; then
            echo "SHUTDOWNING"
            return 0
        else
            echo "ERROR"
            return 1
        fi
    elif [[ ${status} == *"SHUTDOWN"* || ${status} == *"UNKNOWN"* || ${status} == *"Connectionrefused"* ]] ; then
            echo "SHUTDOWNED"
            return 0
     fi
}



status_managed1=$(stop_node_background $1 "lan-a-1")
echo $1 " status_managed1="  ${status_managed1}
status_managed2=$(stop_node_background $1 "lan-a-2")
echo $1 " status_managed2="  ${status_managed2}
status_admin=$(stop_node_background $1 "admin")
echo $1 " status_admin="  ${status_admin}