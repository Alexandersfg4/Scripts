#/bin/sh

useradd $1
echo "The next user has been created"
chmod 557 /home/$1
passwd $1
