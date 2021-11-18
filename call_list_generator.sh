#!/bin/sh
#the list generates list by the next varibles
DEF_COUNRY_CODE=1
AMOUNT_OF_RECORDS=1000
#do not change the next part
var=0
cat <<'EOF' > calling_list$AMOUNT_OF_RECORDS.txt
Account, Name, Phone number
EOF
until [ $var -eq $AMOUNT_OF_RECORDS ]
do	
	printf "$var, name, $DEF_COUNRY_CODE$var \n" >> calling_list$AMOUNT_OF_RECORDS.txt
	var=`expr $var + 1`
done 

