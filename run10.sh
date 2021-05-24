#!/bin/bash

python ./main.py -s=true -c=true &
for number in {1..9}
do
  python ./main.py -c=true -n="$number" &
done
