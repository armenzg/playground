#!/bin/sh
set -ex
DIR=`pwd`
CONFIG_FILES=`cd config_files && find . -type f | sed 's|./||'`
# Create the config giles
cd ~
# XXX: we have to verify that there is a file to remove; otherwise it will fail
for file in $CONFIG_FILES; do rm ~/$file && ln -s $DIR/config_files/$file .; done
# Create the scripts
mkdir -p ~/moz/scripts
cp $DIR/scripts/* ~/moz/scripts
