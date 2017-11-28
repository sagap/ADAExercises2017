#!/usr/bin/env bash

USERNAME=`cat ./username`

rsync -urltv --delete -e ssh tweeter_events/ "$USERNAME@iccluster060.iccluster.epfl.ch:/home/$USERNAME/tweeter_events-$USERNAME"
