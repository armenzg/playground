#!/bin/sh
BUILD_TAG=FIREFOX_9_0b4_BUILD1
RELEASE_TAG=FIREFOX_9_0b4_RELEASE
FENNEC_BUILD_TAG=FENNEC_9_0b4_BUILD1
FENNEC_RELEASE_TAG=FENNEC_9_0b4_RELEASE

cd ~/repos/buildbot-configs
hg pull -u; hg up -C; hg up -r production
revision=`hg id --id` 
hg tag -r $revision $BUILD_TAG $RELEASE_TAG $FENNEC_BUILD_TAG $FENNEC_RELEASE_TAG 

cd ~/repos/buildbotcustom
hg pull -u; hg up -C; hg up -r production-0.8
revision=`hg id --id` 
hg tag -r $revision $BUILD_TAG $RELEASE_TAG $FENNEC_BUILD_TAG $FENNEC_RELEASE_TAG 

cd ~/repos/tools
hg pull -u; hg up -C
revision=`hg id --id` 
hg tag -r $revision $BUILD_TAG $RELEASE_TAG $FENNEC_BUILD_TAG $FENNEC_RELEASE_TAG 

cd ~/repos/mozharness_hg
hg pull -u; hg up -C
revision=`hg id --id` 
hg tag -r $revision $BUILD_TAG $RELEASE_TAG $FENNEC_BUILD_TAG $FENNEC_RELEASE_TAG 
