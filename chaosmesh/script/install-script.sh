#!/bin/sh


echo "Installing the NET_SCH_NETEM module"
curl -L -O https://kojipkgs.fedoraproject.org//packages/kernel/5.12.7/300.fc34/x86_64/kernel-modules-extra-5.12.7-300.fc34.x86_64.rpm
rpm2cpio kernel-modules-extra-5.12.7-300.fc34.x86_64.rpm | cpio -idmv
ls -l ./lib/modules/5.12.7-300.fc34.x86_64/kernel/net/sched/sch_netem.ko.xz
insmod ./lib/modules/5.12.7-300.fc34.x86_64/kernel/net/sched/sch_netem.ko.xz
lsmod | grep netem
