#!/bin/bash
# Script:  generate-locale.sh
# Author:  Armen Zambrano Gasparnian
# Contact: armenzg@mozilla.com
# Purpose: Repackage a locale in hg
# Date:    Jan 13th, 2010

# NOTE:
#    If you run this script and you reach the step "make installers-$LOCALE"
#    you can skip running this script and just run these subset of steps:
#      cd $BASE_DIR/$BRANCH/browser/locales
#      PYTHONPATH=../../../compare-locales/lib python ../../../compare-locales/scripts/compare-locales -m merged l10n.ini ../../../l10n $LOCALE | tee ../../../compare-locales.log
#      make installers-$LOCALE LOCALE_MERGEDIR=$PWD/merged; cd -
#    You want to add new files and do modifications of your locale in:
#      $BASE_DIR/l10n/$LOCALE  

# Change it to your locale
export LOCALE='hy-AM'

set -ex
echo "Creating a nightly";
export BASE_DIR=`pwd`
export L10N_HG_SERVER='http://hg.mozilla.org/l10n-central'
export BRANCH='mozilla-central'
export EN_US_REPO='http://hg.mozilla.org/$BRANCH'
export EN_US_BINARY_URL="http://ftp.mozilla.org/pub/mozilla.org/firefox/nightly/latest-mozilla-central"
export REVISION='default'
# We don't really disable webm but we just bypass a check in the confgure step that we don't need
export CONFIGURE_ARGS='--enable-application=browser --with-l10n-base='$BASE_DIR'/l10n --disable-webm'


### 1) Clobber previous run
rm -rf $BRANCH/dist/install
rm -rf $BRANCH/dist/*$LOCALE*

### 2) Checkout the browser repo
# if checkout does not exists
[ -d $BRANCH ] || hg clone $EN_US_HG_SERVER/$REPO_PATH ; 
hg -R $BRANCH pull -r default 

### 3) Checkout the locale repo
mkdir -p $BASE_DIR/l10n
cd $BASE_DIR/l10n
# if we don't have the locale clone it
[ -d $LOCALE ] || hg clone $L10N_HG_SERVER/$LOCALE ; 
hg -R $LOCALE pull -r default

### 4) Let's generate a "merged" directory with compare-locales
cd $BASE_DIR 
rm -rf compare-locales
hg clone http://hg.mozilla.org/build/compare-locales compare-locales
cd compare-locales; hg up -C -r RELEASE_AUTOMATION; cd ..
cd $BASE_DIR/$BRANCH/browser/locales
# a directory called "merged" will be generated under browser/locales
PYTHONPATH=../../../compare-locales/lib python ../../../compare-locales/scripts/compare-locales -m merged l10n.ini ../../../l10n $LOCALE | tee ../../../compare-locales.log

### 5) Setup
cd $BASE_DIR/$BRANCH
autoconf-2.13
cd js/src && autoconf-2.13 && cd ../..
./configure $CONFIGURE_ARGS 
make -C config
if [ "`uname -s`" == "Darwin" ]; then
    export MOZ_PKG_PLATFORM=mac 
fi
# get the latest en-US and unpack it
make -C browser/locales wget-en-US
make -C browser/locales unpack;

make -C nsprpub
make -C modules/libmar
# 6) generate the xpi and the installers
cd browser/locales; make installers-$LOCALE LOCALE_MERGEDIR=$PWD/merged; cd -
# 7) list the packages in the correct place, the correct naming and the correct chmod
cd $BASE_DIR
mv $BRANCH/dist/*hy-AM* $BRANCH/dist/install/*xpi .
