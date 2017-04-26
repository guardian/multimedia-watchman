#!/usr/bin/env bash

function increment_release {
    FILENAME=$1

    RELEASEVER=$(grep '%define release' ${FILENAME} | awk -F ' ' '{print $3}')
    if [ ${CIRCLE_BUILD_NUM} != "" ]; then
        NEWVER=${CIRCLE_BUILD_NUM}
    else
        NEWVER=$(($RELEASEVER+1))
    fi
    echo Release version was ${RELEASEVER}, now is ${NEWVER}
    cat ${FILENAME} | sed "s/\%define release .*/%define release ${NEWVER}/" > ${FILENAME}.new
    mv ${FILENAME} ${FILENAME}.old
    mv ${FILENAME}.new ${FILENAME}
}

BUILD_DIR=${HOME}/rpmbuild
VERSION=`grep WATCHMAN_VERSION setup.py | cut -d '"' -f2`   #extract version number from WATCHMAN_VERSION in setup.py

RPMBUILD=`which rpmbuild`
if [ "$?" == "1" ]; then
    echo rpm-build is not installed.  Attempting to install, if this does not work then run "yum -y install rpm-build python-setuptools" as root
    yum -y install rpm-build python-setuptools
    echo
    echo
fi

echo RPM build dir is ${BUILD_DIR}
mkdir -p ${BUILD_DIR}/SOURCES
tar cv . --exclude "./.git" --exclude "./.idea" --exclude ".DS_Store" --transform "s,^\.,Watchman-${VERSION},"  | gzip > ${BUILD_DIR}/SOURCES/Watchman-${VERSION}.tar.gz

mkdir -p /etc/supervisor/conf.d

increment_release Watchman.spec

rpmbuild -bb Watchman.spec

mv ${BUILD_DIR}/RPMS/noarch/*.rpm .
