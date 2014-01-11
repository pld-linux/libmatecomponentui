# NOTE: this package is deprecated, meant for MATE <= 1.4 compatibility only
#
# Conditional build:
%bcond_with	static_libs	# static library
#
Summary:	MateComponent user interface components
Summary(pl.UTF-8):	Komponenty interfejsu użytkownika do MateComponent
Name:		libmatecomponentui
Version:	1.4.0
Release:	1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz
# Source0-md5:	b4d97af4b7cbc15e51b0577d9e2aa327
URL:		http://mate-desktop.org/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.9
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.6.0
BuildRequires:	gtk+2-devel >= 2:2.6.0
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libglade2-devel >= 2.0
BuildRequires:	libmatecanvas-devel
BuildRequires:	libmatecomponent-devel
BuildRequires:	libmate-devel
BuildRequires:	libtool >= 1:1.4.3
BuildRequires:	libxml2-devel >= 1:2.4.20
BuildRequires:	mate-common
BuildRequires:	mate-conf-devel
BuildRequires:	pango-devel
BuildRequires:	pangox-compat-devel
BuildRequires:	pkgconfig
BuildRequires:	popt-devel >= 1.5
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
BuildConflicts:	gdk-pixbuf-devel < 0.12
Requires:	glib2 >= 1:2.6.0
Requires:	gtk+2 >= 2:2.6.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MateComponent is a component system based on CORBA, used by the MATE
desktop. libmatecomponentui contains the user interface related
components that come with MateComponent.

%description -l pl.UTF-8
MateComponent jest systemem komponentów bazującym na CORB-ie, używanym
przez środowisko MATE. libmatecomponentui zawiera komponenty związane
z interfejsem użytkownika, które przychodzą z MateComponent.

%package devel
Summary:	Headers for libmatecomponentui
Summary(pl.UTF-8):	Pliki nagłówkowe libmatecomponentui
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.6.0
Requires:	gtk+2-devel >= 2:2.6.0
Requires:	libglade2-devel >= 2.0
Requires:	libmate-devel
Requires:	libmatecomponent-devel
Requires:	libmatecanvas-devel
Requires:	libxml2-devel >= 1:2.4.20
Requires:	mate-conf-devel

%description devel
This package contains header files used to compile programs that use
libmatecomponentui.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do kompilacji programów
używających libmatecomponentui.

%package static
Summary:	Static libmatecomponentui library
Summary(pl.UTF-8):	Statyczna biblioteka libmatecomponentui
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static version of libmatecomponentui.

%description static -l pl.UTF-8
Ten pakiet zawiera statyczną wersję biblioteki libmatecomponentui.

%package apidocs
Summary:	libmatecomponentui API documentation
Summary(pl.UTF-8):	Dokumentacja API libmatecomponentui
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
libmatecomponentui API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API libmatecomponentui.

%package -n mate-matecomponent-browser
Summary:	MateComponent component viewer
Summary(pl.UTF-8):	Przeglądarka komponentów matecomponent
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description -n mate-matecomponent-browser
Shows available MateComponent components.

%description -n mate-matecomponent-browser -l pl.UTF-8
Wyświetla dostępne komponenty matecomponent.

%prep
%setup -q

%build
%{__gtkdocize}
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	PATH_TO_XRDB=/usr/bin/xrdb \
	--enable-gtk-doc \
	%{!?with_static_libs:--disable-static} \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no static modules and *.la for glade modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libglade/2.0/*.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libglade/2.0/*.a
%endif
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%{__mv} $RPM_BUILD_ROOT%{_datadir}/locale/{sr@ije,sr@ijekavian}

%find_lang %{name}
# --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/mate-test-moniker
%attr(755,root,root) %{_libdir}/libmatecomponentui-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmatecomponentui-2.so.0
%attr(755,root,root) %{_libdir}/libglade/2.0/libmatecomponent.so
%{_libdir}/matecomponent/servers/CanvDemo.server
%{_libdir}/matecomponent/servers/MateComponent_Sample_Controls.server
%attr(755,root,root) %{_libdir}/matecomponent-2.0/samples/matecomponent-sample-controls-2
%dir %{_datadir}/mate-2.0
%dir %{_datadir}/mate-2.0/ui
%{_datadir}/mate-2.0/ui/MateComponent_Sample_Container-ui.xml
%{_datadir}/mate-2.0/ui/MateComponent_Sample_Hello.xml

%files devel
%defattr(644,root,root,755)
%doc doc/*.xml doc/*.txt doc/*.html doc/*.dtd
%attr(755,root,root) %{_libdir}/libmatecomponentui-2.so
%{_pkgconfigdir}/libmatecomponentui-2.0.pc
%{_includedir}/libmatecomponentui-2.0

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmatecomponentui-2.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libmatecomponentui

%files -n mate-matecomponent-browser
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/matecomponent-browser
%{_datadir}/mate-2.0/ui/matecomponent-browser.xml
%{_desktopdir}/matecomponent-browser.desktop
