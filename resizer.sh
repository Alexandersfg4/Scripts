#!/bin/sh
#wav 38MB file creater
#create test file for cpoying data
cat $1 > test.vaw
size=$(ls -l $1 | awk '{print $5}')
echo "actual file size is: $size"
while [ $size -lt 38000000 ]
do
	cat test.vaw >> $1
	size=$(ls -l $1 | awk '{print $5}')
	if [ $size -ge 38000000 ]
	then
		break
	fi
done
echo "new file size is: $size"
#removing the test file
rm -rf test.vaw	 
