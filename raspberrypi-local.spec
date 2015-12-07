Name:           raspberrypi-local
Version:        1.0.4
Release:        1%{?dist}
Summary:        Raspberry Pi2 rc.local, config and scripts
License:        GPLv2+
URL:            http://www.agrez.net
Source0:	%{name}-%{version}.tar.gz
BuildArch:      noarch
Requires:       initscripts
Requires:	systemd


%description
Raspberry Pi2 rc.local, config and scripts

%prep
%setup -q

%build
echo "Nothing to do!"

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
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/modules-load.d
%{__install} -p -m0644 modules-load-snd-bcm2835.conf\
 $RPM_BUILD_ROOT%{_sysconfdir}/modules-load.d/99-snd-bcm2835.conf
%{__install} -p -m0644 modules-load-bcm2708-wdog.conf\
 $RPM_BUILD_ROOT%{_sysconfdir}/modules-load.d/99-bcm2708-wdog.conf

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
%{__install} -p -m0755 rpi-freq\
 $RPM_BUILD_ROOT%{_sbindir}/rpi-freq
%{__install} -p -m0755 rpi-mem\
 $RPM_BUILD_ROOT%{_sbindir}/rpi-mem
%{__install} -p -m0755 rpi-temp\
 $RPM_BUILD_ROOT%{_sbindir}/rpi-temp
%{__install} -p -m0755 rpi-volts\
 $RPM_BUILD_ROOT%{_sbindir}/rpi-volts
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
%{__install} -p -m0644 config.txt.hdmi_nooverscan\
 $RPM_BUILD_ROOT/boot/config.txt.hdmi_nooverscan
%{__install} -p -m0644 config.txt.hdmi_overscan\
 $RPM_BUILD_ROOT/boot/config.txt.hdmi_overscan
%{__install} -p -m0644 config.txt.ntsc_japan\
 $RPM_BUILD_ROOT/boot/config.txt.ntsc_japan
%{__install} -p -m0644 config.txt.ntsc_northamerica\
 $RPM_BUILD_ROOT/boot/config.txt.ntsc_northamerica
%{__install} -p -m0644 config.txt.pal\
 $RPM_BUILD_ROOT/boot/config.txt.pal
%{__install} -p -m0644 config.txt.pal_brazil\
 $RPM_BUILD_ROOT/boot/config.txt.pal_brazil

%files
%doc COPYING
%config(noreplace) %attr(0755,-,-) %{_sysconfdir}/rc.d/rc.local
%config(noreplace) %attr(0755,-,-) %{_sysconfdir}/dracut.conf.d/*.conf
%config(noreplace) %attr(0644,-,-) %{_sysconfdir}/modules-load.d/*.conf
%attr(0755,-,-) %{_sbindir}/rpi-*
%config(noreplace) %attr(0644,-,-) /boot/cmdline.txt
%config(noreplace) %attr(0644,-,-) /boot/config.txt
%config %attr(0644,-,-) /boot/config.txt.*
%config(noreplace) %attr(0644,-,-) /usr/lib/sysctl.d/*.conf
%config(noreplace) %attr(0644,-,-) /usr/lib/udev/rules.d/*.rules

%changelog
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
