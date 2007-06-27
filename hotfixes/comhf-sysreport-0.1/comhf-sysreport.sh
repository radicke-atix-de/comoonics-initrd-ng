#!/bin/bash

#****h* comoonics-bootimage/hotfixes/com-sysinfo/com-sysreport.sh
#  NAME
#    com-sysreport.sh
#    $id $
#  DESCRIPTION
#*******
#
# $Id: comhf-sysreport.sh,v 1.4 2007-06-27 13:38:14 marc Exp $
#
# @(#)$File$
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
#

# This package is only a temporary workaround for the following fixes:
# 1. dynamically update the local chroot environment (fenceack-server)
# 2. collect system information from a fenceack-server shell

vardir=/var/com-sysinfo
mydir=$vardir/$(date +%F-%H%M%S)
resdir=$mydir/results
logfile=$mydir/com-sysinfo.log
repfile=$(hostname)_sysreport_$(date +%F).tgz
chrootdir="/tmp/fence_tool"

function usage() {
	echo "`basename $0` [ [-h] | [-v] ]"
	echo "  -h help "
	echo "  -v be chatty"
	echo "  -V show version"
}

function log() {
	if [ "$verbose" ]; then
		echo $*
	fi
	echo "$(date): $*" >> $logfile
}

function rc2str() {
	if [ $1 -ne 0 ]; then
		echo "[ ERROR ]"
	else
		echo "[   OK  ]"
	fi
}

function do_pre() {
	mkdir -p $resdir

	log "preparing chroot environment"
	log " - mounting /proc"
	if [ ! -d /proc ]; then
		log "/proc does not exist I'll create it"
		mkdir /proc
	fi
	mount -t proc none /proc

}

function do_post() {
	log "cleaning up"
	log " - umounting /proc"
	umount /proc

}

# borrowed from redhats sysreport
function catifexec() {
  if [ -x $1 ]; then
    log "$*"
    echo -n $STATUS
    echo "$*" >> $resdir/`/bin/basename $1`
    $* >> $resdir/`/bin/basename $1` 2>&1
    echo $(rc2str 0)
    return 1
  fi
  return 0
}

# borrowed from redhats sysreport
function catiffile() {
  log $STATUS
  log "copy $1"
  if [ -d $1 ]; then
    /bin/cp -x --parents -R $1 $resdir 2>>$logfile
    echo -n $STATUS
    echo $(rc2str 0)
    return 1
  fi
  if [ -f $1 ]; then
    /bin/cp --parents $1 $resdir 2>>$logfile
    echo -n $STATUS
    echo $(rc2str 0)
    return 1
  fi

  return 0
}

function get_cluster_dlm_locks() {
	for service in $(cat /proc/cluster/services | grep "DLM Lock Space" | awk -F '\"' ' {print $2}'); do
		log "Getting locks for $service"
		echo $service > /proc/cluster/dlm_locks
		cat /proc/cluster/dlm_locks > $resdir/dlm_locks_$service
	done
}

while getopts vhV option ; do
	case "$option" in
	    V) # version
		echo "$0 Version '$Revision $'"
		exit 0
		;;
	    h) # help
		usage
		exit 0
		;;
		v) #verbose
		verbose=1
		;;
	    *)
		echo "Error wrong option."
		usage
		exit 1
		;;
	esac
done
shift $(($OPTIND - 1))

do_pre

log "starting com-sysinfo"

# get all information out of /proc/cluster
STATUS="Gathering slabinfo (/proc/slabinfo)"
catiffile "/proc/slabinfo"

STATUS="Gathering dmesg output"
catifexec "/bin/dmesg"

STATUS="Gathering procfs cluster information (/proc/cluster):"
catiffile "/proc/cluster"

STATUS="Gathering dlm_locks (/proc/cluster/dlm_locks)"
echo $STATUS
log $STATUS
get_cluster_dlm_locks

log "creating tar.gz file"
cd $mydir
tar czf $repfile *
cd -

do_post

echo "DONE."
echo "INFO: The sysreport can be found at $chrootdir/$mydir/$repfile"