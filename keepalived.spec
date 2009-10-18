#
# TODO:
# - why it uses 2.6.x kernel header directly instead of llh?
#   and more - it looks for /usr/src/linux/net/core/link_watch.c 
#   (kernel-source) for LVS features - check build/kernel dependency.
#   [-D_WITH_LINKWATCH_ allows force this feature without file existence]
# - genhash to separate package
#
Summary:	HA monitor built upon LVS, VRRP and services poller
Summary(pl.UTF-8):	Monitor HA zbudowany w oparciu o LVS, VRRP i narzędzie do sprawdzania usług
Name:		keepalived
Version:	1.1.19
Release:	0.2
License:	GPL v2
Group:		Applications/System
Source0:	http://www.keepalived.org/software/%{name}-%{version}.tar.gz
# Source0-md5:	a35b8d9d462810f7650d292bd7457523
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-config.patch
URL:		http://www.keepalived.org/
#BuildRequires:	kernel-source >= 2.6.0
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	popt-devel
BuildRequires:	rpmbuild(macros) >= 1.268
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

%description -l pl.UTF-8
Głównym celem projektu keepalived jest dodanie potężnego udogodnienia
keepalive do projektu Linux Virtual Server. Ten projekt jest napisany
w C z wielowarstwowym sprawdzaniem stosu TCP/IP. keepalived
implementuje szkielet oparty na sprawdzaniu trzech rodzin: warstwy 3,
warstwy 4 i warstwy 5. Ten szkielet daje demonowi możliwość
sprawdzania stanów puli serwerów LVS. Kiedy jeden serwer z puli
serwerów LVS przestaje działać, keepalived informuje o tym jądro
Linuksa poprzez wywołanie setsockopt w celu usunięcia wpisu o serwerze
z topologii LVS. Poza tym keepalived implementuje stos VRRPv2 do
obsługi przejmowania zadań (failover) samego urządzenia zarządzającego
(director). Czyli w skrócie keepalived to działający w przestrzeni
użytkownika demon do sprawdzania stanu węzłów klastra LVS oraz
przejmowania zadań urządzenia zarządzającego.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	CFLAGS="%{rpmcflags} -include %{_includedir}/linux/errno.h -D_WITH_LINKWATCH_"
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

# Cleanups:
rm -rf $RPM_BUILD_ROOT/etc/keepalived/samples
rm -f $RPM_BUILD_ROOT/etc/init.d/keepalived

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add keepalived
%service keepalived restart

%preun
if [ "$1" = "0" ]; then
	%service keepalived stop
	/sbin/chkconfig --del keepalived
fi

%files
%defattr(644,root,root,755)
%doc AUTHOR ChangeLog CONTRIBUTORS README TODO doc/samples doc/keepalived*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/keepalived/keepalived.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(755,root,root) %{_bindir}/genhash
%attr(755,root,root) %{_sbindir}/keepalived
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%dir %{_sysconfdir}/keepalived
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*
