Name:       fedberry-local
Version:    24
Release:    5%{?dist}
Summary:    FedBerry rc.local, config and scripts for the Raspberry Pi 2/3 B
License:    GPLv2+
URL:        https://github.com/fedberry
Source0:    https://github.com/fedberry/%{name}/blob/master/cmdline.txt
Source1:    https://github.com/fedberry/%{name}/blob/master/config.txt
Source2:    https://github.com/fedberry/%{name}/blob/master/COPYING
Source3:    https://github.com/fedberry/%{name}/blob/master/dracut-rpi.conf
Source4:    https://github.com/fedberry/%{name}/blob/master/rc.local
Source5:    https://github.com/fedberry/%{name}/blob/master/rpi-snd-bcm2835-route-analogue
Source6:    https://github.com/fedberry/%{name}/blob/master/rpi-snd-bcm2835-route-auto
Source7:    https://github.com/fedberry/%{name}/blob/master/rpi-snd-bcm2835-route-hdmi
Source8:    https://github.com/fedberry/%{name}/blob/master/sysctl-vm_min_free_kbytes.conf
Source9:    https://github.com/fedberry/%{name}/blob/master/udev-vchiq-permissions.rules
BuildArch:  noarch
Requires:   initscripts
Requires:   systemd
Obsoletes:  raspberrypi-local
Conflicts:  raspberrypi-local


%description
%{summary}.


%prep
%setup -c -T
cp -a %{sources} .


%build


%install
rm -rf $RPM_BUILD_ROOT

##
## rc.local
##
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rc.d
%{__install} -p -m0755 rc.local $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc.local

##
## dracut.conf.d
##
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/dracut.conf.d
%{__install} -p -m0755 dracut-rpi.conf $RPM_BUILD_ROOT%{_sysconfdir}/dracut.conf.d/rpi.conf
 
##
## modules-load.d: Modules that wouldn't otherwise auto-load
##
#mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/modules-load.d
#%{__install} -p -m0644 modules-load-snd-bcm2835.conf\
# $RPM_BUILD_ROOT%{_sysconfdir}/modules-load.d/99-snd-bcm2835.conf

##
## /usr/lib/sysctl.d
##
mkdir -p $RPM_BUILD_ROOT/usr/lib/sysctl.d/
%{__install} -p -m0644 sysctl-vm_min_free_kbytes.conf\
 $RPM_BUILD_ROOT/usr/lib/sysctl.d/99-vm_min_free_kbytes.conf

##
## /usr/lib/udev/rules.d
##
mkdir -p $RPM_BUILD_ROOT/usr/lib/udev/rules.d
%{__install} -p -m0644 udev-vchiq-permissions.rules\
 $RPM_BUILD_ROOT/usr/lib/udev/rules.d/10-vchiq-permissions.rules

##
## Utility scripts
##
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
%{__install} -p -m0755 rpi-snd-bcm2835-route-auto\
 $RPM_BUILD_ROOT%{_sbindir}/rpi-snd-bcm2835-route-auto
%{__install} -p -m0755 rpi-snd-bcm2835-route-analogue\
 $RPM_BUILD_ROOT%{_sbindir}/rpi-snd-bcm2835-route-analogue
%{__install} -p -m0755 rpi-snd-bcm2835-route-hdmi\
 $RPM_BUILD_ROOT%{_sbindir}/rpi-snd-bcm2835-route-hdmi
 
##
## /boot config
##
mkdir -p $RPM_BUILD_ROOT/boot
%{__install} -p -m0644 cmdline.txt\
 $RPM_BUILD_ROOT/boot/cmdline.txt
%{__install} -p -m0644 config.txt\
 $RPM_BUILD_ROOT/boot/config.txt


