#!/bin/bash
if [[ $1 == *"START"* ]] ; then
    nohup /usr/sbin/asgs/fmw2_domain_starter.bash $2 &>/dev/null &
else
    /usr/sbin/asgs/fmw2_domain_stopper.bash $2
fi