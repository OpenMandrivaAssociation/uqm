%define	title		Ur-Quan Masters
%define	longtitle	The Ur-Quan Masters
%define debug_package	%{nil}

Name:		uqm
Version:	0.8.0
Release:	1
Summary:	The Ur-Quan Masters
License:	GPLv2
Group:		Games/Strategy
URL:		http://sc2.sourceforge.net
Source0:	https://sourceforge.net/projects/sc2/files/UQM/%(echo %{version} |cut -d. -f1-2)/uqm-%{version}-src.tgz
Source1:	%{name}-16.png
Source2:	%{name}-32.png
Source3:	%{name}-48.png
#Patch0:		%{name}-0.6.2-build.patch
Requires:	%{name}-content
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(libmikmod)
BuildRequires:	pkgconfig(glu)

%description
The Ur-Quan Masters is a port of the 3DO version of Star Control 2.

%prep
%autosetup -p1

# create configuration
cat > config.state <<EOF
CHOICE_debug_VALUE='nodebug'
CHOICE_graphics_VALUE='sdl2'
CHOICE_sound_VALUE='mixsdl'
CHOICE_mikmod_VALUE='external'
CHOICE_ovcodec_VALUE='standard'
CHOICE_netplay_VALUE='full'
CHOICE_joystick_VALUE='enabled'
CHOICE_ioformat_VALUE='stdio_zip'
CHOICE_accel_VALUE='asm'
CHOICE_threadlib_VALUE='sdl'
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
install -D -m 644 %{S:3} %{buildroot}%{_liconsdir}/%{name}.png 
install -D -m 644 %{S:2} %{buildroot}%{_iconsdir}/%{name}.png 
install -D -m 644 %{S:1} %{buildroot}%{_miconsdir}/%{name}.png

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
