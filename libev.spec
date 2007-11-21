%bcond_without	static_libs	# don't build static library
#
Summary:	libev - an event notification library
Summary(pl.UTF-8):	libev - biblioteka powiadamiająca o zdarzeniach
Name:		libev
Version:	1.3e
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://dist.schmorp.de/libev/%{name}-%{version}.tar.gz
# Source0-md5:	7f54d064bf0769a63efd19eace23a8b1
URL:		http://software.schmorp.de/pkg/libev
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libev API provides a mechanism to execute a callback function when
a specific event occurs on a file descriptor or after a timeout has
been reached. It is meant to replace the asynchronous event loop found
in event-driven network servers.

%description -l pl.UTF-8
API libev dostarcza mechanizm do wykonywania funkcji callback, kiedy
nastąpiło określone zdarzenie w deskryptorze pliku lub po
określonym czasie. Ma to na celu zastąpienie asynchronicznych pętli
w sterowanych zdarzeniami usługach sieciowych.

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
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libev-*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libev.so
%{_libdir}/libev.la
%{_includedir}/ev*.h
%{_mandir}/man3/ev*.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libev.a
%endif
