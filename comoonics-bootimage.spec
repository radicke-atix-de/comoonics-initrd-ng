#****h* comoonics-bootimage/comoonics-bootimage.spec
#  NAME
#    comoonics-bootimage.spec
#    $id$
#  DESCRIPTION
#    RPM Configurationfile for the Comoonics bootimage
#  AUTHOR
#    Marc Grimme
#
#*******
# @(#)$File:$
#
# Copyright (c) 2001 ATIX GmbH.
# Einsteinstrasse 10, 85716 Unterschleissheim, Germany
# All rights reserved.
#
# This software is the confidential and proprietary information of ATIX
# GmbH. ("Confidential Information").  You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with ATIX.
# $Id: comoonics-bootimage.spec,v 1.64 2007-10-18 08:22:37 marc Exp $
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

%define FENCEACKSV_SOURCE fencing/fence-ack-server
%define FENCEACKSV_DIR    /opt/atix/comoonics-fenceacksv

%define FENCECLIENTS_SOURCE fencing/
%define FENCECLIENTS_DIR /opt/atix/comoonics-fencing
%define FENCECLIENTS_DOC /usr/share/doc/comoonics-fencing

Name: comoonics-bootimage
Summary: Comoonics Bootimage. Scripts for creating an initrd in a gfs shared root environment
Version: 1.3
BuildArch: noarch
Requires: comoonics-cs-py >= 0.1-43 comoonics-cluster-py >= 0.1-2 comoonics-bootimage-initscripts >= 1.3 comoonics-bootimage-listfiles >= 1.3
#Conflicts:
Release: 21
Vendor: ATIX AG
Packager: Mark Hlawatschek (hlawatschek (at) atix.de)
ExclusiveArch: noarch
URL:     http://www.atix.de/
Source:  http://www.atix.de/software/downloads/comoonics/comoonics-bootimage-%{version}.tar.gz
License: GPL
Group:   Storage/Management
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

%description
Comoonics Bootimage. Scripts for creating an initrd in a gfs shared root environment

%package extras-network
Version: 0.1
Release: 1
Requires: comoonics-bootimage >= 1.3-1
Summary: listfiles for special network configurations (vlan)
Group:   Storage/Management
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

%description extras-network
Extra listfiles for special network configurations

%package extras-nfs
Version: 0.1
Release: 1
Requires: comoonics-bootimage >= 1.3-1
Summary: listfiles for nfs sharedroot configurations
Group:   Storage/Management
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

%description extras-nfs
Extra listfiles for nfs sharedroot configurations

%package extras-dm-multipath
Version: 0.1
Release: 1
Requires: comoonics-bootimage >= 1.3-1
Summary: listfiles for device mapper multipath sharedroot configurations
Group:   Storage/Management
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

%description extras-dm-multipath
Extra listfiles for device mapper multipath sharedroot configurations

%package extras-rdac-multipath
Version: 0.1
Release: 1
Requires: comoonics-bootimage >= 1.3-8
Summary: listfiles for rdac multipath sharedroot configurations
Group:   Storage/Management
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

%description extras-rdac-multipath
Extra listfiles for rdac multipath sharedroot configurations

%package extras-xen
Version: 0.1
Release: 1
Requires: comoonics-bootimage >= 1.3-14
Summary: listfiles for xen support in the open-sharedroot cluster
Group:   Storage/Management
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

%description extras-xen
listfiles for xen support in the open-sharedroot cluster

%package extras-iscsi
Version: 0.1
Release: 1
Requires: comoonics-bootimage >= 1.3-21
Summary: listfiles for iscsi support in the open-sharedroot cluster
Group:   Storage/Management
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

%description extras-iscsi
support in the open-sharedroot cluster
PREVIEW VERSION

%package compat
Version: 0.1
Release: 1
Requires: comoonics-bootimage >= 1.3-1
Summary: files needed for compatibility to 1.2 releases
Group:   Storage/Management
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

