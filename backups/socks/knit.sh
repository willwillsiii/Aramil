#!/bin/bash
if [[ -z $1 ]]; then
	SOCKNAME=${USER}Sock
else
	SOCKNAME=${1}
fi
tmux -S /opt/aradev/socks/$SOCKNAME new -Adc /opt/aradev &&\
	echo "Socket created: /opt/aradev/socks/$SOCKNAME"
setfacl -x g:wizardev /opt/aradev/socks/$SOCKNAME &&\
	echo "Permissions of socket file adjusted for security."
