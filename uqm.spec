%define name	uqm
%define version	0.6.2
%define release 9
%define	title		Ur-Quan Masters
%define	longtitle	The Ur-Quan Masters

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	The Ur-Quan Masters
License:	GPLv2
Group:		Games/Strategy
URL:		http://sc2.sourceforge.net
Source0:	http://prdownloads.sourceforge.net/sc2/%{name}-%{version}-source.tar.bz2
Source1:	%{name}-16.png.bz2
Source2:	%{name}-32.png.bz2
Source3:	%{name}-48.png.bz2
Patch0:		%{name}-0.6.2-build.patch
Requires:	%{name}-content
BuildRequires:	SDL-devel >= 1.2.3
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libmikmod-devel
BuildRequires:	mesaglu-devel
#ExcludeArch:	x86_64 amd64
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
The Ur-Quan Masters is a port of the 3DO version of Star Control 2.

%prep
%setup -q -n %{name}-%{version}/sc2
%patch0 -p 2
bzcat %{SOURCE1} > %{name}-16.png
bzcat %{SOURCE2} > %{name}-32.png
bzcat %{SOURCE3} > %{name}-48.png

# create configuration
cat > config.state <<EOF
CHOICE_debug_VALUE='nodebug'
CHOICE_graphics_VALUE='opengl'
CHOICE_sound_VALUE='mixsdl'
CHOICE_ioformat_VALUE='stdio_zip'
INPUT_install_prefix_VALUE='%{_gamesbindir}'
INPUT_install_bindir_VALUE='%{_gamesbindir}'
INPUT_install_libdir_VALUE='%{_libdir}'
INPUT_install_sharedir_VALUE='%{_gamesdatadir}'
EOF

%build
./build.sh uqm < /dev/null

%install
rm -rf %{buildroot}
perl -pi -e 's|%{_prefix}|%{buildroot}%{_prefix}|' build.vars
./build.sh uqm install

# icons
install -D -m 644 %{name}-48.png %{buildroot}%{_liconsdir}/%{name}.png 
install -D -m 644 %{name}-32.png %{buildroot}%{_iconsdir}/%{name}.png 
install -D -m 644 %{name}-16.png %{buildroot}%{_miconsdir}/%{name}.png

# menu
install -d -m 755 %{buildroot}%{_datadir}/applications
cat >  %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{title}
Comment=%{longtitle}
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=Game;StrategyGame
EOF

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS BUGS COPYING WhatsNew ChangeLog README Contributing
%doc doc/users/manual.txt
%{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png




%changelog
* Sat Jul 10 2010 Tomas Kindl <supp@mandriva.org> 0.6.2-8mdv2011.0
+ Revision: 550186
- bump revision (rev. 547807 fixes...)
- make it compile again, fix patch tag
- allow build on x86_64 as it works...

* Fri Sep 05 2008 Guillaume Rousse <guillomovitch@mandriva.org> 0.6.2-7mdv2009.0
+ Revision: 281709
- fix menu (bug #43288)

* Thu Aug 14 2008 Götz Waschk <waschk@mandriva.org> 0.6.2-6mdv2009.0
+ Revision: 271862
- update license

* Sun Aug 03 2008 Thierry Vignaud <tv@mandriva.org> 0.6.2-5mdv2009.0
+ Revision: 261778
- rebuild

* Wed Jul 30 2008 Thierry Vignaud <tv@mandriva.org> 0.6.2-4mdv2009.0
+ Revision: 255180
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 0.6.2-2mdv2008.1
+ Revision: 140925
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - kill desktop-file-validate's error: string list key "Categories" in group "Desktop Entry" does not have a semicolon (";") as trailing character
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'


* Wed Feb 14 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.6.2-2mdv2007.0
+ Revision: 121003
- drop versioning on content dependency

* Wed Jan 24 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.6.2-1mdv2007.1
+ Revision: 112948
- fix build dependencies
- new version
- rediff build patch
- new version
- Import uqm

* Thu Jun 22 2006 Guillaume Rousse <guillomovitch@mandriva.org> 0.5.0-3mdv2007.0
- fix buildrequires
- xdg menu

* Fri May 12 2006 Guillaume Rousse <guillomovitch@mandriva.org> 0.5.0-2mdk
- excludes x86_64 arch, as it contains uncompatible assembler code

* Tue Mar 21 2006 Guillaume Rousse <guillomovitch@mandriva.org> 0.5.0-1mdk
- New release 0.5.0

* Wed Aug 24 2005 Guillaume Rousse <guillomovitch@mandriva.org> 0.4.0-3mdk
- fix x86_64 build
- %%mkrel

* Tue May 31 2005 Guillaume Rousse <guillomovitch@mandriva.org> 0.4.0-2mdk 
- requires uqm-content = 0.6.2

* Sun May 29 2005 Guillaume Rousse <guillomovitch@mandriva.org> 0.4.0-1mdk
- New release 0.4.0
- fix build
- correct optimisations
- fix menu entry
- spec cleanup

* Sat Jul 24 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.3-3mdk 
- rpmbuildupdate aware
- fixed menu category

