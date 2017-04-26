%define name Watchman
%define version 1.4
%define unmangled_version 1.4
%define release 1

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
Requires: python-devel, python2-pip

%description
UNKNOWN

%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --install-scripts=usr/bin --install-purelib=usr/lib64/python2.7/site-packages --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)

%post
mkdir -p /var/log/supervisor
mkdir -p /var/log/watchman
useradd celery
