#!/bin/sh
#example ./log_zipper.sh {archive name} 
log_folder=/var/log/servicepattern/
find $log_folder -name "*[[:alpha:]].log" -print | zip $1 -@
echo "The next archive has been created: $1"

