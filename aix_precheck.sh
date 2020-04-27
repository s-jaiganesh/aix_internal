#!/usr/bin/ksh
## Check /mksysb presence ###
## ---------------------- ###
if [[ "`df -gt|grep -iEv 'export|-'|grep -i /mksysb>/dev/null 2>&1;echo $?`" -ne 0 && "`ls -ld /mksysb>/dev/null 2>&1;echo $?`" -eq 0 ]]
then
     mount /mksysb >/dev/null 2>&1
     mkdir -p /mksysb/ZZZ-pre-post-conf-ZZZ >/dev/null 2>&1
else
     mkdir -p /mksysb/ZZZ-pre-post-conf-ZZZ >/dev/null 2>&1
fi
## End of checking /mksysb presence ###

# Run bosboot and Set bootlist ##
### -------------------------- ###
LINECOUNT="`lslv -l hd5|grep -i hdisk|awk '{print $1}'|wc -l`"
if [[ $LINECOUNT -gt 1 ]]
then
    lslv -l hd5|grep -i hdisk|awk '{print $1}' >/tmp/hd5hdisklist
    for i in `cat /tmp/hd5hdisklist`
    do
       bosboot -ad /dev/$i
    done
    paste -s /tmp/hd5hdisklist >/tmp/hd5hdisklist1
    cat /tmp/hd5hdisklist1 |grep -v '^$'>/tmp/hd5hdisklist2
    exec 4</tmp/hd5hdisklist2
    while read -u4 A B
    do
        bootlist -m normal $A $B
    done
else
    lslv -l hd5|grep -i hdisk|awk '{print $1}' >/tmp/hd5hdisklist
    for i in `cat /tmp/hd5hdisklist`
    do
       bosboot -ad /dev/$i >/dev/null 2>&1
    done
    for i in `cat /tmp/hd5hdisklist`
    do
        bootlist -m normal  $i  >/dev/null 2>&1
    done
fi
rm /tmp/hd5hdisklist* >/dev/null 2>&1
## End of bosboot and bootlist section ###

mkdir /tmp/patchmount >/dev/null 2>&1

# Collect preconf data ##
### ------------------- ###
rm -rf /mksysb/ZZZ-pre-post-conf-ZZZ/* >/dev/null 2>&1

oslevel -sq |head -n1 >/mksysb/ZZZ-pre-post-conf-ZZZ/oslevel-s-out

echo "DF-K">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "============">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
df -k |grep -iv 'patchmount'>>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "\n">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf

echo "DISK total count">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "============">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
lsdev -C|grep -i disk|awk '{print $1}'>>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "\n">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf

echo "LSPV-total-count">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "============">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
lspv >>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "\n">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf

echo "FCS total count">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "============">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
lsdev -C|grep -i fcs|awk '{print $1}'>>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "\n">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf

echo "ENT total count">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "============">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
lsdev -C |grep -i ent>>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "\n">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf

echo "PATH total count">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "============">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
lspath >>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "\n">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf

echo "BOOTINFO-B">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "============">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
/usr/sbin/bootinfo -b>>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "\n">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf

echo "LSVG total count">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "============">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
lsvg>>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "\n">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf

echo "LSVG active count">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "============">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
lsvg -o>>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "\n">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf

echo "OPENLV">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "============">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
lsvg -o|lsvg -il|grep -i open>>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "\n">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf

echo "CLOSELV">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "============">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
lsvg -o|lsvg -il|egrep -i 'stale|close'>>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "\n">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf

echo "IFCONFIG DETAIL">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "============">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
ifconfig -a>>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "\n">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf

for i in `ifconfig -a |egrep 'en|lo'|awk '/:/ {print $(NF-1)}'|tr ":" " "`
do
   ifconfig $i >>/mksysb/ZZZ-pre-post-conf-ZZZ/IPb4
   echo "\n">>/mksysb/ZZZ-pre-post-conf-ZZZ/IPb4
done

echo "ROUTE DETAIL">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-route
netstat -nr>>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-route

lsdev -C |grep EtherChannel |awk '{print $1}'>ether-tmp
lsdev -C |grep EtherChannel |awk '{print $1}'>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-etherchanel-count
for i in `cat ether-tmp`
do
   lsattr -E -a backup_adapter -l $i >ether-tmp1
   cat ether-tmp1 |grep -i NONE >/dev/null
   if [[ $? -eq 0 ]]
   then
        echo "$i-etherchannel-NONESET">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-etherchnlconf
   else
        echo "$i-etherchannel-`entstat -d $i |grep -i 'Active channel' |awk -F \":\" '{print $2}'|sed 's|^[ \t]*||g'|awk '{print $1}'`">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-etherchnlconf
   fi
done
rm ether-tmp ether-tmp1 2>/dev/null

ifconfig -a |grep : |awk -F ":" '{print $1}'|egrep -v 'lo0|inet6|^$' >/mksysb/ZZZ-pre-post-conf-ZZZ/netcardb4
for ncb4 in `cat /mksysb/ZZZ-pre-post-conf-ZZZ/netcardb4`
do
   echo "$ncb4 `ifconfig $ncb4 |grep inet`" >>/mksysb/ZZZ-pre-post-conf-ZZZ/$ncb4-pre
done
lsdev -Cc tape |egrep -i 'tape|Medium Changer' |grep -i avail |wc -l >/mksysb/ZZZ-pre-post-conf-ZZZ/tapeavailcount
lsdev -C |grep -i iocp >/mksysb/ZZZ-pre-post-conf-ZZZ/iocpout

echo "\n" >>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "DATE">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "=====================">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
date |awk '{print $5}'>>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "\n" >>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf

echo "TZ">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "=====================">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo $TZ>>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "\n" >>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf

echo "Paging">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "=====================">>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
lsps -a >>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf
echo "\n" >>/mksysb/ZZZ-pre-post-conf-ZZZ/pre-conf


lparstat -i >/mksysb/ZZZ-pre-post-conf-ZZZ/prelparstat

showmount -a >/dev/null 2>&1
if [[ $? -eq 0 ]]
then 
     showmount -a |awk -F ":" '{print $1}' |awk '!a[$0]++'>/mksysb/ZZZ-pre-post-conf-ZZZ/NFSclientlist
fi
### End of preconfiguration collection section ###

