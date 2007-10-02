#!/bin/bash
#
# $Id: linuxrc.generic.sh,v 1.41 2007-10-02 12:16:02 marc Exp $
#
# @(#)$File$
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
#
#****h* comoonics-bootimage/linuxrc.generic.sh
#  NAME
#    linuxrc
#    $Id: linuxrc.generic.sh,v 1.41 2007-10-02 12:16:02 marc Exp $
#  DESCRIPTION
#    The first script called by the initrd.
#*******

#****b* comoonics-bootimage/linuxrc/com-stepmode
#  NAME
#    com-stepmode
#  DESCRIPTION
#   If set it asks for <return> after every step
#***** com-step

#****b* comoonics-bootimage/linuxrc/com-debug
#  NAME
#    com-debug
#  DESCRIPTION
#    If set debug info is output
#***** com-debug

#****f* linuxrc.generic.sh/main
#  NAME
#    main
#  SYNOPSIS
#    function main()
#  MODIFICATION HISTORY
#  IDEAS
#
#  SOURCE
#
# initstuff is done in here

. /etc/sysconfig/comoonics

. /etc/chroot-lib.sh
. /etc/boot-lib.sh
. /etc/hardware-lib.sh
. /etc/network-lib.sh
. /etc/clusterfs-lib.sh
. /etc/std-lib.sh
. /etc/stdfs-lib.sh
. /etc/defaults.sh

clutype=$(getCluType)
. /etc/${clutype}-lib.sh

# including all distribution dependent files
distribution=$(getDistribution)
[ -e /etc/${distribution}/hardware-lib.sh ] && source /etc/${distribution}/hardware-lib.sh
[ -e /etc/${distribution}/network-lib.sh ] && source /etc/${distribution}/network-lib.sh
[ -e /etc/${distribution}/clusterfs-lib.sh ] && source /etc/${distribution}/clusterfs-lib.sh
[ -e /etc/${distribution}/${clutype}-lib.sh ] && source /etc/${distribution}/${clutype}-lib.sh

echo_local "Starting ATIX initrd"
echo_local "Comoonics-Release"
release=$(cat /etc/comoonics-release)
echo_local "$release"
echo_local 'Internal Version $Revision: 1.41 $ $Date: 2007-10-02 12:16:02 $'
echo_local "Builddate: "$(date)

initBootProcess

x=`cat /proc/version`;
KERNEL_VERSION=`expr "$x" : 'Linux version \([^ ]*\)'`
echo_local "Kernel-version: ${KERNEL_VERSION}"
if [ "${KERNEL_VERSION:0:3}" = "2.4" ]; then
  modules_conf="/etc/modules.conf"
else
  modules_conf="/etc/modprobe.conf"
fi

# boot parameters
echo_local -n "Scanning for Bootparameters..."
bootparms=$(getBootParameters)
return_code=$?
debug=$(getParm ${bootparms} 1)
stepmode=$(getParm ${bootparms} 2)
mount_opts=$(getParm ${bootparms} 3)
tmpfix=$(getParm ${bootparms} 4)
scsifailover=$(getParm ${bootparms} 5)
dstepmode=$(getParm ${bootparms} 6)
return_code 0

# network parameters
echo_local -n "Scanning for network parameters..."
netparms=$(getNetParameters)
ipConfig=$(getParm ${netparms} 1)
return_code 0

# clusterfs parameters
echo_local -n "Scanning for clusterfs parameters..."
cfsparams=$(getClusterFSParameters)
rootsource=$(getParm ${cfsparams} 1)
root=$(getParm ${cfsparams} 2)
lockmethod=$(getParm ${cfsparams} 3)
sourceserver=$(getParm ${cfsparams} 4)
quorumack=$(getParm ${cfsparams} 5)
nodeid=$(getParm ${cfsparams} 6)
nodename=$(getParm ${cfsparams} 7)
rootfs=$(getParm ${cfsparams} 8)
return_code 0

if [ -n "$rootsource" ] && [ "$rootsource" = "iscsi" ]; then
    source /etc/iscsi-lib.sh
    source /etc/${distribution}/iscsi-lib.sh