%files
%doc COPYING
%config(noreplace) %attr(0755,-,-) %{_sysconfdir}/rc.d/rc.local
%config(noreplace) %attr(0755,-,-) %{_sysconfdir}/dracut.conf.d/*.conf
#%config(noreplace) %attr(0644,-,-) %{_sysconfdir}/modules-load.d/*.conf
%attr(0755,-,-) %{_sbindir}/*
%config(noreplace) %attr(0644,-,-) /boot/cmdline.txt
%config(noreplace) %attr(0644,-,-) /boot/config.txt
%config(noreplace) %attr(0644,-,-) /usr/lib/sysctl.d/*.conf
%config(noreplace) %attr(0644,-,-) /usr/lib/udev/rules.d/*.rules


%changelog
* Sun Dec 18 2016 Vaughan <devel at agrez dot net> - 24-5
- Add cgroup_disable=memory to cmdline.txt
- Update %%prep section

* Fri Sep 16 2016 Vaughan <devel at agrez dot net> - 24-4
- Update cmdline.txt
- Drop rpi-[freq mem temp volts] scripts

* Sun Aug 21 2016 Vaughan <devel at agrez dot net> - 24-3
- Set console_loglevel to print KERN_WARNING (2) or more severe
  messages (rc.local)

* Tue Jun 21 2016 Vaughan <devel at agrez dot net> - 24-2
- Update cmdline.txt

* Thu Jun 16 2016 Vaughan <devel at agrez dot net> - 24-1
- Prep for FedBerry 24 release
- Split out all files

* Fri Mar 12 2016 Vaughan <devel at agrez dot net> - 23.1-1
- Drop modules-load-snd-bcm2835.conf (its a DT parameter now)
- Enable DT parameter audio=on by default
- Clean up / refactor config.txt options
- Drop all regional specific config.txt examples.
- cmdline.txt option elevator=deadline now default for all releases
- Bump release
  
* Thu Feb 04 2016 Vaughan <devel at agrez dot net> - 23-1
- Rename package to fedberry-local
- Version now follows FedBerry distro release version
- Compress source file using xz

* Tue Jan 26 2016 Vaughan <devel at agrez dot net> - 1.0.4-2
- bcm2708-wdog module has been removed from kernel-4.3.y series
- Update URL & Source URL

* Sun Nov 29 2015 Vaughan <devel at agrez dot net> - 1.0.4-1
- config.txt modifications:
    Add raspberry camera module switches
    Disable overscan by default

* Thu Aug 20 2015 Vaughan <devel at agrez dot net> - 1.0.3-1
- Add 'quiet' boot option to cmdline.txt
- Set initial default gpu_mem=32 (config.txt)
  refer to: https://github.com/raspberrypi/firmware/issues/428

* Wed Aug 19 2015 Vaughan <devel at agrez dot net> - 1.0.2-1
- Disable dracut creating kernel rescue images (rpi.conf) 

* Sun Jun 14 2015 Vaughan <devel at agrez dot net> - 1.0.1-1
- Disable enabling of ondemand govenor in rc.local (its now default in my kernel)
- Remove requires for sc-local

* Thu May 21 2015 Clive Messer <clive.messer@squeezecommunity.org> - 1.0-15
- Disable wlan0 powersave from rc.local.

* Sat May 16 2015 Clive Messer <clive.messer@squeezecommunity.org> - 1.0-14
- Re-package for F22.

* Wed Apr 01 2015 Clive Messer <clive.messer@squeezecommunity.org> - 1.0-13
- Move the sources into a tar file.

* Tue Mar 31 2015 Clive Messer <clive.messer@squeezecommunity.org> - 1.0-12
- Add 10-vchiq-permissions.rules.

* Tue Mar 31 2015 Clive Messer <clive.messer@squeezecommunity.org> - 1.0-11
- Add bcm2835 audio routing scripts.

* Fri Mar 27 2015 Clive Messer <clive.messer@squeezecommunity.org> - 1.0-10
- Add comment to raspberrypi-local-sysctl-vm_min_free_kbytes.conf

* Fri Mar 27 2015 Clive Messer <clive.messer@squeezecommunity.org> - 1.0-9
- Requires: sysctl-ssd-vm-conf

* Sat Feb 28 2015 Clive Messer <clive.messer@squeezecommunity.org> - 1.0-8
- Move sysctl scripts to /usr/lib/sysctl.d. (Vendor dir.)
- Add vm_swappiness.conf and vm_vfs_cache_pressure.conf.
- Add slub_debug=FP to /boot/cmdline.txt.
  Trying to debug an oops...

* Sat Feb 28 2015 Clive Messer <clive.messer@squeezecommunity.org> - 1.0-7
- Add COPYING. (GPLv2 LICENSE)
- Add sysctl.d vm_min_free_kbytes.conf.

* Mon Feb 23 2015 Clive Messer <clive.messer@squeezecommunity.org> - 1.0-6
- Update config.txt.
  Add Pi2 overclock settings.

* Sun Feb 22 2015 Clive Messer <clive.messer@squeezecommunity.org> - 1.0-5
- Add "default" network config.
  /etc/sysconfig/network-scripts/{ifcfg-eth0,ifcfg-wlan0,keys-wlan0}

* Mon Feb 16 2015 Clive Messer <clive.messer@squeezecommunity.org> - 1.0-4
- Update 8192cu.conf.

* Mon Feb 16 2015 Clive Messer <clive.messer@squeezecommunity.org> - 1.0-3
- Add 8192cu.conf to disable power save on RTL81{88,92} wi-fi dongles.

* Wed Feb 11 2015 Clive Messer <clive.messer@squeezecommunity.org> - 1.0-1
- Initial build
