%define modname tokyo_tyrant
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A96_%{modname}.ini

Summary:	Provides a wrapper to the Tokyo Tyrant client library
Name:		php-%{modname}
Version:	0.2.0
Release:	%mkrel 1
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/tokyo_tyrant/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Patch0:		tokyo_tyrant-0.1.0-build_fix.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	tokyotyrant
BuildRequires:	tokyotyrant-devel
BuildRequires:	tokyocabinet-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
tokyo_tyrant extension provides object oriented API for communicating with
Tokyo Tyrant key-value store.

This extension requires Tokyo Cabinet, Tokyo Tyrant and PHP version 5.2.0+.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%patch0 -p0

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS package*.xml 
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}

