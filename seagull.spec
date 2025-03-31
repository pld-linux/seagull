#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries
#
Summary:	SQLite helper library
Summary(pl.UTF-8):	Biblioteka pomocnicza SQLite
Name:		seagull
Version:	0.3.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://downloads.sourceforge.net/pidgin/%{name}-%{version}.tar.xz
# Source0-md5:	0c221e08352f305a9920d8636e05b5dd
URL:		https://keep.imfreedom.org/seagull/seagull/
# C17
BuildRequires:	gcc >= 6:7
BuildRequires:	gi-docgen >= 2024.1
BuildRequires:	glib2-devel >= 1:2.76.0
BuildRequires:	meson >= 1.1.10
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	sqlite3-devel >= 3.27.0
Requires:	glib2 >= 1:2.76.0
Requires:	sqlite3 >= 3.27.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library is meant to make the developer experience when working
SQLite3 in a GObject based library easier while not creating an entire
ORM (Object-relational mapping).

This library includes things a schema migration manager as well as
helpers for using prepared statements with named parameters.

%description -l pl.UTF-8
Ta biblioteka ma ułatwiać pracę programistom przy pracy z SQLite3 w
kodzie opartym na bibliotece GObject poprzez nietworzenie całkowitego
ORM (odwzorowania obiektowo-relacyjnego).

Ta biblioteka zawiera elementy takie jak zarządcę migracji schematów,
a także funkcje pomocnicze do używania przygotowanych instrukcji z
nazwanymi parametrami.

%package devel
Summary:	Header files for Seagull library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Seagull
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.76.0
Requires:	sqlite3-devel >= 3.27.0

%description devel
Header files for Seagull library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Seagull.

%package static
Summary:	Static Seagull library
Summary(pl.UTF-8):	Statyczna biblioteka Seagull
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Seagull library.

%description static -l pl.UTF-8
Statyczna biblioteka Seagull.

%package apidocs
Summary:	API documentation for Seagull library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Seagull
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Seagull library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Seagull.

%prep
%setup -q

%build
%meson

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/seagull $RPM_BUILD_ROOT%{_gidocdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.md
%attr(755,root,root) %{_libdir}/libseagull.so.*.*.*
%ghost %{_libdir}/libseagull.so.0
%{_libdir}/girepository-1.0/Seagull-1.0.typelib

%files devel
%defattr(644,root,root,755)
%{_libdir}/libseagull.so
%{_includedir}/seagull-1.0
%{_datadir}/gir-1.0/Seagull-1.0.gir
%{_pkgconfigdir}/seagull.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libseagull.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/seagull
%endif