fi

check_cmd_params $*

echo_local_debug "*****************************"
echo_local_debug "Debug: $debug"
echo_local_debug "Stepmode: $stepmode"
echo_local_debug "Debug-stepmode: $dstepmode"
echo_local_debug "Clutype: $clutype"
echo_local_debug "mount_opts: $mount_opts"
echo_local_debug "tmpfix: $tmpfix"
echo_local_debug "ip: $ipConfig"
echo_local_debug "rootsource: $rootsource"
echo_local_debug "root: $root"
echo_local_debug "lockmethod: $lockmethod"
echo_local_debug "sourceserver: $sourceserver"
echo_local_debug "scsifailover: $scsifailover"
echo_local_debug "quorumack: $quorumack"
echo_local_debug "nodeid: $nodeid"
echo_local_debug "nodename: $nodename"
echo_local_debug "rootfs: $rootfs"
echo_local_debug "clutype: $clutype"
echo_local_debug "*****************************"

echo_local_debug "*****************************"
# step
echo_local -en $"\t\tPress 'I' to enter interactive startup."
echo_local

{
 sleep 2
 hardware_detect

 echo_local "Starting network configuration for lo0"
 exec_local nicUp lo
 return_code
 auto_netconfig
} &
read -n1 -t5 confirm
if [ "$confirm" = "i" ]; then
  echo_local -e "\t\tInteractivemode recognized. Switching step_mode to on"
  stepmode=1
fi
wait

step "Inialization started"

# cluster_conf is set in clusterfs-lib.sh or overwritten in gfs-lib.sh
# FIXME: This overrides boot setting !
# BUG: bz#31

cfsparams=( $(clusterfs_config $cluster_conf $ipConfig $nodeid $nodename ) )
echo "cfsparams: $cfsparams"
nodeid=${cfsparams[0]}
nodename=${cfsparams[1]}
rootvolume=${cfsparams[2]}
_mount_opts=${cfsparams[3]}
_scsifailover=${cfsparams[4]}
rootfs=${cfsparams[5]}
_ipConfig=${cfsparams[@]:6}
[ -n "$_ipConfig" ] && ( [ -z "$ipConfig" ] || [ "$ipConfig" = "cluster" ] ) && ipConfig=$_ipConfig
[ -n "$_mount_opts" ] && [ -z "$mount_opts" ] && mount_opts=$_mount_opts
[ -n "$_scsifailover" ] && [ -z "$scsifailover" ] && scsifailover=$_scsifailover
[ -z "$root" ] || [ "$root" = "/dev/ram0" ] && root=$rootvolume
cc_auto_hosts $cluster_conf

echo_local_debug "*****************************"
echo_local_debug "nodeid: $nodeid"
echo_local_debug "nodename: $nodename"
echo_local_debug "rootvolume: $rootvolume"
echo_local_debug "scsifailover: $scsifailover"
echo_local_debug "rootfs: $rootfs"
echo_local_debug "ipConfig: $ipConfig"
echo_local_debug "*****************************"

step "Parameter loaded"

if [ "$clutype" != "$rootfs" ]; then
	source /etc/${rootfs}-lib.sh
	[ -e /etc/${distribution}/${rootfs}-lib.sh ] && source /etc/${distribution}/${rootfs}-lib.sh
fi

netdevs=""
for ipconfig in $ipConfig; do
  dev=$(getPosFromIPString 6, $ipconfig)

#  echo_local "Device $dev"
  # Special case for bonding
  { echo "$dev"| grep "^bond" && grep -v "alias $dev" $modules_conf; } >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    # Think about bonding parameters.
    # Multi load of bonding driver possible?
    echo_local -n "Patching $modules_conf for bonding "
    echo "alias $dev bonding" >> $modules_conf
    return_code $?
    depmod -a >/dev/null 2>&1
  fi

  nicConfig $ipconfig

  echo_local -n "Powering up $dev.."
  exec_local nicUp $dev >/dev/null 2>&1
  return_code
  netdevs="$netdevs $dev"
done

step "Network configuration started"


dm_start
scsi_start $scsifailover

