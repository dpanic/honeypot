#!/bin/bash
SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
echo $SCRIPTPATH
cd $SCRIPTPATH

python3 -B ../processor.py
 