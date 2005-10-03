# TODO: why it uses 2.6.x kernel header directly instead of llh?
Summary:	HA monitor built upon LVS, VRRP and services poller
Summary(pl):	Monitor HA zbudowany w oparciu o LVS, VRRP i narzêdzie do sprawdzania us³ug
Name:		keepalived
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
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The main goal of the keepalived project is to add a strong & robust
keepalive facility to the Linux Virtual Server project. This project
is written in C with multilayer TCP/IP stack checks. Keepalived
implements a framework based on three family checks: Layer3, Layer4 &
Layer5. This framework gives the daemon the ability of checking a LVS
server pool states. When one of the server of the LVS server pool is
down, keepalived informs the Linux kernel via a setsockopt call to
remove this server entry from the LVS topology. In addition
keepalived implements a VRRPv2 stack to handle director failover. So
in short keepalived is a userspace daemon for LVS cluster nodes
healthchecks and LVS directors failover.

%description -l pl
G³ównym celem projektu keepalived jest dodanie potê¿nego udogodnienia
keepalive do projektu Linux Virtual Server. Ten projekt jest napisany
w C z wielowarstwowym sprawdzaniem stosu TCP/IP. keepalived
implementuje szkielet oparty na sprawdzaniu trzech rodzin: warstwy 3,
warstwy 4 i warstwy 5. Ten szkielet daje demonowi mo¿liwo¶æ
sprawdzania stanów puli serwerów LVS. Kiedy jeden serwer z puli
serwerów LVS przestaje dzia³aæ, keepalived informuje o tym j±dro
Linuksa poprzez wywo³anie setsockopt w celu usuniêcia wpisu o serwerze
z topologii LVS. Poza tym keepalived implementuje stos VRRPv2 do
obs³ugi przejmowania zadañ (failover) samego urz±dzenia zarz±dzaj±cego
(director). Czyli w skrócie keepalived to dzia³aj±cy w przestrzeni
u¿ytkownika demon do sprawdzania stanu wêz³ów klastra LVS oraz
przejmowania zadañ urz±dzenia zarz±dzaj±cego.

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
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del keepalived
fi

%files
%defattr(644,root,root,755)
%doc doc/samples doc/keepalived*
%doc AUTHOR ChangeLog CONTRIBUTORS README TODO
%attr(755,root,root) %{_bindir}/genhash
%attr(755,root,root) %{_sbindir}/keepalived
%attr(754,root,root) /etc/rc.d/init.d/keepalived
%{_sysconfdir}/keepalived
%{_mandir}/man?/*