%description compat
Files needed for the compatibility to 1.2 releases
installes the file /etc/sysconfig/comoonics-chroot
This will mount vg_local-lv_tmp on /tmp during initrd
process

%package fenceacksv
Version: 0.3
Release: 1
Requires: comoonics-cs-py >= 0.1-43
Requires: comoonics-bootimage >= 1.3-1
Summary: The Fence ackserver is a service running in the fencedchroot and managing manual fenced nodes
Group:   Storage/Management
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

%description fenceacksv
The Fence ackserver is a service running in the fencedchroot and managing manual fenced nodes

%package fenceclient-ilo
Version: 0.1
Release: 18
Summary: An alternative fence client for ilo cards of HP servers. Written in python.
Group:   Storage/Management
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

%description fenceclient-ilo
An alternative fence client for ilo cards of HP servers. Written in python.

%package fenceclient-ilomp
Version: 0.1
Release: 1
Summary: A fence client for iloMP cards of HP inegrity servers. Written in python.
Group:   Storage/Management
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

%description fenceclient-ilomp
A fence client for iloMP cards of HP inegrity servers. Written in python.

%package fenceclient-vmware
Version: 0.1
Release: 4
Summary: Fencing for vmware
Group:   Storage/Management
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

%description fenceclient-vmware
Fencing for vmware client

%package fencemaster-vmware
Version: 0.1
Release: 1
Summary: Fencing for vmware
Group:   Storage/Management
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
AutoReqProv: no

%description fencemaster-vmware
Fencing for the vmware master server

%prep
%setup -q

%build

%install
make PREFIX=$RPM_BUILD_ROOT INSTALL_DIR=%{APPDIR} install

# Files for compat
install -d -m 755 $RPM_BUILD_ROOT/%{SYSCONFIGDIR}
install -m644 etc/sysconfig/comoonics-chroot.compat-vg_local $RPM_BUILD_ROOT/%{SYSCONFIGDIR}/comoonics-chroot


# Files for fenceacksv
install -d -m 755 $RPM_BUILD_ROOT/%{FENCEACKSV_DIR}
install -m755 %{FENCEACKSV_SOURCE}/fence_ack_server.py $RPM_BUILD_ROOT/%{FENCEACKSV_DIR}/
install -m644 %{FENCEACKSV_SOURCE}/shell.py $RPM_BUILD_ROOT/%{FENCEACKSV_DIR}/
#install -m644 %{FENCEACKSV_SOURCE}/pexpect.py $RPM_BUILD_ROOT/%{FENCEACKSV_DIR}/
install -m640 %{FENCEACKSV_SOURCE}/server.pkey $RPM_BUILD_ROOT/%{FENCEACKSV_DIR}/
install -m640 %{FENCEACKSV_SOURCE}/server.cert $RPM_BUILD_ROOT/%{FENCEACKSV_DIR}/
install -m640 %{FENCEACKSV_SOURCE}/CA.pkey $RPM_BUILD_ROOT/%{FENCEACKSV_DIR}/
install -m640 %{FENCEACKSV_SOURCE}/CA.cert $RPM_BUILD_ROOT/%{FENCEACKSV_DIR}/

install -d -m 755 $RPM_BUILD_ROOT/%{INITDIR}
install -m755 %{FENCEACKSV_SOURCE}/fenceacksv.sh $RPM_BUILD_ROOT/%{INITDIR}/fenceacksv
install -d -m 755 $RPM_BUILD_ROOT/%{CONFIGDIR}/bootimage-chroot
install -m644 %{FENCEACKSV_SOURCE}/files-fenceacksv.list $RPM_BUILD_ROOT/%{CONFIGDIR}/bootimage-chroot/files.initrd.d/fenceacksv.list
install -m644 %{FENCEACKSV_SOURCE}/rpms-fenceacksv.list $RPM_BUILD_ROOT/%{CONFIGDIR}/bootimage-chroot/rpms.initrd.d/fenceacksv.list
# install -m640 %{FENCEACKSV_SOURCE}/fenceacksv-config.sh $RPM_BUILD_ROOT/%{SYSCONFIGDIR}/fenceacksv

