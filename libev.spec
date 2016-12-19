#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	libev - an event notification library
Summary(pl.UTF-8):	libev - biblioteka powiadamiająca o zdarzeniach
Name:		libev
Version:	4.23
Release:	1
License:	BSD or GPL v2+
Group:		Libraries
Source0:	http://dist.schmorp.de/libev/%{name}-%{version}.tar.gz
# Source0-md5:	f1dbf786ead8307e0d4f5f68f2f8526c
URL:		http://software.schmorp.de/pkg/libev.html
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
# inotify interface
BuildRequires:	glibc-devel >= 6:2.4
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libev API provides a mechanism to execute a callback function when
a specific event occurs on a file descriptor or after a timeout has
been reached. It is meant to replace the asynchronous event loop found
in event-driven network servers.

%description -l pl.UTF-8
API libev dostarcza mechanizm do wykonywania funkcji callback, kiedy
nastąpiło określone zdarzenie w deskryptorze pliku lub po określonym
czasie. Ma to na celu zastąpienie asynchronicznych pętli w sterowanych
zdarzeniami usługach sieciowych.

%package devel
Summary:	Header files for libev library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libev
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libev library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libev.

%package static
Summary:	Static libev library
Summary(pl.UTF-8):	Statyczna biblioteka libev
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libev library.

%description static -l pl.UTF-8
Statyczna biblioteka libev.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}

# override -O3 which overrides our optflags in configure
%{__make} \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# avoid conflict with libevent
install -d $RPM_BUILD_ROOT%{_includedir}/libev
mv $RPM_BUILD_ROOT%{_includedir}/event.h $RPM_BUILD_ROOT%{_includedir}/libev

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Changes LICENSE README TODO
%attr(755,root,root) %{_libdir}/libev.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libev.so.4

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libev.so
%{_libdir}/libev.la
%{_includedir}/ev.h
%{_includedir}/ev++.h
%dir %{_includedir}/libev
%{_includedir}/libev/event.h
%{_mandir}/man3/ev.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libev.a
%endif
