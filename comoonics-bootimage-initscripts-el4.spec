#****h* comoonics-bootimage/comoonics-bootimage.spec
#  NAME
#    comoonics-bootimage-initscripts.spec
#    $id$
#  DESCRIPTION
#    initscripts for the Comoonics bootimage
#  AUTHOR
#    Mark Hlawatschek
#
#*******
# @(#)$File:$
#
# Copyright (c) 2007 ATIX GmbH.
# Einsteinstrasse 10, 85716 Unterschleissheim, Germany
# All rights reserved.
#
# This software is the confidential and proprietary information of ATIX
# GmbH. ("Confidential Information").  You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with ATIX.
# $Id: comoonics-bootimage-initscripts-el4.spec,v 1.3 2007-09-14 15:07:18 mark Exp $
#
##
##

%define _user root
%define CONFIGDIR /%{_sysconfdir}/comoonics
%define APPDIR    /opt/atix/%{name}
%define ENVDIR    /etc/profile.d
%define ENVFILE   %{ENVDIR}/%{name}.sh
%define INITDIR   /etc/rc.d/init.d
%define SYSCONFIGDIR /%{_sysconfdir}/sysconfig

Name: comoonics-bootimage-initscripts
Summary: Comoonics Bootimage initscripts. Initscripts used by the comoonics shared root cluster environment.
Version: 1.3
BuildArch: noarch
Requires: comoonics-bootimage >= 1.3-1
#Conflicts:
Release: 1.el4
Vendor: ATIX AG
Packager: Mark Hlawatschek (hlawatschek (at) atix.de)
ExclusiveArch: noarch
URL:     http://www.atix.de/
Source:  http://www.atix.de/software/downloads/comoonics/comoonics-bootimage-%{version}.tar.gz
License: GPL
Group:   Storage/Management
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

%description
Comoonics Bootimage initscripts. Initscripts used by the comoonics shared root cluster environment.


%prep
%setup -n comoonics-bootimage-%{version}

%build

%install
install -d -m 755 $RPM_BUILD_ROOT/%{INITDIR}
install -m755 initscripts/rhel4/bootsr $RPM_BUILD_ROOT/%{INITDIR}/bootsr
install -m755 initscripts/rhel4/ccsd-chroot $RPM_BUILD_ROOT/%{INITDIR}/ccsd-chroot
install -m755 initscripts/rhel4/fenced-chroot $RPM_BUILD_ROOT/%{INITDIR}/fenced-chroot

%clean
rm -rf %{buildroot}

%postun

if [ "$1" -eq 0 ]; then
  echo "Postuninstalling comoonics-bootimage-initscripts"
  root_fstype=$(mount | grep "/ " | awk '
BEGIN { exit_c=1; }
{ if ($5) {  print $5; exit_c=0; } }
END{ exit exit_c}')
  if [ "$root_fstype" != "gfs" ]; then
	/sbin/chkconfig --del bootsr
	/sbin/chkconfig --del ccsd-chroot
	/sbin/chkconfig --del fenced-chroot
    /sbin/chkconfig --add fenced &>/dev/null
    /sbin/chkconfig --list fenced
    /sbin/chkconfig --add ccsd &>/dev/null
    /sbin/chkconfig --list ccsd
  fi
fi

%post

echo "Starting postinstall.."
services="bootsr ccsd-chroot fenced-chroot"
echo "Resetting services ($services)"
for service in $services; do
   /sbin/chkconfig --del $service &>/dev/null
   /sbin/chkconfig --add $service
   /sbin/chkconfig $service on
   /sbin/chkconfig --list $service
done

services="ccsd fenced"
echo "Disabling services ($services)"
for service in $services; do
   /sbin/chkconfig --del $service &> /dev/null
done
/bin/true


%files

%attr(750, root, root) %{INITDIR}/bootsr
%attr(750, root, root) %{INITDIR}/fenced-chroot
%attr(750, root, root) %{INITDIR}/ccsd-chroot
%changelog
* Wed Sep 12 2007 Mark Hlawatschek <hlawatschek@atix.de> 1.3.1
- first revision
# ------
# $Log: comoonics-bootimage-initscripts-el4.spec,v $
# Revision 1.3  2007-09-14 15:07:18  mark
# removed sensless comment
#
# Revision 1.2  2007/09/14 13:36:05  marc
# fixed cleaning up
#
# Revision 1.1  2007/09/13 08:35:22  mark
# initital check in
#
