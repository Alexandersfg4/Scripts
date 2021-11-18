#!/bin/sh
#example ./log_zipper.sh {archive name} 
LOG_FOLDER=/var/log/servicepattern/
find $LOG_FOLDER -name "*[[:alpha:]].log" -print | zip $1 -@
echo "The next archive has been created: $1"

