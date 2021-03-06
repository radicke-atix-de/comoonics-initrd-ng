#****h* comoonics-bootimage/create-gfs-initrd-lib.sh
#  NAME
#    create-gfs-initrd-lib.sh
#    $id$
#  DESCRIPTION
#    Library for the creating of initrds for sharedroot
#*******
#
# Copyright (c) 2001 ATIX GmbH, 2007 ATIX AG.
# Einsteinstrasse 10, 85716 Unterschleissheim, Germany
# All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

#

#****f* create-gfs-initrd-lib.sh/perlcc_file
#  NAME
#    perlcc_file
#  SYNOPSIS
#    function perlcc_file(perlfile, destfile) {
#  DESCRIPTION
#    Compiles the perlfile to a binary in destfile
#  IDEAS
#    To be used if special perlfiles are needed without puting all
#    perl things into the initrd.
#  SOURCE
#
function perlcc_file() {
  local filename=$1
  local destfile=$2
  [ -z "$destfile" ] && destfile=$filename
  echo "compiling(perlcc) $filename to ${destfile}..." >&2
  olddir=pwd
  cd $(dirname $destfile)
  perlcc $filename && mv a.out $destfile
}
#************ perlcc_file

#****f* create-gfs-initrd-lib.sh/make_initrd
#  NAME
#    make_initrd
#  SYNOPSIS
#    function make_initrd() {
#  DESCRIPTION
#    Creates a new memory filesystem initrd with the given size
#  IDEAS
#  SOURCE
#
function make_initrd() {
  local filename=$1
  local size=$2
  dd if=/dev/zero of=$filename bs=1k count=$size > /dev/null 2>&1 && \
  mkfs.ext2 -F -m 0 -i 2000 $filename > /dev/null 2>&1
}
#************ make_initrd

#****f* create-gfs-initrd-lib.sh/mount_initrd
#  NAME
#    mount_initrd
#  SYNOPSIS
#    function mount_initrd() {
#  DESCRIPTION
#    Mounts the given unpacked filesystem to the given directory
#  IDEAS
#  SOURCE
#
function mount_initrd() {
  local filename=$1
  local mountpoint=$2
  mount -o loop -t ext2 $filename $mountpoint > /dev/null 2>&1
}

#
# Unmounts the given loopback memory filesystem and zips it to the given file
#************ mount_initrd
#****f* create-gfs-initrd-lib.sh/umount_and_zip_initrd
#  NAME
#    umount_and_zip_initrd
#  SYNOPSIS
#    function umount_and_zip_initrd() {
#  MODIFICATION HISTORY
#  IDEAS
#  SOURCE
#
function umount_and_zip_initrd() {
  local mountpoint=$1
  local filename=$2
  local force=$3
  local opts=""
  local LODEV=$(mount | grep "^$mountpoint" | tail -1 | cut -f6 -d" " | cut -d"=" -f2)
  [ -z "$compression_cmd" ] && compression_cmd="gzip"
  [ -z "$compression_opts" ] && compression_opts="-c -9"
  LODEV=$(echo ${LODEV/%\)/})
  [ -n "$force" ] && [ $force -gt 0 ] && opts="-f"
  (umount $mountpoint && \
   losetup -d $LODEV && \
   mv $filename ${filename}.tmp && \
   $compression_cmd $compression_opts $opts ${filename}.tmp > $filename && rm ${filename}.tmp) || (fuser -mv "$mountpoint" && exit 1)
}
#****** umount_and_zip_initrd