Summary:	Tools for burning CDRs in Disk At Once mode
Name:		cdrdao
Version:	1.2.3
Release:	2
License:	GPL v2+
Group:		Applications/System
Source0:	http://heanet.dl.sourceforge.net/cdrdao/%{name}-%{version}.tar.bz2
# Source0-md5:	8d15ba6280bb7ba2f4d6be31d28b3c0c
# http://cdrdao.sourceforge.net/drives.html#dt
Source1:	%{name}.drivers
Patch0:		%{name}-nolibs.patch
Patch1:		%{name}-pccts-antlr.patch
Patch2:		%{name}-glibc-2.10.patch
Patch3:		%{name}-stat.patch
URL:		http://cdrdao.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	lame-libs-devel
BuildRequires:	libao-devel
BuildRequires:	libmad-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libvorbis-devel
BuildRequires:	pkg-config
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cdrdao records audio and data CD-Rs in Disk At Once mode. This mode
gives much better control over contents of CD.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%{__sed} -i 's#/usr/src/linux/include##g' scsilib/DEFAULT*/Defaults.linux

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
PKG_CONFIG=%{_bindir}/pkg-config	\
%configure				\
	--with-mp3-support		\
	--with-ogg-support		\
	--with-pcctsbin=%{_bindir}	\
	--with-pcctsinc=%{_libdir}/pccts/h

%{__make} \
	CC="%{__cc}"			\
	COPTOPT="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/%{name}/drivers

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CREDITS README README.PlexDAE
%attr(755,root,root) %{_bindir}/cdrdao
%attr(755,root,root) %{_bindir}/toc2*
%attr(755,root,root) %{_bindir}/cue2toc
%{_datadir}/%{name}
%{_mandir}/man1/cdrdao.1*
%{_mandir}/man1/cue2toc.1*
%{_mandir}/man1/toc2cddb.1*
%{_mandir}/man1/toc2cue.1*

