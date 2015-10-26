%define name Watchman
%define version 1.0
%define unmangled_version 1.0
%define unmangled_version 1.0
%define release 2

Summary: A system which watches folders and executes commands when files are created in the folders
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: UNKNOWN
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Andy Gallagher and David Allison <multimediatech@theguardian.com>
Requires: python-devel, python-setuptools

%description
UNKNOWN

%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)

%post
mkdir -p /var/log/supervisor
mkdir -p /var/log/watchman
useradd celery
easy_install supervisor celery certifi raven redis watchdog
