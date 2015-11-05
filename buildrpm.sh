#!/usr/bin/env bash

RPMBUILD=${HOME}/rpmbuild
VERSION='1.0'

RPMBUILD=`which rpmbuild`
if [ "$?" == "1" ]; then
    echo rpm-build is not installed.  Attempting to install, if this does not work then run "yum -y install rpm-build python-setuptools" as root
    yum -y install rpm-build python-setuptools
    echo
    echo
fi

echo RPM build dir is ${RPMBUILD}
mkdir -p ${RPMBUILD}/SOURCES
tar cv . --exclude "./.git" --exclude "./.idea" --exclude ".DS_Store" --transform "s,^\.,Watchman-${VERSION},"  | gzip > ${RPMBUILD}/SOURCES/Watchman-${VERSION}.tar.gz

mkdir -p /etc/supervisor/conf.d

rpmbuild -bb Watchman.spec

mv ${RPMBUILD}/RPMS/noarch/*.rpm .