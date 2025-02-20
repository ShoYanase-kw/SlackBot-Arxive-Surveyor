#!/bin/bash

set -e +vx

RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
BLUE="\e[34m"
END="\e[0m"

function DATE() {
    date +%Y.%m.%d\ %H:%M:%S
}



INFO="[INFO] :::"
WARNING="[WARNING] :::"
ERROR="[ERROR] :::"

REPOSITORY_ROOT=`pwd`

set -ex
