%define         _disable_ld_no_undefined 0
%define		_disable_rebuild_configure %nil

%define         major                    40

%define         cxx_major                %{major}
%define         usempif08_major          %{major}
%define         usempi_ignore_major      %{major}
%define         mpifh_major              %{major}
%define         ompitrace_major          %{major}
%define         opentrace_major          %{major}
%define         openpal_major            %{major}
%define         openrte_major            %{major}
%define         oshmem_major             %{major}

%global		macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

%define         libname                  %mklibname %{name} %{major}
%define         develname                %mklibname %{name} -d
%define         staticdevelname          %mklibname %{name} -s -d

%define         gccinstalldir   %(LC_ALL=C %__cc --print-search-dirs | %__grep install | %__awk '{print $2}')
%define         fincludedir     %{_libdir}/%{name}

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
# We set this to for convenience, since this is the unique dir we use for this
# particular package, version, compiler
%global namearch openmpi-%{_arch}%{?_cc_name_suffix}

# Private openmpi libraries
%global __provides_exclude_from %{_libdir}/openmpi/lib/(lib(mca|ompi|open-(pal|rte|trace))|openmpi/).*.so
%global __requires_exclude lib(mca|ompi|open-(pal|rte|trace)|vt).*

%ifarch aarch64 ppc64le %{x86_64}
%bcond_with ucx
%else
%bcond_with ucx
%endif

# ARM 32-bit is not supported by rdma
# https://bugzilla.redhat.com/show_bug.cgi?id=1780584
%ifarch %{arm}
%bcond_with rdma
%else
%bcond_without rdma
%endif


Summary:        An implementation of the Message Passing Interface
Name:           openmpi
Version:        4.1.2
Release:        1
License:        BSD
Group:          Development/Other

URL:            http://www.open-mpi.org
# We can't use %%{name} here beVcause of _cc_name_suffix
Source0:	https://www.open-mpi.org/software/ompi/v4.1/downloads/openmpi-%{version}.tar.bz2
Source1:        openmpi.module.in
Source3:        openmpi.pth.py3
Source4:        macros.openmpi

Patch0:         ompi_autogen_sh.patch
Patch1:         arm_detection.diff
Patch2:         openmpi-1.10.1-fix-function-if.patch
Patch11:        openmpi-3.1.0-addconditional-scmpset-atomic.patch

BuildRequires:  perl
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gawk
BuildRequires:  valgrind-devel
BuildRequires:  pkgconfig(libevent)
BuildRequires:  gcc-gfortran
%ifarch %ix86 %{x86_64} aarch64
BuildRequires:  java-openjdk
BuildRequires:  java-devel
%endif
%if %{with rdma}
BuildRequires:  pkgconfig(librdmacm)
%endif
%if %{with ucx}
BuildRequires:   ucx-devel
%endif
BuildRequires:  gcc-c++
BuildRequires:  binutils-devel
BuildRequires:  pkgconfig(libibverbs)
BuildRequires:  libgomp-devel
#BuildRequires:  torque-devel >= 2.3.7
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(hwloc)
BuildRequires:  hwloc
BuildRequires:  autoconf

Requires:       %{libname} = %{version}-%{release}
Recommends:       %{develname} = %{version}-%{release}

Conflicts:      mpich
Conflicts:      mpich2
Conflicts:      lam


%description
The Open MPI Project is an open source fully compliant MPI-3
implementation that is developed and maintained by a consortium of
academic, research, and industry partners. OpenMPI is therefore able
to combine the expertise, technologies, and resources from all across
the High Performance Computing community in order to build the best
MPI library available. OpenMPI offers advantages for system and
software vendors, application developers and computer science
researchers. This package contains all of the tools necessary to
compile, link, and run OpenMPI jobs.



%package -n %{libname}
Summary:        Shared libraries for OpenMPI
Group:          Development/Other
Provides:       lib%{name} = %{version}-%{release}
Obsoletes:      %{_lib}openmpi0 <= 1.5
# Build with wrong major:
Obsoletes:      %{_lib}openmpi1 < 1.10.0-2

%description -n %{libname}
%{summary}.



%package -n %{develname}
Summary:        Development files for OpenMPI
Group:          Development/Other
Requires:       %{libname} = %{version}-%{release}
#was Requires
Recommends:       %{name} = %{version}-%{release}
Requires:       gcc-gfortran 
Requires:       gcc-c++
Provides:       lib%{name}-devel  = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
Conflicts:      lam-devel
Conflicts:      mpich1-devel
Conflicts:      mpich2-devel

%description -n %{develname}
%{summary}.