# loads kernel modules for cluster stack
# TODO: - rename to clusterfs_kernel_load
#       - add cluster_kernel_load
#       - move below ?
# 1.3.+ ?
clusterfs_load $lockmethod
return_code

step "Hardware detected, modules loaded"

echo_local -n "Starting udev "
exec_local udev_start
return_code

if [ "$scsifailover" = "mapper" ] || [ "$scsifailover" = "devicemapper" ]; then
  dm_mp_start
fi
step "UDEV started"

lvm_start

step "LVM subsystem started"


# TODO:
# - mount chroot from either
#   - local disk defined in /etc/sysconfig/comoonics-chroot
#   - cluster.conf
#   - ramdisk
# - create chroot environment in /comoonics by
#   - copy everything from / except /lib/modules
#   - mount --bind /dev /comoonics/dev
#   - mount -t proc proc /comoonics/proc ?
#   - mount -t sysfs none /comoonics/sys

# TODO:
# Put all things into a library function

echo_local -n "Building comoonics chroot environment"
res=( $(build_chroot $cluster_conf $nodename) )
chroot_mount=${res[0]}
chroot_path=${res[1]}
return_code $?

echo_local_debug "res: $res -> chroot_mount=$chroot_mount, chroot_path=$chroot_path"


step "chroot environment created"

# TODO: start syslog in /comoonics ?
cc_auto_syslogconfig $cluster_conf $nodename
start_service /sbin/syslogd no_chroot -m 0

step "Syslog service started"


if [ -z "$quorumack" ]; then
  echo_local -n "Checking for all nodes to be available"
  exec_local cluster_checkhosts_alive
  return_code
  if [ $return_c -ne 0 ]; then
  	echo_local ""
  	echo_local ""
  	echo_local "I couldn't talk to the required number of cluster nodes."
	echo_local "To avoid data inconsitency caused by cluster partitioning (split brain) "
	echo_local "the next step has to be acknowledged manually."
	echo_local ""
	echo_local "If you are sure, that the cluster is in a consistent state, please type YES."
	echo_local ""
	echo_local ""
	echo_local "CAUTION: !!! If you are unsure about all other nodes state, check first."
	echo_local "         Otherwise you'll risk split brain with data inconsistency !!!"

	confirm="XXX"
	if [ $debug ]; then set -x; fi
	until [ $confirm == "YES" ] || [ $confirm == "NO" ]; do
  		echo_local "USER INPUT: (YES|NO): "
  		read confirm
  		echo_local_debug "confirm: $confirm"
  		if [ $confirm == "NO" ]; then
  			echo_local "Cluster not acknowledged. Falling back to shell"
  			exit_linuxrc 1
  		fi
  	done
  	if [ $debug ]; then set +x; fi
  fi
fi

setHWClock
clusterfs_services_start $chroot_path $lockmethod

if [ $return_c -ne 0 ]; then
   echo_local "Could not start all cluster services. Exiting"
   exit_linuxrc 1
fi
sleep 5

step "Cluster services started"

clusterfs_mount $rootfs $root $newroot $mount_opts 3 5
if [ $return_c -ne 0 ]; then
   echo_local "Could not mount cluster filesystem $rootfs $root to $mount_point. Exiting ($mount_opts)"
   exit_linuxrc 1
fi

step "RootFS mounted"

clusterfs_mount_cdsl $newroot $cdsl_local_dir $nodeid $cdsl_prefix
if [ $return_c -ne 0 ]; then
   echo_local "Could not mount cdsl $cdsl_local_dir to ${cdsl_prefix}/$nodeid. Exiting"
   exit_linuxrc 1
fi

step "CDSL tree mounted"

#if [ -n "$debug" ]; then set -x; fi
#TODO clean up method
#copy_relevant_files $cdsl_local_dir $newroot $netdevs
#if [ -n "$debug" ]; then set +x; fi
step


# TODO:
# remove tmpfix as this is replaced with /comoonics
if [ -n "$tmpfix" ]; then
  echo_local -n "Setting up tmp..."
  exec_local createTemp /dev/ram1
  return_code
