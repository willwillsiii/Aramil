#!/bin/bash
if [[ -z $1 ]]; then
	SOCKNAME=/opt/aradev/socks/${USER}Sock
else
	SOCKNAME=${1}
fi
tmux -S $SOCKNAME new -Adc /opt/aradev &&\
	echo "Socket created: $SOCKNAME"
setfacl -m g::-,o::- $SOCKNAME && setfacl -x g:wizardev $SOCKNAME &&\
	echo "Permissions of socket file adjusted for security."
