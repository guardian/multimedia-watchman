%define name Watchman
%define version 1.4
%define unmangled_version 1.4
%define release 1

#disable automatic requirements scanning, as this introduces a dependency on the python path of circleci's virtualenv
AutoReqProv: no
AutoReq: no
Summary: A system which watches folders and executes commands when files are created in the folders
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GNM Internal Software
Group: Applications/Utilities
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Andy Gallagher and David Allison <multimediatech@theguardian.com>
Requires: python, python-devel, python2-pip, systemd

%description
UNKNOWN

%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
#have to specify the python we want it to run against when installed here, not the virtualenv one.
#-f (force) is needed because by this point circleci has already run this once.
python setup.py build -e "/usr/bin/python" -f

%install
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --install-scripts=usr/bin --install-purelib=usr/lib64/python2.7/site-packages --record=INSTALLED_FILES
mkdir -p $RPM_BUILD_ROOT/etc/systemd/system
cp watcher_config/watchman-watcher.service $RPM_BUILD_ROOT/etc/systemd/system
cp watcher_config/watchman-worker.service $RPM_BUILD_ROOT/etc/systemd/system
cp watcher_config/watchman.target $RPM_BUILD_ROOT/etc/systemd/system
cp watcher_config/example_config.xml $RPM_BUILD_ROOT/etc/ffqueue-config.xml
mkdir -p $RPM_BUILD_ROOT/usr/share/watchman
cp requirements.txt $RPM_BUILD_ROOT/usr/share/watchman

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
/etc/systemd/system/watchman-watcher.service
/etc/systemd/system/watchman-worker.service
/usr/share/watchman/requirements.txt
/etc/systemd/system/watchman.target
/etc/ffqueue-config.xml

%defattr(-,root,root)

%post
mkdir -p /var/log/watchman
pip install -r /usr/share/watchman/requirements.txt
systemctl daemon-reload
systemctl enable watchman.target