%package -n %{staticdevelname}
Summary:        Static Development files for OpenMPI
Group:          Development/Other
Requires:       %{libname} = %{version}-%{release}
Requires:       gcc-gfortran 
Requires:       gcc-c++
Provides:       lib%{name}-static-devel  = %{version}-%{release}
Provides:       %{name}-static-devel = %{version}-%{release}
Conflicts:      lam-devel
Conflicts:      mpich1-devel
Conflicts:      mpich2-devel

%description -n %{staticdevelname}
%{summary}.

%package java
Summary:    Java library
Requires:   %{name} = %{version}-%{release}
Requires:   java-headless
 
%description java
Java library.
 
%package java-devel
Summary:    Java development files for openmpi
Requires:   %{name}-java = %{version}-%{release}
Requires:   java-devel
%description java-devel
Contains development wrapper for compiling Java with openmpi.

%package -n python-openmpi
Summary:    OpenMPI support for Python 3
Requires:   %{name} = %{version}-%{release}
Requires:   python(abi) = %{python3_version}
 
%description -n python-openmpi
OpenMPI support for Python 3.


%prep
%setup -q


%build
./configure --prefix=%{_libdir}/%{name} \
	--mandir=%{_mandir}/%{namearch} \
	--includedir=%{_includedir}/%{namearch} \
	--sysconfdir=%{_sysconfdir}/%{namearch} \
	--disable-silent-rules \
	--enable-builtin-atomics \
	--enable-mpi-cxx \
	--enable-mpi-java \
	--enable-static \
	--enable-mpi1-compatibility \
	--with-sge \
	--with-valgrind \
	--enable-memchecker \
	--with-hwloc=/usr \
	--with-libevent=external \
	--with-pmix=external \
	CC=%{opt_cc} CXX=%{opt_cxx} \
	CFLAGS="%{optflags} -fno-strict-aliasing" \
	CXXFLAGS="%{optflags} -fno-strict-aliasing"

%make_build

%install
%make_install
find %{buildroot}%{_libdir}/%{name}/lib -name \*.la | xargs rm
find %{buildroot}%{_mandir}/%{namearch} -type f | xargs gzip -9
ln -s mpicc.1.gz %{buildroot}%{_mandir}/%{namearch}/man1/mpiCC.1.gz
# Remove dangling symlink
rm %{buildroot}%{_mandir}/%{namearch}/man1/mpiCC.1
mkdir %{buildroot}%{_mandir}/%{namearch}/man{2,4,5,6,8,9,n}

# Make the environment-modules file
mkdir -p %{buildroot}%{_datadir}/modulefiles/mpi
# Since we're doing our own substitution here, use our own definitions.
sed 's#@LIBDIR@#%{_libdir}/%{name}#;
     s#@ETCDIR@#%{_sysconfdir}/%{namearch}#;
     s#@FMODDIR@#%{_fmoddir}/%{name}#;
     s#@INCDIR@#%{_includedir}/%{namearch}#;
     s#@MANDIR@#%{_mandir}/%{namearch}#;
     /@PY2SITEARCH@/d;
     s#@PY3SITEARCH@#%{python3_sitearch}/%{name}#;
     s#@COMPILER@#openmpi-%{_arch}%{?_cc_name_suffix}#;
     s#@SUFFIX@#%{?_cc_name_suffix}_openmpi#' \
     <%{SOURCE1} \
     >%{buildroot}%{_datadir}/modulefiles/mpi/%{namearch}

# make the rpm config file
install -Dpm 644 %{SOURCE4} %{buildroot}/%{macrosdir}/macros.%{namearch}

