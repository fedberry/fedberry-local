Name:       fedberry-local
Version:    29
Release:    2%{?dist}
Summary:    FedBerry rc.local, configs and scripts for the Raspberry Pi
License:    GPLv2+
URL:        https://github.com/%{name}
Source0:    %{url}/raw/master/cmdline.txt
Source1:    %{url}/raw/master/config.txt
Source2:    %{url}/raw/master/COPYING
Source3:    %{url}/raw/master/dracut-rpi.conf
Source4:    %{url}/raw/master/rc.local
Source8:    %{url}/raw/master/sysctl-vm-min-free-kbytes.conf
Source9:    %{url}/raw/master/sysctl-vm-swappiness.conf
Source10:   %{url}/raw/master/sysctl-quiet-printk.conf
Source11:   %{url}/raw/master/pulseaudio-raspberrypi.conf
Source12:   %{url}/raw/master/pulseaudio-rpi.rules
Source13:   %{url}/raw/master/fedberry-xfce-defaults.tar.xz
Source14:   %{url}/raw/master/default-gtk2.conf
Source15:   %{url}/raw/master/default-gtk3.conf
Source16:   %{url}/raw/master/xorg-fbturbo.conf
Source17:   %{url}/raw/master/disable-pulseaudio.desktop
Source18:   %{url}/raw/master/chromium-preferences
Source19:   %{url}/raw/master/chromium-flags
BuildArch:      noarch
BuildRequires:  systemd

Requires:   initscripts
Requires:   systemd

%description
%{summary}.


%package xfce-config
Summary: Default Fedberry configuration files for Xfce

%description xfce-config
This package contains default Fedberry configuration files for Xfce.


%package gtk-config
Summary: Default Fedberry configuration files for GTK+2/3
Requires: breeze-gtk
Requires: breeze-icon-theme
Requires: breeze-cursor-theme

%description gtk-config
This package contains default Fedberry configuration files for GTK+2/3.


%package xorg-config
Summary: Default Fedberry configuration files for xorg
Requires: xorg-x11-drv-fbturbo

%description xorg-config
This package contains default Fedberry configuration files for xorg.


%package chromium
Summary: Default Fedberry configuration files for chromium
Requires: chromium
Requires: raspberrypi-vc-libs >= 20180704-1.409dfcd

%description chromium
This package contains default Fedberry configuration files for chromium.


%prep
%setup -c -T
cp -a %{SOURCE2} .


%build


%install
##
## rc.local
##
mkdir -p %{buildroot}/%{_sysconfdir}/rc.d
%{__install} -p -m0755 %{SOURCE4} %{buildroot}/%{_sysconfdir}/rc.d/

##
## dracut.conf.d
##
mkdir -p %{buildroot}/%{_sysconfdir}/dracut.conf.d
%{__install} -p -m0755 %{SOURCE3} \
%{buildroot}/%{_sysconfdir}/dracut.conf.d/rpi.conf

##
## /usr/lib/sysctl.d
##
mkdir -p %{buildroot}/%{_libdir}/sysctl.d
%{__install} -p -m0644 %{SOURCE8} \
%{buildroot}/%{_libdir}/sysctl.d/99-vm-min-free-kbytes.conf
%{__install} -p -m0644 %{SOURCE9} \
%{buildroot}/%{_libdir}/sysctl.d/99-vm-swappiness.conf
%{__install} -p -m0644 %{SOURCE10} \
%{buildroot}/%{_libdir}/sysctl.d/20-quiet-printk.conf

##
## /usr/lib/udev/rules.d
##
mkdir -p %{buildroot}%{_udevrulesdir}
%{__install} -p -m0644 %{SOURCE12} \
%{buildroot}%{_udevrulesdir}/91-pulseaudio-rpi.rules


##
## /boot config
##
mkdir -p %{buildroot}/boot
%{__install} -p -m0644 %{SOURCE0} %{buildroot}/boot/
%{__install} -p -m0644 %{SOURCE1} %{buildroot}/boot/

##
## pulseaudio :-/
##
mkdir -p %{buildroot}/%{_datadir}/pulseaudio/alsa-mixer/profile-sets
%{__install} -p -m0644 %{SOURCE11} \
%{buildroot}/%{_datadir}/pulseaudio/alsa-mixer/profile-sets/raspberrypi.conf
mkdir -p %{buildroot}/%{_sysconfdir}/skel/.config/autostart
%{__install} -p -m0644 %{SOURCE17} \
%{buildroot}/%{_sysconfdir}/skel/.config/autostart/pulseaudio.desktop

##
## /etc/skel files
##
mkdir -p %{buildroot}/%{_sysconfdir}/skel/.config
tar xvfJ %{SOURCE13} -C %{buildroot}/%{_sysconfdir}/skel/.config

