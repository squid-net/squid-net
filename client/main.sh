#!/bin/bash

IP=$1
REVERSE_SHELL_CODE = "reverse_shell"

while true; do
    echo $IP
    RESPONSE=$(curl -s http://$IP)
    if [[ $RESPONSE == "" ]]; then
        echo "server down."
    else
        if [[ $RESPONSE == $REVERSE_SHELL_CODE ]]; then
            echo "REVERSE_SHELL"
        else
            echo $RESPONSE
            echo "something else"
        fi
    fi
    sleep 10 
done