# Files for fence-clients (ilo)
install -d -m 755 $RPM_BUILD_ROOT/%{FENCECLIENTS_DIR}
install -d -m 755 $RPM_BUILD_ROOT/%{FENCECLIENTS_DOC}
install -m755 %{FENCECLIENTS_SOURCE}/fence_ilo.py  $RPM_BUILD_ROOT/%{FENCECLIENTS_DIR}/fence_ilo
install -d -m 755 $RPM_BUILD_ROOT/%{CONFIGDIR}/bootimage/rpms.initrd.d
install -m755 %{FENCECLIENTS_SOURCE}/rpms-fence_ilo.list $RPM_BUILD_ROOT/%{CONFIGDIR}/bootimage/rpms.initrd.d/fence_ilo.list
install -m755 %{FENCECLIENTS_SOURCE}/fence_ilomp.py  $RPM_BUILD_ROOT/%{FENCECLIENTS_DIR}/fence_ilomp
install -m755 %{FENCECLIENTS_SOURCE}/rpms-fence_ilomp.list $RPM_BUILD_ROOT/%{CONFIGDIR}/bootimage/rpms.initrd.d/fence_ilomp.list

# Files for fence-vmware
install -m755 %{FENCECLIENTS_SOURCE}/fence_vmware_client  $RPM_BUILD_ROOT/%{FENCECLIENTS_DIR}
install -m755 %{FENCECLIENTS_SOURCE}/rpms-fence_vmware_client.list $RPM_BUILD_ROOT/%{CONFIGDIR}/bootimage/rpms.initrd.d/fence_vmware_client.list
install -m755 %{FENCECLIENTS_SOURCE}/fence_vmware_master  $RPM_BUILD_ROOT/%{FENCECLIENTS_DIR}
install -m755 %{FENCECLIENTS_SOURCE}/README.fence_vmware  $RPM_BUILD_ROOT/%{FENCECLIENTS_DOC}
install -m755 %{FENCECLIENTS_SOURCE}/INSTALL.fence_vmware  $RPM_BUILD_ROOT/%{FENCECLIENTS_DOC}

%postun

