%define name	uqm
%define version	0.6.2
%define release %mkrel 2
%define	title		Ur-Quan Masters
%define	longtitle	The Ur-Quan Masters

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	The Ur-Quan Masters
License:	GPL
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
ExcludeArch:	x86_64 amd64
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
The Ur-Quan Masters is a port of the 3DO version of Star Control 2.

%prep
%setup -q -n %{name}-%{version}/sc2
%patch -p 2
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
Categories=Game/Strategy;
EOF

%post
%{update_menus}

%postun
%{clean_menus}

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


