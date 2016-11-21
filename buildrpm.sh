#!/usr/bin/env bash

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

rpmbuild -bb Watchman.spec

mv ${BUILD_DIR}/RPMS/noarch/*.rpm .
