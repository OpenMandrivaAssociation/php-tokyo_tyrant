%define modname tokyo_tyrant
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A96_%{modname}.ini

Summary:	Provides a wrapper to the Tokyo Tyrant client library
Name:		php-%{modname}
Version:	0.6.0
Release:	7
Group:		Development/PHP
License:	PHP License
URL:		https://pecl.php.net/package/tokyo_tyrant/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Patch0:		tokyo_tyrant-0.6.0-php54x.diff
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

%patch0 -p1

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



%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-6mdv2012.0
+ Revision: 796983
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-5
+ Revision: 761338
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-4
+ Revision: 696483
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-3
+ Revision: 695484
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-2
+ Revision: 646697
- rebuilt for php-5.3.6

* Wed Feb 23 2011 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-1
+ Revision: 639434
- 0.6.0

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.5.0-5mdv2011.0
+ Revision: 629894
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.5.0-4mdv2011.0
+ Revision: 628203
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5.0-3mdv2011.0
+ Revision: 600543
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5.0-2mdv2011.0
+ Revision: 588880
- rebuild

* Fri Jun 11 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5.0-1mdv2010.1
+ Revision: 547883
- 0.5.0

* Tue Mar 30 2010 Oden Eriksson <oeriksson@mandriva.com> 0.4.0-1mdv2010.1
+ Revision: 529185
- 0.4.0

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.3.0-2mdv2010.1
+ Revision: 514703
- rebuilt for php-5.3.2

* Mon Mar 01 2010 Oden Eriksson <oeriksson@mandriva.com> 0.3.0-1mdv2010.1
+ Revision: 512918
- 0.3.0

* Sun Jan 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-1mdv2010.1
+ Revision: 485918
- remove one redundant patch
- 0.2.0

* Sun Dec 27 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.2-1mdv2010.1
+ Revision: 482779
- 0.1.2

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-2mdv2010.1
+ Revision: 468266
- rebuilt against php-5.3.1

* Sun Oct 04 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-1mdv2010.0
+ Revision: 453365
- 0.1.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-2mdv2010.0
+ Revision: 451368
- rebuild

* Wed Aug 19 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdv2010.0
+ Revision: 418225
- import php-tokyo_tyrant


* Wed Aug 19 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdv2009.1
- initial Mandriva package
