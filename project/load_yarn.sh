#!/usr/bin/env bash

getAbsPath() {
    if [[ -d "$1" ]]; then
        cd "$1"
        ABS_PATH="$(pwd -P)"
        cd ..
    else 
        cd "$(dirname "$1")"
        ABS_PATH="$(pwd -P)/$(basename "$1")"
        cd ..
    fi
}

# set variables for YARN
getAbsPath "ADA_YARN"
export YARN_CONF_DIR=$ABS_PATH
export HADOOP_USER_NAME=dona

# add spark to PATH
#export PATH="/usr/local/opt/apache-spark@1.6/bin:$PATH"
