#
# Conditional build:
%bcond_without	gconf		# gconf plugin
%bcond_without	gtk		# gtk window decorator
%bcond_without	gnome		# gnome settings module
%bcond_without	metacity	# metacity theme support
%bcond_with	kde		# kde-window-decorator (not working)
#
Summary:	OpenGL window and compositing manager
Summary(pl):	OpenGL-owy zarz�dca okien i sk�adania
Name:		compiz
Version:	0.2.0
Release:	1
License:	GPL or MIT
Group:		X11/Applications
Source0:	http://xorg.freedesktop.org/releases/individual/app/%{name}-%{version}.tar.bz2
# Source0-md5:	286a36ddb5d5b05534eb809eab541ec8
Source1:	%{name}-pld.png
# Source1-md5:	3050dc90fd4e5e990bb5baeb82bd3c8a
URL:		http://xorg.freedesktop.org/
%if %{with gconf} || %{with gtk}
BuildRequires:	GConf2-devel >= 2.0
%endif
BuildRequires:	Mesa-libGL-devel >= 6.5-1.20060411.2
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.0
BuildRequires:	dbus-devel >= 0.35
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	glitz-devel
BuildRequires:	intltool
BuildRequires:	libpng-devel
BuildRequires:	librsvg-devel >= 2.14.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	startup-notification-devel >= 0.7
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libXcomposite-devel
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXres-devel
%if %{with gtk}
BuildRequires:	gtk+2-devel >= 2:2.8.0
BuildRequires:	libwnck-devel >= 2.14.1-2
BuildRequires:	pango-devel >= 1.10.0
BuildRequires:	xorg-lib-libXrender-devel >= 0.8.4
%if %{with gnome}
BuildRequires:	control-center-devel >= 2.0
BuildRequires:	gnome-desktop-devel >= 2.0
BuildRequires:	gnome-menus-devel
%endif
%if %{with metacity}
BuildRequires:	metacity-devel >= 2.15.21
%endif
%endif
%if %{with kde}
BuildRequires:	QtCore-devel
BuildRequires:	QtGui-devel
BuildRequires:	qt4-build
%endif
Requires(post,preun):	GConf2
Conflicts:	xorg-xserver-xgl < 0.0.20060505
Obsoletes:	compiz-opacity
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Compiz is an OpenGL compositing manager that use
GLX_EXT_texture_from_pixmap for binding redirected top-level windows
to texture objects. It has a flexible plug-in system and it is
designed to run well on most graphics hardware.

%description -l pl
Compiz jest OpenGL-owym zarz�dc� sk�adania, u�ywaj�cym rozszerzenia
GLX_EXT_texture_from_pixmap w celu wi�zania przekierowanych okien do
tekstur. Posiada elastyczny system wtyczek i jest tak zaprojektowany,
by dobrze dzia�a� na wi�kszo�ci kart graficznych.

%package devel
Summary:	Header files for compiz
Summary(pl):	Pliki nag��wkowe dla compiza
Group:		X11/Development/Libraries
# (by compiz.pc; header requires only: OpenGL-devel, startup-notification-devel, damageproto, xextproto, libX11-devel)
Requires:	OpenGL-devel
Requires:	libpng-devel
Requires:	startup-notification-devel >= 0.7
Requires:	xorg-lib-libSM-devel
Requires:	xorg-lib-libXcomposite-devel
Requires:	xorg-lib-libXdamage-devel
Requires:	xorg-lib-libXinerama-devel
Requires:	xorg-lib-libXrandr-devel

%description devel
Header files for compiz.

%description devel -l pl
Pliki nag��wkowe dla compiza.

%package gconf
Summary:	GConf plugin for Compiz
Summary(pl):	Wtyczka GConf dla Compiza
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gconf
GConf plugin for Compiz.

%description gconf -l pl
Wtyczka GConf dla Compiza.

%package gnome-settings
Summary:	Compiz settings for GNOME control panel
Summary(pl):	Ustawienia compiza dla panelu sterowania GNOME
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gnome-settings
Compiz settings for GNOME control panel.

%description gnome-settings -l pl
Ustawienia compiza dla panelu sterowania GNOME.

%package gtk-decorator
Summary:	Window decorator for GTK+
Summary(pl):	Dekorator okien dla GTK+
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Obsoletes:	compiz-gnome-decorator

%description gtk-decorator
Window decorator for GTK+.

%description gtk-decorator -l pl
Dekorator okien dla GTK+.

%package kde-decorator
Summary:	Window decorator for KDE
Summary(pl):	Dekorator okien dla KDE
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description kde-decorator
Window decorator for KDE.

%description kde-decorator -l pl
Dekorator okien dla KDE.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static \
	--enable-librsvg \
	%{!?with_gconf:--disable-gconf} \
	%{!?with_gnome:--disable-gnome} \
	%{!?with_gtk:--disable-gtk} \
	%{!?with_metacity:--disable-metacity} \
	%{?with_kde:--enable-kde}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	desktopfilesdir=%{_datadir}/wm-properties \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/compiz/novell.png

rm -f $RPM_BUILD_ROOT%{_libdir}/compiz/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post gconf
%gconf_schema_install compiz.schemas

%preun gconf
%gconf_schema_uninstall compiz.schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING COPYING.MIT ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/compiz
%dir %{_libdir}/compiz
%attr(755,root,root) %{_libdir}/compiz/*.so
%{?with_gconf:%exclude %{_libdir}/compiz/libgconf.so}
%{_datadir}/compiz

%files devel
%defattr(644,root,root,755)
%{_includedir}/compiz
%{_pkgconfigdir}/compiz.pc

%if %{with gconf}
%files gconf
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/compiz/libgconf.so
%{_sysconfdir}/gconf/schemas/compiz.schemas
%endif

%if %{with gnome}
%files gnome-settings
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/window-manager-settings/*.so
%{_datadir}/wm-properties/compiz.desktop
%endif

%if %{with gtk}
%files gtk-decorator
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gtk-window-decorator
%endif

%if %{with kde}
%files kde-decorator
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kde-window-decorator
%endif
