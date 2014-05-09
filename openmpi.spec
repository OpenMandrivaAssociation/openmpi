%global _fmoddir %{_libdir}/gfortran
%global _disable_ld_no_undefined 1
%global serverbuild_hardened 1
# We only compile with gcc, but other people may want other compilers.
# Set the compiler here.
%global opt_cc gcc
# Optional CFLAGS to use with the specific compiler...gcc doesn't need any,
# so uncomment and define to use
#global opt_cflags
%global opt_cxx g++
#global opt_cxxflags
%global opt_f77 gfortran
#global opt_fflags
%global opt_fc gfortran
#global opt_fcflags

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
# Optional name suffix to use...we leave it off when compiling with gcc, but
# for other compiled versions to install side by side, it will need a
# suffix in order to keep the names from conflicting.
#global _cc_name_suffix -gcc

%global macrosdir %_sys_macros_dir

Name:			openmpi%{?_cc_name_suffix}
Version:		1.8.1
Release:		1%{?dist}
Summary:		Open Message Passing Interface

License:		BSD, MIT and Romio
URL:			http://www.open-mpi.org/

# We can't use %{name} here because of _cc_name_suffix
Source0:		http://www.open-mpi.org/software/ompi/v1.8/downloads/openmpi-%{version}.tar.bz2
Source1:		openmpi.module.in
Source2:		macros.openmpi
Source3:		%{name}.rpmlintrc
# Patch to use system ltdl for tests
Patch1:			openmpi-ltdl.patch

BuildRequires:		gcc-gfortran
#sparc64 and aarch64 don't have valgrind
%ifnarch %{sparc} aarch64
BuildRequires:		valgrind-devel
%endif
BuildRequires:		libibverbs-devel >= 1.1.3, opensm-devel > 3.3.0
BuildRequires:		librdmacm-devel libibcm-devel
BuildRequires:		pkgconfig(hwloc)
# So configure can find lstopo
BuildRequires:		hwloc
BuildRequires:		java-devel
BuildRequires:		libevent-devel
BuildRequires:		papi-devel
BuildRequires:		python libltdl-devel
BuildRequires:		torque-devel

Provides:		mpi
Requires:		environment-modules
# openmpi currently requires ssh to run
# https://svn.open-mpi.org/trac/ompi/ticket/4228
Requires:		openssh-clients

# s390 is unlikely to have the hardware we want, and some of the -devel
# packages we require aren't available there.
ExcludeArch: s390 s390x

# Private openmpi libraries
%global __provides_exclude_from %{_libdir}/openmpi/lib/(lib(mca|ompi|open-(pal|rte|trace)|otf|v)|openmpi/).*.so
%global __requires_exclude lib(mca|ompi|open-(pal|rte|trace)|otf|vt).*

%description
Open MPI is an open source, freely available implementation of both the 
MPI-1 and MPI-2 standards, combining technologies and resources from
several other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in
order to build the best MPI library available.  A completely new MPI-2
compliant implementation, Open MPI offers advantages for system and
software vendors, application developers, and computer science
researchers. For more information, see http://www.open-mpi.org/ .

%package devel
Summary:	Development files for openmpi

Requires:	%{name} = %{version}-%{release}, gcc-gfortran
Provides:	mpi-devel

%description devel
Contains development headers and libraries for openmpi.

%package java
Summary:	Java library

Requires:	%{name} = %{version}-%{release}
Requires:	java-headless

%description java
Java library.

%package java-devel
Summary:	Java development files for openmpi

Requires:	%{name}-java = %{version}-%{release}
Requires:	java-devel

%description java-devel
Contains development wrapper for compiling Java with openmpi.

# We set this to for convenience, since this is the unique dir we use for this
# particular package, version, compiler
%global namearch openmpi-%{_arch}%{?_cc_name_suffix}

%prep
%setup -q -n openmpi-%{version}
%patch1 -p1 -b .ltdl
# Make sure we don't use the local libltdl library
rm -r opal/libltdl

%build
./configure --prefix=%{_libdir}/%{name} \
	--mandir=%{_mandir}/%{namearch} \
	--includedir=%{_includedir}/%{namearch} \
	--sysconfdir=%{_sysconfdir}/%{namearch} \
	--disable-silent-rules \
	--enable-mpi-java \
	--enable-opal-multi-threads \
	--with-libevent=/usr \
	--with-verbs=/usr \
	--with-sge \
%ifnarch %{sparc} aarch64
	--with-valgrind \
	--enable-memchecker \
%endif
	--with-hwloc=/usr \
	--with-libltdl=/usr \
	CC=%{opt_cc} CXX=%{opt_cxx} \
	LDFLAGS='%{ldflags}' \
	CFLAGS="%{?opt_cflags} %{!?opt_cflags:$RPM_OPT_FLAGS}" \
	CXXFLAGS="%{?opt_cxxflags} %{!?opt_cxxflags:$RPM_OPT_FLAGS}" \
	FC=%{opt_fc} FCFLAGS="%{?opt_fcflags} %{!?opt_fcflags:$RPM_OPT_FLAGS}" \
	F77=%{opt_f77} FFLAGS="%{?opt_fflags} %{!?opt_fflags:$RPM_OPT_FLAGS}"

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}
rm -fr %{buildroot}%{_libdir}/%{name}/lib/pkgconfig
find %{buildroot}%{_libdir}/%{name}/lib -name \*.la | xargs rm
find %{buildroot}%{_mandir}/%{namearch} -type f | xargs gzip -9
ln -s mpicc.1.gz %{buildroot}%{_mandir}/%{namearch}/man1/mpiCC.1.gz
rm -f %{buildroot}%{_mandir}/%{namearch}/man1/mpiCC.1
rm -f %{buildroot}%{_mandir}/%{namearch}/man1/orteCC.1*
rm -f %{buildroot}%{_libdir}/%{name}/share/vampirtrace/doc/opari/lacsi01.ps.gz
mkdir %{buildroot}%{_mandir}/%{namearch}/man{2,4,5,6,8,9,n}

