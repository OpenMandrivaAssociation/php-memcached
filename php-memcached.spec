%define modname memcached
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A91_%{modname}.ini

Summary:	A libmemcached library interface for PHP
Name:		php-%{modname}
Version:	3.0.4
Release:	2
Group:		Development/PHP
License:	PHP License
URL:		https://pecl.php.net/package/memcached
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Source1:	%{modname}.ini
BuildRequires:	libmemcached-devel >= 0.38
BuildRequires:	php-devel >= 3:5.2.1
BuildRequires:	dos2unix
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This extension uses libmemcached library to provide API for communicating with
memcached servers.

%prep

%setup -n %{modname}-%{version}
mv %{_builddir}/package.xml %{_builddir}/%{modname}-%{version}/

cp %{SOURCE1} %{inifile}

find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

# strip away annoying ^M
find -type f | grep -v ".gif" | grep -v ".png" | grep -v ".jpg" | xargs dos2unix

%build
%serverbuild

phpize
%configure --with-libdir=%{_lib} \
    --enable-%{modname}=shared,%{_prefix} \
    --with-zlib-dir=%{_prefix}

%make
mv modules/*.so .

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

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
%doc CREDITS ChangeLog memcached-api.php package.xml
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}



%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 2.0.1-2mdv2012.0
+ Revision: 795476
- rebuild for php-5.4.x

* Tue Apr 10 2012 Oden Eriksson <oeriksson@mandriva.com> 2.0.1-1
+ Revision: 790155
- 2.0.1

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-12
+ Revision: 761268
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-11
+ Revision: 696445
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-10
+ Revision: 695440
- rebuilt for php-5.3.7

* Tue Jun 21 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-9
+ Revision: 686442
- rebuilt against libmemcached.so.8

* Fri Apr 22 2011 Funda Wang <fwang@mandriva.org> 1.0.2-8
+ Revision: 656603
- rebuild

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-7
+ Revision: 646661
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-6mdv2011.0
+ Revision: 629835
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-5mdv2011.0
+ Revision: 628162
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-4mdv2011.0
+ Revision: 600508
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-3mdv2011.0
+ Revision: 588846
- rebuild

* Sun Oct 10 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-2mdv2011.0
+ Revision: 584645
- rebuilt against new libmemcached

* Thu May 06 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-1mdv2010.1
+ Revision: 542970
- 1.0.2

* Sat Apr 24 2010 Funda Wang <fwang@mandriva.org> 1.0.1-2mdv2010.1
+ Revision: 538456
- rebuild

* Sat Mar 27 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-1mdv2010.1
+ Revision: 527912
- 1.0.1
- fix deps
- rebuilt for php-5.3.2

* Wed Jan 13 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-7mdv2010.1
+ Revision: 490982
- rebuilt against new libmemcached.so.4

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-6mdv2010.1
+ Revision: 485405
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-5mdv2010.1
+ Revision: 468188
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-4mdv2010.0
+ Revision: 451292
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1.0.0-3mdv2010.0
+ Revision: 397556
- Rebuild

* Sat Jul 11 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-2mdv2010.0
+ Revision: 394779
- rebuilt against new libmemcached

* Wed Jul 08 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1mdv2010.0
+ Revision: 393463
- 1.0.0

* Sat Jun 06 2009 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-1mdv2010.0
+ Revision: 383324
- 0.2.0

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.5-1mdv2010.0
+ Revision: 376963
- 0.1.5

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-2mdv2009.1
+ Revision: 346519
- rebuilt for php-5.2.9

* Sun Feb 22 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-1mdv2009.1
+ Revision: 343816
- 0.1.4

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.3-2mdv2009.1
+ Revision: 341778
- rebuilt against php-5.2.9RC2

* Sat Feb 07 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.3-1mdv2009.1
+ Revision: 338374
- import php-memcached


* Sat Feb 07 2009 Oden Eriksson <oeriksson@mandriva.org> 0.1.3-1mdv2009.1
- initial Mandriva package
