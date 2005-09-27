Name:		keepalived
Summary:	HA monitor built upon LVS, VRRP and services poller
Version:	1.1.11
Release:	0.8
License:	GPL v2
Group:		Applications/System
Source0:	http://www.keepalived.org/software/%{name}-%{version}.tar.gz
# Source0-md5:	bd028acb16f47d2286fb9a00d62b0c79
#Source1:	%{name}.init
URL:		http://www.keepalived.org/
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	popt-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The main goal of the keepalived project is to add a strong & robust
keepalive facility to the Linux Virtual Server project. This project
is written in C with multilayer TCP/IP stack checks. Keepalived
implements a framework based on three family checks : Layer3, Layer4 &
Layer5. This framework gives the daemon the ability of checking a LVS
server pool states. When one of the server of the LVS server pool is
down, keepalived informs the linux kernel via a setsockopt call to
remove this server entrie from the LVS topology. In addition
keepalived implements a VRRPv2 stack to handle director failover. So
in short keepalived is a userspace daemon for LVS cluster nodes
healthchecks and LVS directors failover.

%prep
%setup -q
sed -i 's/_KRNL_2_2_/_KRNL_2_6_/' configure

%build
%configure \
	CFLAGS="-D__KERNGLUE__ -I%{_kernelsrcdir}/include \
	-include %{_kernelsrcdir}/include/asm-generic/errno.h"
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/keepalived,/etc/rc.d/init.d}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,5,8}}

install keepalived/etc/keepalived/keepalived.conf $RPM_BUILD_ROOT%{_sysconfdir}/keepalived
install keepalived/etc/init.d/keepalived.init $RPM_BUILD_ROOT/etc/rc.d/init.d/keepalived
install bin/genhash $RPM_BUILD_ROOT%{_bindir}
install bin/keepalived $RPM_BUILD_ROOT%{_sbindir}
install doc/man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1
install doc/man/man5/* $RPM_BUILD_ROOT%{_mandir}/man5
install doc/man/man8/* $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add keepalived

%preun
/sbin/chkconfig --del keepalived

%files
%defattr(644,root,root,755)
%doc doc/samples doc/keepalived*
%doc AUTHOR ChangeLog CONTRIBUTORS README TODO
%attr(755,root,root) %{_bindir}/genhash
%attr(755,root,root) %{_sbindir}/keepalived
%attr(754,root,root) /etc/rc.d/init.d/keepalived
%{_sysconfdir}/keepalived
%{_mandir}/man?/*