# Make the environment-modules file
mkdir -p %{buildroot}%{_sysconfdir}/modulefiles/mpi
# Since we're doing our own substitution here, use our own definitions.
sed 's#@LIBDIR@#'%{_libdir}/%{name}'#g;s#@ETCDIR@#'%{_sysconfdir}/%{namearch}'#g;s#@FMODDIR@#'%{_fmoddir}/%{namearch}'#g;s#@INCDIR@#'%{_includedir}/%{namearch}'#g;s#@MANDIR@#'%{_mandir}/%{namearch}'#g;s#@PYSITEARCH@#'%{python_sitearch}/%{name}'#g;s#@COMPILER@#openmpi-'%{_arch}%{?_cc_name_suffix}'#g;s#@SUFFIX@#'%{?_cc_name_suffix}'_openmpi#g' < %SOURCE1 > %{buildroot}%{_sysconfdir}/modulefiles/mpi/%{namearch}

# make the rpm config file
install -Dpm 644 %{SOURCE2} %{buildroot}/%{macrosdir}/%{namearch}.macros
mkdir -p %{buildroot}/%{_fmoddir}/%{namearch}
mkdir -p %{buildroot}/%{python_sitearch}/openmpi%{?_cc_name_suffix}
# Remove extraneous wrapper link libraries (bug 814798)
sed -i -e s/-ldl// -e s/-lhwloc// \
  %{buildroot}%{_libdir}/%{name}/share/openmpi/*-wrapper-data.txt

%check
make check

%files
%dir %{_libdir}/%{name}
%dir %{_sysconfdir}/%{namearch}
%dir %{_libdir}/%{name}/bin
%dir %{_libdir}/%{name}/lib
%dir %{_libdir}/%{name}/lib/openmpi
%dir %{_mandir}/%{namearch}
%dir %{_mandir}/%{namearch}/man*
%dir %{_fmoddir}/%{namearch}
%dir %{python_sitearch}/%{name}
%config(noreplace) %{_sysconfdir}/%{namearch}/*
%{_libdir}/%{name}/bin/mpi[er]*
%{_libdir}/%{name}/bin/ompi*
#%#{_libdir}/%{name}/bin/opari
%{_libdir}/%{name}/bin/orte[-dr_]*
%{_libdir}/%{name}/bin/oshmem_info
%{_libdir}/%{name}/bin/oshrun
%{_libdir}/%{name}/bin/otf*
%{_libdir}/%{name}/bin/shmemrun
%{_libdir}/%{name}/lib/*.so.*
%{_mandir}/%{namearch}/man1/mpi[er]*
%{_mandir}/%{namearch}/man1/ompi*
%{_mandir}/%{namearch}/man1/orte[-dr_]*
%{_mandir}/%{namearch}/man1/oshmem_info*
%{_mandir}/%{namearch}/man7/ompi*
%{_mandir}/%{namearch}/man7/orte*
%{_libdir}/%{name}/lib/openmpi/*
%{_sysconfdir}/modulefiles/mpi/
%dir %{_libdir}/%{name}/share
%dir %{_libdir}/%{name}/share/openmpi
%{_libdir}/%{name}/share/openmpi/doc
%{_libdir}/%{name}/share/openmpi/amca-param-sets
%{_libdir}/%{name}/share/openmpi/help*.txt
%{_libdir}/%{name}/share/openmpi/mca-btl-openib-device-params.ini
%{_libdir}/%{name}/share/openmpi/mca-coll-ml.config

%files devel
%dir %{_includedir}/%{namearch}
%dir %{_libdir}/%{name}/share/vampirtrace
%{_libdir}/%{name}/bin/mpi[cCf]*
%{_libdir}/%{name}/bin/opal_*
%{_libdir}/%{name}/bin/orte[cCf]*
%{_libdir}/%{name}/bin/osh[cf]*
%{_libdir}/%{name}/bin/shmem[cf]*
%{_libdir}/%{name}/bin/vt*
%{_includedir}/%{namearch}/*
%{_libdir}/%{name}/lib/*.so
%{_libdir}/%{name}/lib/lib*.a
%{_libdir}/%{name}/lib/mpi.mod
%{_mandir}/%{namearch}/man1/mpi[cCf]*
%{_mandir}/%{namearch}/man1/opal_*
%{_mandir}/%{namearch}/man3/*
%{_mandir}/%{namearch}/man7/opal*
%{_libdir}/%{name}/share/openmpi/openmpi-valgrind.supp
%{_libdir}/%{name}/share/openmpi/*-wrapper-data.txt
%{_libdir}/%{name}/share/vampirtrace/*
%{macrosdir}/%{namearch}.macros

%files java
%{_libdir}/%{name}/lib/mpi.jar

%files java-devel
%{_libdir}/%{name}/bin/mpijavac
%{_libdir}/%{name}/bin/mpijavac.pl
# Currently this only contaings openmpi/javadoc
%{_libdir}/%{name}/share/doc/
%{_mandir}/%{namearch}/man1/mpijavac.1*
