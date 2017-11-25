#!/usr/bin/env bash

USERNAME=`cat ./username`

scp -r tweeter_events $USERNAME@iccluster060.iccluster.epfl.ch:/home/$USERNAME/.