if [ "$1" -eq 0 ]; then
  echo "Postuninstalling comoonics-bootimage.."
  find /etc/comoonics/bootimage -name "files*.list" -o -name "rpms*.list" -type l -exec rm -f {} \; &>/dev/null
  root_fstype=$(mount | grep "/ " | awk '
BEGIN { exit_c=1; }
{ if ($5) {  print $5; exit_c=0; } }
END{ exit exit_c}')
  if [ "$root_fstype" != "gfs" ]; then
    /sbin/chkconfig --add cman &>/dev/null
    /sbin/chkconfig --list cman
    /sbin/chkconfig --add gfs &>/dev/null
    /sbin/chkconfig --list gfs
  fi
  rm %{APPDIR}/mkinitrd
  rm %{ENVFILE}
fi

%post

echo "Starting postinstall.."
echo "Checking %{ENVFILE}"
if ! $(grep '%{APPDIR}' %{ENVFILE} > /dev/null 2>&1); then
    echo "Patching path.."
    echo 'PATH=%{APPDIR}:${PATH}' >> %{ENVFILE}
fi
echo "Creating mkinitrd link..."
ln -sf %{APPDIR}/create-gfs-initrd-generic.sh %{APPDIR}/mkinitrd

if cat /etc/redhat-release | grep -i "release 5" &> /dev/null; then
	services="cman gfs clvmd qdiskd"
else
	services="cman gfs clvmd qdiskd"
fi

echo "Disabling services ($services)"
for service in $services; do
   /sbin/chkconfig --del $service &> /dev/null
done
/bin/true

echo 'Information:
Cluster services will be started in a chroot environment. Check out latest documentation
on http://www.open-sharedroot.org
If you want syslog to log fence messages you should add an additional logdevice
to the syslog configuration
(command switch syslogd -a $(cat /var/comoonics/chrootpath)/dev/log)

CAUTION:
- tmpwatch:
if you use the /tmp filesystem for your chroot environment,
and tmpwatch is installed, you need to modify
/etc/cron.daily/tmpwatch to fit your needs.
'

%post fenceacksv
echo "Setting up fenceacksv"
pushd %{FENCEACKSV_DIR} >/dev/null
ln -sf fence_ack_server.py fenceacksv
popd >/dev/null
chkconfig --add fenceacksv &> /dev/null
chkconfig --list fenceacksv
echo "Done"

%preun fenceacksv
if [ "$1" -eq 0 ]; then
  echo "Uninstalling fenceacksv"
  chkconfig --del fenceacksv
fi

%files

%dir %{APPDIR}/boot-scripts/sys
%dir %{APPDIR}/boot-scripts/var/log
%dir %{APPDIR}/boot-scripts/var/lib/dhcp
%dir %{APPDIR}/boot-scripts/var/run/netreport
%dir %{APPDIR}/boot-scripts/proc
%dir %{APPDIR}/boot-scripts/dev
%attr(750, root, root) %{APPDIR}/create-gfs-initrd-generic.sh
%attr(640, root, root) %{APPDIR}/create-gfs-initrd-lib.sh
%attr(750, root, root) %{APPDIR}/manage_chroot.sh
%attr(750, root, root) %{APPDIR}/boot-scripts/com-halt.sh
%attr(750, root, root) %{APPDIR}/boot-scripts/com-realhalt.sh
%attr(750, root, root) %{APPDIR}/boot-scripts/linuxrc.generic.sh
%attr(750, root, root) %{APPDIR}/boot-scripts/exec_part_from_bash.sh
%attr(750, root, root) %{APPDIR}/boot-scripts/detectHardware.sh
%attr(750, root, root) %{APPDIR}/boot-scripts/rescue.sh
%attr(750, root, root) %{APPDIR}/boot-scripts/linuxrc
%attr(750, root, root) %{APPDIR}/boot-scripts/linuxrc.bash
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/atix.txt
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/boot-lib.sh
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/chroot-lib.sh
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/clusterfs-lib.sh
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/comoonics-release
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/defaults.sh
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/ext3-lib.sh
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/gfs-lib.sh
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/hardware-lib.sh
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/inittab
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/iscsi-lib.sh
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/network-lib.sh
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/nfs-lib.sh
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/xen-lib.sh
#%attr(640, root, root) %{APPDIR}/boot-scripts/etc/passwd
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/stdfs-lib.sh
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/std-lib.sh
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/sysconfig/comoonics
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/rhel4/boot-lib.sh
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/rhel4/hardware-lib.sh
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/rhel4/network-lib.sh
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/rhel5/boot-lib.sh
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/rhel5/gfs-lib.sh
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/rhel5/hardware-lib.sh
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/rhel5/network-lib.sh
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/sles8/hardware-lib.sh
%attr(640, root, root) %{APPDIR}/boot-scripts/etc/sles8/network-lib.sh

%dir %{CONFIGDIR}/bootimage-chroot
%attr(640, root, root) %{CONFIGDIR}/bootimage-chroot/files.list
%attr(640, root, root) %{CONFIGDIR}/bootimage-chroot/rpms.list
%dir %{CONFIGDIR}/bootimage-chroot/files.initrd.d
%dir %{CONFIGDIR}/bootimage-chroot/rpms.initrd.d

%config(noreplace) %{CONFIGDIR}/comoonics-bootimage.cfg
%config(noreplace) %{CONFIGDIR}/bootimage/files.initrd.d/user_edit.list

%doc CHANGELOG

%files compat
%attr(640, root, root) %{SYSCONFIGDIR}/comoonics-chroot

%files extras-network
%attr(640, root, root) %{CONFIGDIR}/bootimage/files.initrd.d/vlan.list

%files extras-nfs
%attr(640, root, root) %{CONFIGDIR}/bootimage/rpms.initrd.d/nfs.list

%files extras-dm-multipath
%attr(640, root, root) %{CONFIGDIR}/bootimage/rpms.initrd.d/dm_multipath.list

%files extras-rdac-multipath
%attr(640, root, root) %{CONFIGDIR}/bootimage/files.initrd.d/rdac_multipath.list

%files extras-xen
%attr(640, root, root) %{CONFIGDIR}/bootimage/files.initrd.d/xen.list
%attr(640, root, root) %{CONFIGDIR}/bootimage/rpms.initrd.d/xen.list

%files extras-iscsi
%attr(640, root, root) %{CONFIGDIR}/bootimage/files.initrd.d/iscsi.list
%attr(640, root, root) %{CONFIGDIR}/bootimage/rpms.initrd.d/iscsi.list

%files fenceacksv
%attr(755, root, root) %{FENCEACKSV_DIR}/fence_ack_server.py
#%attr(755, root, root) %{FENCEACKSV_DIR}/fence_ack_server.pyc
#%attr(755, root, root) %{FENCEACKSV_DIR}/fence_ack_server.pyo
%attr(644, root, root) %{FENCEACKSV_DIR}/shell.py
#%attr(644, root, root) %{FENCEACKSV_DIR}/shell.pyc
#%attr(644, root, root) %{FENCEACKSV_DIR}/shell.pyo
%attr(640, root, root) %{FENCEACKSV_DIR}/server.pkey
%attr(640, root, root) %{FENCEACKSV_DIR}/server.cert
%attr(640, root, root) %{FENCEACKSV_DIR}/CA.pkey
%attr(640, root, root) %{FENCEACKSV_DIR}/CA.cert
%attr(755, root, root) %{INITDIR}/fenceacksv
%attr(644, root, root) %{CONFIGDIR}/bootimage-chroot/files.initrd.d/fenceacksv.list
%attr(644, root, root) %{CONFIGDIR}/bootimage-chroot/rpms.initrd.d/fenceacksv.list
#%config(noreplace)     %{SYSCONFIGDIR}/fenceacksv
%doc CHANGELOG

%files fenceclient-ilo
%attr(755, root, root) %{FENCECLIENTS_DIR}/fence_ilo
%attr(640, root, root) %{CONFIGDIR}/bootimage/rpms.initrd.d/fence_ilo.list
%doc CHANGELOG

%files fenceclient-ilomp
%attr(755, root, root) %{FENCECLIENTS_DIR}/fence_ilomp
%attr(640, root, root) %{CONFIGDIR}/bootimage/rpms.initrd.d/fence_ilomp.list
%doc CHANGELOG

%files fenceclient-vmware
%attr(755, root, root) %{FENCECLIENTS_DIR}/fence_vmware_client
%doc %{FENCECLIENTS_DOC}/INSTALL.fence_vmware
%doc %{FENCECLIENTS_DOC}/README.fence_vmware
%attr(640, root, root) %{CONFIGDIR}/bootimage/rpms.initrd.d/fence_vmware_client.list
%doc CHANGELOG

%files fencemaster-vmware
%attr(755, root, root) %{FENCECLIENTS_DIR}/fence_vmware_master
%doc %{FENCECLIENTS_DOC}/INSTALL.fence_vmware
%doc %{FENCECLIENTS_DOC}/README.fence_vmware
%doc CHANGELOG

%clean
rm -rf %{buildroot}


%changelog
* Mon Oct 17 2007 Marc Grimme <grimme@atix.de> 1.3-21
- Fixed Bug 144, where mounoptions where not used
- Added ISCSI Support preview (thanks to Gordan Bobic)
- Fixed Bug 142, where in RHEL4 qdiskd could not be started
* Wed Oct 10 2007 Mark Hlawatschek <hlawatschek@atix.de> 1.3-20
- Fixes BUG 114
- Fixes BUG 139
* Wed Oct 10 2007 Mark Hlawatschek <hlawatschek@atix.de> 1.3-19
- Fixes BUG 138
* Tue Oct 09 2007 Mark Hlawatschek <hlawatschek@atix.de> 1.3-18
- Another fix for BUG 136
- start syslogd in chroot
* Mon Oct 08 2007 Marc Grimme <grimme@atix.de> 1.3-17
- readded usb (hid) Support
- added stabilized for having stabilized files
* Mon Oct 08 2007 Mark Hlawatschek <hlawatschek@atix.de> 1.3-16
- Fixed BUG 136
* Fri Oct 05 2007 Marc Grimme <grimme@atix.de> 1.3-15
- added xensupport
* Tue Oct 02 2007 Marc Grimme <grimme@atix.de> 1.3-14
- Fixed BUG 127, chrootenv and /etc/sysconfig/comoonics-chroot would not work before
- Fixed BUG 128, chroot was not build correctly if oldone existed
- Fixed BUG 130, fenced is hanging because dev-bindmounts do not work
* Thu Sep 27 2007 Marc Grimme <grimme@atix.de> 1.3-13
- Fixed BUG 125 (qdisk was wrongly started)
- Fixed Problem with hardware detection (/etc/passwd) has to be removed
* Wed Sep 26 2007 Mark Hlawatschek <hlawatschek@atix.de> 1.3.12
- modifications and bugfixes for el5
* Tue Sep 18 2007 Mark Hlawatschek <hlawatschek@atix.de> 1.3.11
- modifications for el5, bugfixes
* Tue Sep 18 2007 Mark Hlawatschek <hlawatschek@atix.de> 1.3.10
- bugfixes
* Fri Sep 14 2007 Marc Grimme <grimme@atix.de> - 1.3-8
- added support for rdac multipath
* Wed Aug 08 2007 Mark Hlawatschek <hlawatschek@atix.de> 1.3.4
- moved dm_multipath listfile into extra rpm
* Wed Aug 08 2007 Mark Hlawatschek <hlawatschek@atix.de> 1.3.3
- minor bugfixes
* Tue Aug 07 2007 Mark Hlawatschek <hlawatschek@atix.de> 1.3.2
- minor bugfixes
* Tue Aug 07 2007 Mark Hlawatschek <hlawatschek@atix.de> 1.3.1
- new major bootimage revision
* Tue Jul 24 2007 Mark Hlawatschek <hlawatschek@atix.de> 1.2.03
- added support for fence_ipmilan
* Wed May 23 2007 Mark Hlawatschek <hlawatschek@atix.de> 1.2.02
- added support for RHEL4u5
* Wed Apr 11 2007 Mark Hlawatschek <hlawatschek@atix.de> 1.2.01
- modified switchroot to 2.6 style
- added nfs rootfs support
- added ext3 rootfs supprt
- seperated fs and cluster type
* Fri Feb 09 2007 Mark Hlawatschek <hlawatschek@atix.de> 1.0.81
- added support for dm_multipath partitions
* Fri Feb 09 2007 Marc Grimme <grimme@atix.de> 1.0.81-rc
- added nodeid parameter at boottime (bonding not clear)
- bootsr will only rebuild if needed
- added nsswitch.conf to chroot. Because of ccs_tool update sometime failed.
- better step continue mode
* Mon Jan 22 2007 Mark Hlawatschek <hlawatschek at atix.de> 1.0.73
- added changelog
- added support for vlan devices
- added support for kernel cmdline initlevel
- added dstep-mode kernel parameter -> ask (Y|n|c) with evey exec_local
* Fri May 12 2006  <grimme@atix.de> - 1.0-7
- First stable 1.0 Version is RPM 1.0-7

* Wed Jan 25 2006  <grimme@atix.de> - 0.3-12
- First stable 0.3 version


* Mon Jan  3 2005 Marc Grimme <grimme@atix.de> - 0.1-16
- first offical rpm version

%changelog extras-rdac-multipath
* Fri Sep 14 2007 Marc Grimme <grimme@atix.de> - 0.1-1
- first release

%changelog extras-xen
* Tue Oct 18 2007 Marc Grimme <grimme@atix.de> - 0.1-2
- added nss rpm for fence_xvm
* Wed Oct 03 2007 Marc Grimme <grimme@atix.de> - 0.1-1
- first release

%changelog extras-iscsi
* Fri Oct 12 2007 Marc Grimme <grimme@atix.de> - 0.1-1
- first release

%changelog fenceacksv
* Mon Sep 10 2007 Marc Grimme <grimme@atix.de> - 0.3-1
  - Fixed Bug BZ#107, fixed problems with not installed plugins
  - Fixed Bug BZ#29, output of ackmanual
  - Rewritten
  - Support for plugins (available: sysrq, sysreport)
* Mon Sep 10 2007 Mark Hlawatschek <hlawatschek@atix.de> - 0.2-1
  - first release for 1.3 bootimage
* Wed Feb 07 2007 Marc Grimme <grimme@atix.de> - 0.1-11
- introducted changelog

%changelog fenceclient-ilo
* Mon Jul 30 2007 Marc Grimme <grimme@atix.de> - 0.1-17
- added help for -x|--xmlfile (#BZ 39)
* Wed Feb 07 2007 Marc Grimme <grimme@atix.de - 0.1-16
- introducted changelog

%changelog fenceclient-vmware
* Wed Feb 07 2007 Marc Grimme <grimme@atix.de - 0.1-4
- introducted changelog

%changelog fencemaster-vmware
* Wed Feb 07 2007 Marc Grimme <grimme@atix.de - 0.1-1
- introducted changelog

# ------
# $Log: comoonics-bootimage.spec,v $
# Revision 1.64  2007-10-18 08:22:37  marc
# - new version of extras-xen 0.1-2
#
# Revision 1.63  2007/10/18 08:15:27  mark
# new build
#
# Revision 1.62  2007/10/16 08:04:33  marc
# - added get_rootsource
# - fixed BUG 142
# - lvm switch support
#
# Revision 1.61  2007/10/11 07:34:37  mark
# new revision
#
# Revision 1.60  2007/10/10 19:50:52  marc
# new version 1.3-20
#
# Revision 1.59  2007/10/10 15:11:07  mark
# new release
#
# Revision 1.58  2007/10/10 12:29:16  mark
# new release
#
# Revision 1.57  2007/10/09 14:25:12  marc
# - new release of comoonics-bootimage 1.3-17
#
# Revision 1.56  2007/10/08 16:15:05  mark
# new release
#
# Revision 1.55  2007/10/05 14:09:53  mark
# new revision
#
# Revision 1.54  2007/10/05 10:10:13  marc
# - new version comoonics-bootimage-1.3-15
#
# Revision 1.53  2007/10/02 12:16:30  marc
# - new release comoonics-bootimage-1.3-14
#
# Revision 1.52  2007/09/27 11:56:14  marc
# new version of comoonics-bootimage-1.3-13
#
# Revision 1.51  2007/09/26 11:55:51  mark
# new releases
#
# Revision 1.50  2007/09/21 15:34:51  mark
# new release
#
# Revision 1.49  2007/09/18 11:21:15  mark
# bootimage-1.3.10
#
# Revision 1.48  2007/09/15 14:49:38  mark
# moved listfiles into extra rpms
#
# Revision 1.47  2007/09/14 13:35:52  marc
# added rdac-rpm and comments
#
# Revision 1.46  2007/09/13 09:06:44  mark
# merged changes
#
# Revision 1.45  2007/09/12 13:48:05  mark
# moved initscripts into another specfile
#
# Revision 1.44  2007/09/10 15:03:18  marc
# - new version of fenceacksv 0.3-1
#
# Revision 1.43  2007/09/10 09:24:01  marc
# -new version of fenceacksv 0.3-1
#
# Revision 1.42  2007/09/07 08:30:25  mark
# merged fixes from 1.2
#
# Revision 1.41  2007/09/07 07:55:42  mark
# removed tmpwatch conflict
# added rhel5 parts
#
# Revision 1.40  2007/08/29 06:46:13  marc
# setting AUTOREQ: NO for vmware agent
#
# Revision 1.39  2007/08/08 14:25:17  mark
# release 1.3.4
#
# Revision 1.38  2007/08/07 12:42:38  mark
# added release 1.3.1
# added extras-nfs
# added extras-network
#
# Revision 1.37  2007/07/30 06:47:12  marc
# added help for -x|--xmlfile (#BZ 39)
#
# Revision 1.36  2007/07/24 17:05:34  mark
# added 1.2.03
#
# Revision 1.35  2007/05/23 15:30:00  mark
# version 1.2.02
#
# Revision 1.34  2007/03/01 10:50:04  marc
# changed getopt
#
# Revision 1.33  2007/02/23 16:44:50  mark
# revision 1.0.81
#
# Revision 1.32  2007/02/09 11:08:17  marc
# new version 81
#
# Revision 1.31  2007/01/23 12:57:14  mark
# new release 1.0.75
#
# Revision 1.30  2006/12/04 17:37:12  marc
# new versions
#
# Revision 1.29  2006/11/10 11:38:29  mark
# release 1.0.73
# added conflicts tmpwatch and tmpwatch warnings
#
# Revision 1.28  2006/10/26 16:13:24  mark
# release got from src.rpm
# added support for ccsd-chroot
#
# Revision 1.27  2006/10/06 08:36:27  marc
# version with quorumack
#
# Revision 1.26  2006/08/28 16:00:27  marc
# very well tested version
#
# Revision 1.25  2006/08/14 17:42:41  marc
# new version with max_drop_count and fenced from local disk
#
# Revision 1.24  2006/07/19 15:14:39  marc
# removed the fence-tool lists for chroot
#
# Revision 1.23  2006/07/19 15:11:36  marc
# fixed fence_bug for x86_64
#
# Revision 1.22  2006/07/13 11:35:16  marc
# new version changing file xtensions
#
# Revision 1.21  2006/07/03 08:33:59  marc
# new version
#
# Revision 1.20  2006/06/19 15:57:40  marc
# added devicemapper support
#
# Revision 1.19  2006/06/09 14:04:05  marc%attr(640, root, root) %{CONFIGDIR}/bootimage/files.initrd.d/configs.list

# new version.
#
# Revision 1.18  2006/06/07 09:42:23  marc
# *** empty log message ***
#
# Revision 1.17  2006/05/12 13:01:56  marc
# First stable 1.0 Version
#
# Revision 1.16  2006/05/07 12:06:56  marc
# version 1.0 stable
#
# Revision 1.15  2006/05/03 12:47:17  marc
# added documentation
#
# Revision 1.14  2006/04/13 18:52:09  marc
# latest versino
#
# Revision 1.13  2006/04/13 18:46:31  marc
# new version
#
# Revision 1.12  2006/04/11 13:42:45  marc
# cvs stable version
#
# Revision 1.11  2006/04/11 13:41:20  marc
# added hostnames and x86_64 support
#
# Revision 1.10  2006/02/16 13:59:06  marc
# stable version 20
#
# Revision 1.9  2006/01/28 15:01:49  marc
# fenced is restarted in the initrd
#
# Revision 1.8  2006/01/25 14:55:51  marc
# first stable 0.3
#
# Revision 1.7  2006/01/23 14:05:30  mark
# added bootsr
#
# Revision 1.6  2005/07/08 13:15:57  mark
# added some files
#
# Revision 1.5  2005/06/27 14:24:20  mark
# added gfs 61, rhel4 support
#
# Revision 1.4  2005/06/08 13:33:22  marc
# new revision
#
# Revision 1.3  2005/01/05 10:57:07  marc
# new release and added the latest files.
#
# Revision 1.2  2005/01/03 08:34:16  marc
# added new subversion for first offical rpm version
#
# Revision 1.1  2005/01/03 08:33:17  marc
# first offical rpm version
# - initial revision
#
#
