
Name:    kdepim3
Summary: Compatibility support for kdepim3 
Version: 3.5.10
Release: 3%{?dist}.goose.1

License: GPLv2
Group:   Applications/Productivity
URL:     http://www.kde.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: ftp://ftp.kde.org/pub/kde/stable/%{version}/src/kdepim-%{version}.tar.bz2

BuildRequires: bison flex
BuildRequires: desktop-file-utils
BuildRequires: kdelibs3-devel >= %{version}
BuildRequires: zlib-devel
BuildRequires: libart_lgpl-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: lockdev-devel
BuildRequires: python-devel
## Crypto Stuff from http://kmail.kde.org/kmail-pgpmime-howto.html
BuildRequires: gpgme-devel
BuildRequires: libXpm-devel libXScrnSaver-devel
BuildRequires: gcc-c++

%description
%{summary}, including libkcal.

%package libs
Summary: Runtime files for %{name}
Group: System Environment/Libraries
%description libs
%{summary}, including libkcal.

%package devel
Summary: Development files for %{name} 
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: kdelibs3-devel
# kdepimlibs-devel-4.2.1-2 fixed to avoid conflicts -- Rex
Conflicts: kdepimlibs-devel < 4.2.1-2
%description devel
%{summary}.


%prep
%setup -q -n kdepim-%{version}


%build
unset QTDIR || : ; . /etc/profile.d/qt.sh

%configure \
   --enable-new-ldflags \
   --disable-dependency-tracking \
   --disable-rpath \
   --disable-debug --disable-warnings \
   --enable-final \
   --includedir=%{_includedir}/kde \
   --with-gpg=%{_bindir}/gpg \
   --with-gpgsm=%{_bindir}/gpgsm \
   --with-sasl \
  %{?_with_gnokii} %{!?_with_gnokii:--without-gnokii} \
  %{?_with_mal} %{!?_with_mal:--without-mal} \
  %{?_with_pilot_link} %{!?_with_pilot_link:--without-pilot-link}

for lib in ktnef libkmime libemailfunctions libkcal libkdepim; do
make %{?_smp_mflags} -C ${lib}
done


%install
rm -rf %{buildroot} 

for lib in ktnef libkmime libemailfunctions libkcal libkdepim; do
make install DESTDIR=%{buildroot} -C $lib
done

#unpackaged files
rm -f  %{buildroot}%{_libdir}/lib*.la
rm -f  %{buildroot}%{_libdir}/libkdepim*
rm -rf %{buildroot}%{_datadir}/apps/libkdepim/
rm -rf %{buildroot}%{_datadir}/apps/kdepimwidgets/
rm -f  %{buildroot}%{_libdir}/kde3/plugins/designer/*
rm -f  %{buildroot}%{_libdir}/lib{kmime,ktnef}.so
rm -rf %{buildroot}%{_includedir}/kde/ktnef/
rm -rf %{buildroot}%{_datadir}/applications
rm -rf %{buildroot}%{_datadir}/icons
rm -rf %{buildroot}%{_datadir}/mimelnk
rm -rf %{buildroot}%{_datadir}/apps/ktnef
rm -f  %{buildroot}%{_bindir}/ktnef


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%clean
rm -rf %{buildroot}


%files libs
%defattr(-,root,root,-)
%doc README korganizer/COPYING
%{_datadir}/config.kcfg/pimemoticons.kcfg
%{_datadir}/apps/libical/
%{_datadir}/services/kresources/kcal*
%{_libdir}/libkcal.so.2*
%{_libdir}/kde3/kcal*
%{_libdir}/libkmime.so.2*
%{_libdir}/libktnef.so.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/kde/kdepimmacros.h
%{_includedir}/kde/libemailfunctions/
%{_includedir}/kde/libkcal/
%{_libdir}/libkcal.so


%changelog
* Mon May 7 2012 Clint Savage <herlo@gooseproject.org> - 3.5.10-3.goose.1
- BR of gcc-c++ is needed

* Tue Jan 12 2010 Radek Novacek <rnovacek@redhat.com> - 3.5.10-3
- Fixed wrong usage of macro in description.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 3.5.10-2.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 03 2009 Rex Dieter <rdieter@fedoraproject.org> 3.5.10-1
- first try at kdepim3 compat pkg, including libkcal

