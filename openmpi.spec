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

%define         libname                  %mklibname %{name} %{major}
%define         develname                %mklibname %{name} -d
%define         staticdevelname          %mklibname %{name} -s -d

%define         gccinstalldir   %(LC_ALL=C %__cc --print-search-dirs | %__grep install | %__awk '{print $2}')
%define         fincludedir     %{_libdir}/%{name}


Summary:        An implementation of the Message Passing Interface
Name:           openmpi
Version:        4.0.1
Release:        1
License:        BSD
Group:          Development/Other

URL:            http://www.open-mpi.org
Source0:        http://www.open-mpi.org/software/ompi/v1.10/downloads/openmpi-%{version}.tar.bz2
Patch0:         ompi_autogen_sh.patch
Patch1:         arm_detection.diff
Patch2:         openmpi-1.10.1-fix-function-if.patch
Patch11:        openmpi-3.1.0-addconditional-scmpset-atomic.patch

BuildRequires:  perl
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gawk
BuildRequires:  pkgconfig(pkg-config)
BuildRequires:  gcc-gfortran
%ifarch %ix86 x86_64
BuildRequires:  java-openjdk
BuildRequires:  quadmath-devel
BuildRequires:  librdmacm-devel
%endif
BuildRequires:  gcc-c++
BuildRequires:  binutils-devel
BuildRequires:  libibverbs-devel
BuildRequires:  libgomp-devel
BuildRequires:  torque-devel >= 2.3.7
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



%prep
%setup -q


%build
export CC=%{_bindir}/gcc
export CXX=%{_bindir}/g++
%configure --enable-shared \
	--enable-mpi1-compatibility \
	--enable-static \
	--disable-wrapper-rpath \
	--disable-wrapper-runpath \
	--enable-mpi-cxx \
%ifnarch armv5tl
        --enable-mpi-thread-multiple \
%endif
        --with-tm \
	--with-hwloc=%{_prefix}


%make_build


%install
%make_install

%__rm -rf %{buildroot}%{_sysconfdir}/openmpi-totalview.tcl
%__rm -rf %{buildroot}%{_datadir}/libtool
%__rm -f %{buildroot}%{_datadir}/config.log
%__rm -f %{buildroot}%{_datadir}/omp.h


%__install -D -m 644 %{buildroot}%{_libdir}/mpi.mod %{buildroot}%{fincludedir}/mpi.mod
%__install -D -m 644 %{buildroot}%{_libdir}/mpi_ext.mod %{buildroot}%{fincludedir}/mpi_ext.mod
%__install -D -m 644 %{buildroot}%{_libdir}/mpi_f08.mod %{buildroot}%{fincludedir}/mpi_f08.mod
%__install -D -m 644 %{buildroot}%{_libdir}/mpi_f08_ext.mod %{buildroot}%{fincludedir}/mpi_f08_ext.mod
%__install -D -m 644 %{buildroot}%{_libdir}/mpi_f08_interfaces.mod %{buildroot}%{fincludedir}/mpi_f08_interfaces.mod
%__install -D -m 644 %{buildroot}%{_libdir}/mpi_f08_interfaces_callbacks.mod %{buildroot}%{fincludedir}/mpi_f08_interfaces_callbacks.mod
#__install -D -m 644 %%{buildroot}%%{_libdir}/mpi_f08_sizeof.mod %%{buildroot}%%{fincludedir}/mpi_f08_sizeof.mod
%__install -D -m 644 %{buildroot}%{_libdir}/mpi_f08_types.mod %{buildroot}%{fincludedir}/mpi_f08_types.mod
%__install -D -m 644 %{buildroot}%{_libdir}/pmpi_f08_interfaces.mod %{buildroot}%{fincludedir}/pmpi_f08_interfaces.mod
%__rm %{buildroot}%{_libdir}/*.mod
pushd %{buildroot}%{_libdir}
%__ln_s %{fincludedir}/*.mod  .
popd

find %{buildroot}%{_libdir} -name *.la -delete



%files
%doc README LICENSE NEWS AUTHORS
%config(noreplace) %{_sysconfdir}/*
%{_bindir}/mpirun
%{_bindir}/mpiexec
%{_bindir}/orted
%{_bindir}/orte-*
%{_bindir}/orterun
#{_bindir}/prun
%{_bindir}/ompi-*
#{_bindir}/osh*
#{_bindir}/shmem*
%{_datadir}/%{name}/*.txt
%{_datadir}/%{name}/amca*
%{_datadir}/%{name}/*.supp
%{_datadir}/%{name}/mca*
%{_datadir}/pmix/*.txt
%{_datadir}/pmix/pmix-valgrind.supp
%{_mandir}/man1/mpirun*
%{_mandir}/man1/mpiexec*
%{_mandir}/man1/orte*
#{_mandir}/man1/osh*
#{_mandir}/man1/prun*
#{_mandir}/man1/shmem*
%{_mandir}/man1/ompi-*
%{_mandir}/man7/*


#may be splitted at some point
%files -n %{libname} 
%{_libdir}/libmpi.so.%{major}{,.*}
%{_libdir}/libmpi_cxx.so.%{cxx_major}{,.*}
%{_libdir}/libmpi_usempif08.so.%{usempif08_major}{,.*}
%{_libdir}/libmpi_usempi_ignore*.so.%{usempi_ignore_major}{,.*}
%{_libdir}/libmpi_mpifh*.so.%{mpifh_major}{,.*}
%{_libdir}/libompitrace*.so.%{ompitrace_major}{,.*}
%{_libdir}/libopen-pal*.so.%{openpal_major}{,.*}
%{_libdir}/libopen-rte*.so.%{openrte_major}{,.*}


%files -n %{develname}
%doc examples/
%{_bindir}/mpif*
%{_bindir}/mpic*
%{_bindir}/mpiC*
%{_bindir}/ortec*
%{_bindir}/opal*
%{_bindir}/ompi_*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/%{name}/*.so
%{_libdir}/*.mod
%{fincludedir}/*.mod
%{_libdir}/pkgconfig/*.pc
%{_datadir}/%{name}/mpi*
%{_mandir}/man1/mpif*
%{_mandir}/man1/mpic*
%{_mandir}/man1/mpiC*
%{_mandir}/man1/ompi_*
%{_mandir}/man1/opal_wrapper*
%{_mandir}/man3/*



%files -n %{staticdevelname}
%{_libdir}/*.a
%{_libdir}/%{name}/*.a