# Link the fortran module to proper location
mkdir -p %{buildroot}%{_fmoddir}/%{name}
for mod in %{buildroot}%{_libdir}/%{name}/lib/*.mod
do
  modname=$(basename $mod)
  ln -s ../../../%{name}/lib/${modname} %{buildroot}/%{_fmoddir}/%{name}/
done

# Link the pkgconfig files into the main namespace as well
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cd %{buildroot}%{_libdir}/pkgconfig
ln -s ../%{name}/lib/pkgconfig/*.pc .
cd -

# Remove extraneous wrapper link libraries (bug 814798)
sed -i -e s/-ldl// -e s/-lhwloc// \
  %{buildroot}%{_libdir}/%{name}/share/openmpi/*-wrapper-data.txt

mkdir -p %{buildroot}/%{python3_sitearch}/%{name}
install -pDm0644 %{SOURCE3} %{buildroot}/%{python3_sitearch}/openmpi.pth

%files
%license LICENSE
%dir %{_libdir}/%{name}
%dir %{_sysconfdir}/%{namearch}
%dir %{_libdir}/%{name}/bin
%dir %{_libdir}/%{name}/lib
%dir %{_libdir}/%{name}/lib/openmpi
%dir %{_mandir}/%{namearch}
%dir %{_mandir}/%{namearch}/man*
%config(noreplace) %{_sysconfdir}/%{namearch}/*
%{_libdir}/%{name}/bin/mpi[er]*
%{_libdir}/%{name}/bin/ompi*
%{_libdir}/%{name}/bin/orte[-dr_]*
%if %{with ucx}
%{_libdir}/%{name}/bin/oshmem_info
%{_libdir}/%{name}/bin/oshrun
%{_libdir}/%{name}/bin/shmemrun
%endif
%{_libdir}/%{name}/share/pmix/
%{_mandir}/%{namearch}/man1/mpi[er]*
%{_mandir}/%{namearch}/man1/ompi*
%{_mandir}/%{namearch}/man1/orte[-dr_]*
%if %{with ucx}
%{_mandir}/%{namearch}/man1/oshmem_info*
%{_mandir}/%{namearch}/man1/oshrun*
%{_mandir}/%{namearch}/man1/shmemrun*
%endif
%{_mandir}/%{namearch}/man7/ompi_*
%{_mandir}/%{namearch}/man7/opal_*
%{_mandir}/%{namearch}/man7/orte*
%{_libdir}/%{name}/lib/openmpi/*
%{_datadir}/modulefiles/mpi/
%dir %{_libdir}/%{name}/share
%dir %{_libdir}/%{name}/share/openmpi
%{_libdir}/%{name}/share/openmpi/amca-param-sets
%{_libdir}/%{name}/share/openmpi/help*.txt
%if %{with rdma}
%{_libdir}/%{name}/share/openmpi/mca-btl-openib-device-params.ini
%endif

#may be splitted at some point
%files -n %{libname} 
%{_libdir}/%{name}/lib/libmpi.so.%{major}{,.*}
%{_libdir}/%{name}/lib/libmpi_cxx.so.%{cxx_major}{,.*}
%{_libdir}/%{name}/lib/libmpi_usempif08.so.%{usempif08_major}{,.*}
%{_libdir}/%{name}/lib/libmpi_usempi_ignore*.so.%{usempi_ignore_major}{,.*}
%{_libdir}/%{name}/lib/libmpi_mpifh*.so.%{mpifh_major}{,.*}
%{_libdir}/%{name}/lib/libompitrace*.so.%{ompitrace_major}{,.*}
%{_libdir}/%{name}/lib/libopen-pal*.so.%{openpal_major}{,.*}
%{_libdir}/%{name}/lib/libopen-rte*.so.%{openrte_major}{,.*}
%ifarch %ix86 %{x86_64} aarch64
%{_libdir}/%{name}/lib/libmpi_java.so.%{major}*
%endif

%files -n %{develname}
%dir %{_includedir}/%{namearch}
#{_libdir}/%{name}/bin/aggregate_profile.pl
#{_libdir}/%{name}/bin/profile2mat.pl
%{_libdir}/%{name}/bin/mpi[cCf]*
%{_libdir}/%{name}/bin/opal_*
%{_libdir}/%{name}/bin/orte[cCf]*
%if %{with ucx}
%{_libdir}/%{name}/bin/osh[cCf]*
%endif
%if %{with ucx}
%{_libdir}/%{name}/bin/shmem[cCf]*
%endif
%{_includedir}/%{namearch}/*
%{_fmoddir}/%{name}/
%{_libdir}/%{name}/lib/*.so
%{_libdir}/%{name}/lib/*.mod
%{_libdir}/%{name}/lib/pkgconfig/
%{_libdir}/pkgconfig/*.pc
%{_mandir}/%{namearch}/man1/mpi[cCf]*
%if %{with ucx}
%{_mandir}/%{namearch}/man1/osh[cCf]*
%{_mandir}/%{namearch}/man1/shmem[cCf]*
%endif
%{_mandir}/%{namearch}/man1/opal_*
%{_mandir}/%{namearch}/man3/*
%{_libdir}/%{name}/share/openmpi/openmpi-valgrind.supp
%{_libdir}/%{name}/share/openmpi/*-wrapper-data.txt
%{macrosdir}/macros.%{namearch}

%files -n %{staticdevelname}
%{_libdir}/%{name}/lib/*.a
%{_libdir}/%{name}/lib/%{name}/*.a

%files java
%{_libdir}/%{name}/lib/mpi.jar

%files java-devel
%{_libdir}/%{name}/bin/mpijavac
%{_libdir}/%{name}/bin/mpijavac.pl
# Currently this only contaings openmpi/javadoc
%{_libdir}/%{name}/share/doc/
%{_mandir}/%{namearch}/man1/mpijavac.1.*

%files -n python-openmpi
%dir %{python3_sitearch}/%{name}
%{python3_sitearch}/openmpi.pth