##
## GTK+ configuration files
##
mkdir -p %{buildroot}/%{_sysconfdir}/gtk-2.0
%{__install} -p -m0755 %{SOURCE14} \
%{buildroot}/%{_sysconfdir}/gtk-2.0/gtkrc

mkdir -p %{buildroot}/%{_sysconfdir}/gtk-3.0
%{__install} -p -m0755 %{SOURCE15} \
%{buildroot}/%{_sysconfdir}/gtk-3.0/settings.ini

##
## xorg.conf.d files
##
mkdir -p %{buildroot}/%{_datadir}/X11/xorg.conf.d
%{__install} -p -m0755 %{SOURCE16} \
%{buildroot}/%{_datadir}/X11/xorg.conf.d/20-fbturbo.conf

##
## chromium files
##
mkdir -p %{buildroot}/%{_sysconfdir}/chromium
%{__install} -p -m0755 %{SOURCE18} \
%{buildroot}/%{_sysconfdir}/chromium/master_preferences
%{__install} -p -m0755 %{SOURCE19} \
%{buildroot}/%{_sysconfdir}/chromium/default


%post
# Older upgraded installs that haven't installed the new xorg-conf package
if [ -f %{_sysconfdir}/X11/xorg.conf.d/20-fbturbo.conf ] && [ ! -f %{_datadir}/X11/xorg.conf.d/20-fbturbo.conf ]; then
    cp -f %{_sysconfdir}/X11/xorg.conf.d/20-fbturbo.conf %{_datadir}/X11/xorg.conf.d/
fi


%files xfce-config
%attr(0755,-,-) %{_sysconfdir}/skel/.config/xfce4/xfconf/xfce-perchannel-xml/*.xml


%files gtk-config
%config %{_sysconfdir}/gtk-2.0/gtkrc
%config %{_sysconfdir}/gtk-3.0/settings.ini


%files xorg-config
%config %{_datadir}/X11/xorg.conf.d/20-fbturbo.conf


%files chromium
%config %{_sysconfdir}/chromium/master_preferences
%config %{_sysconfdir}/chromium/default


%files
%doc COPYING
%{_sysconfdir}/skel/.config/autostart/pulseaudio.desktop
%config(noreplace) %{_sysconfdir}/rc.d/rc.local
%config(noreplace) %{_sysconfdir}/dracut.conf.d/*.conf
%config(noreplace) /boot/cmdline.txt
%config(noreplace) /boot/config.txt
%config(noreplace) %{_libdir}/sysctl.d/*.conf
%{_udevrulesdir}/*.rules
%{_datadir}/pulseaudio/alsa-mixer/profile-sets/*.conf


%changelog
* Fri Oct 12 2018 Vaughan <devel at agrez dot net> - 29-2
- Drop rpi-snd-bcm2835-* scripts (fedberry-config now support this)
- Refactor source file urls

* Thu Oct 11 2018 Vaughan <devel at agrez dot net> - 29-1
- Bump release for Fedberry 29
- Add enable_uart=1 comment stub to config.txt

* Wed Jul 04 2018 Vaughan <devel at agrez dot net> - 28-1
- Bump release for Fedberry 28
- Dropped 10-vchiq-permissions.rules (moved to raspberrypi-vc-libs)
- Add chromium defaults & master_preferences for Fedberry
- Misc spec cleanups / refactoring

* Tue Apr 03 2018 Vaughan <devel at agrez dot net> - 27-6
- Add package for default GTK+2/3 settings
- Add package for xorg.conf.d config (fbturbo.conf)
- Update default xfce settings
- Disable autostart of pulseaudio (for the moment)

* Fri Mar 30 2018 Vaughan <devel at agrez dot net> - 27-5
- Add pulseaudio profile and udev rule
- Add package for xfce default settings

* Sun Mar 25 2018 Vaughan <devel at agrez dot net> - 27-4
- Add fsck.repair=yes to cmdline.txt

* Thu Dec 14 2017 Vaughan <devel at agrez dot net> - 27-3
- brcmfmac is still too noisy (add Source 10)

* Sun Dec 10 2017 Vaughan <devel at agrez dot net> - 27-2
- Drop cgroup_disable=memory from cmdline.txt

* Thu Nov 23 2017 Vaughan <devel at agrez dot net> - 27-1
- Bump release for Fedberry 27

* Mon Aug 07 2017 Vaughan <devel at agrez dot net> - 26-1
- Bump release for Fedberry 26
- Clean up spec
- Update config.txt defaults

* Mon Apr 17 2017 Vaughan <devel at agrez dot net> - 25-3
- Remove plymouth options from default cmdline.txt

* Mon Apr 10 2017 Vaughan <devel at agrez dot net> - 25-2
- Update cmdline.txt & config.txt files

* Mon Jan 02 2017 Vaughan <devel at agrez dot net> - 25-1
- Bump release

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

* Fri Mar 11 2016 Vaughan <devel at agrez dot net> - 23.1-1
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