fi


echo_local -n "Mounting the device file system"
#TODO
# try an exec_local mount --move /dev $newroot/dev
exec_local mount --move /dev $newroot/dev
_error=$?
exec_local cp -a $newroot/dev/console /dev/
#exec_local mount --bind /dev $newroot/dev
return_code $_error

echo_local -n "Copying logfile to $newroot/${bootlog}..."
exec_local cp -f ${bootlog} ${newroot}/${bootlog} || cp -f ${bootlog} ${newroot}/$(basename $bootlog)
if [ -f ${newroot}/$bootlog ]; then
  bootlog=${newroot}/$bootlog
else
  bootlog=${newroot}/$(basename $bootlog)
fi
return_code_warning
exec 3>> $bootlog
exec 4>> $bootlog
step "Logfiles copied"

# FIXME: Remove line
#bootlog="/var/log/comoonics-boot.log"

#TODO: remove lines as syslog can will stay in /comoonics
echo_local -n "Stopping syslogd..."
exec_local stop_service "syslogd" / &&
return_code

echo_local -n "Moving chroot environment to $newroot"
move_chroot $chroot_mount $newroot/$chroot_mount
return_code

echo_local -n "Writing information ..."
exec_local mkdir -p $newroot/var/comoonics
echo $chroot_path > $newroot/var/comoonics/chrootpath
return_code

echo_local -n "cleaning up initrd ..."
exec_local clean_initrd
success
echo

step "Initialization completed."

echo_local "Starting init-process ($init_cmd)..."
exit_linuxrc 0 "$init_cmd" "$newroot"

#********** main

###############
# $Log: linuxrc.generic.sh,v $
# Revision 1.41  2007-10-02 12:16:02  marc
# - cosmetic changes to prevent unnecesarry ugly FAILED
#
# Revision 1.40  2007/09/27 09:34:32  marc
# - comment out copy_relevant_files because of problems with kudzu
#
# Revision 1.39  2007/09/26 11:56:02  marc
# cosmetic changes
#
# Revision 1.38  2007/09/26 11:40:48  mark
# moved network config before storage config
#
# Revision 1.37  2007/09/18 10:06:36  mark
# removed unneeded code
#
# Revision 1.36  2007/09/14 13:28:54  marc
# - Fixed Bug BZ#31
#
# Revision 1.35  2007/09/07 08:04:18  mark
# added cleanup_initrd
#
# Revision 1.34  2007/08/06 15:56:14  mark
# new chroot environment
# bootimage release 1.3
#
# Revision 1.33  2007/05/23 09:15:35  mark
# added support fur RHEL4u5
#
# Revision 1.32  2007/03/09 18:01:11  mark
# added support for nash like switchRoot
#
# Revision 1.31  2007/02/09 11:06:16  marc
# added nodeid and nodename
#
# Revision 1.30  2007/01/19 13:40:20  mark
# init_cmd uses full cmdline /proc/cmdline like nash
# fixes bug #21
#
# Revision 1.29  2006/11/10 11:37:10  mark
# modified quorumack user input
# added retry:3 waittime:5 to clusterfs_mount
#
# Revision 1.28  2006/10/06 08:35:15  marc
# added quorumack functionality
#
# Revision 1.27  2006/07/19 15:12:26  marc
# mulitpath dmapper bugfix with devices
#
# Revision 1.26  2006/07/13 14:14:57  marc
# udev_start as function
#
# Revision 1.25  2006/07/03 08:32:03  marc
# added step
#
# Revision 1.24  2006/06/19 15:56:13  marc
# added devicemapper support
#
# Revision 1.23  2006/06/07 09:42:23  marc
# *** empty log message ***
#
# Revision 1.22  2006/05/12 13:02:24  marc
# Major changes for Version 1.0.
# Loads of Bugfixes everywhere.
#
# Revision 1.21  2006/05/07 11:34:58  marc
# major change to version 1.0.
# Complete redesign.
#
# Revision 1.20  2006/05/03 12:46:24  marc
# added documentation
#
# Revision 1.19  2006/01/28 15:10:23  marc
# added cvs tags
#
