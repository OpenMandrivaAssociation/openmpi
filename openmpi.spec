%define oldmajor 1
%define major	 1
%define libname  %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

# Although CUDA-based code is in the 1.6 source, it doesn't seem 
# configurable yet
%define	cuda	0
%{?_with_cuda: %global %cuda 1}
%{?_without_cuda: %global %cuda 0}

%define	rel	1
Summary: 	A powerful implementation of MPI
Name:		openmpi
Version: 	1.6.2
Release:	%rel
License: 	BSD
Group: 		Development/Other
Source0: 	http://www.open-mpi.org/software/ompi/v1.6/downloads/openmpi-%{version}.tar.bz2
Url: 		http://www.open-mpi.org
Requires:	%{libname} = %{version}, %{develname} = %{version}
BuildRequires:	binutils-devel
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gcc-gfortran
BuildRequires:	libibverbs-devel
BuildRequires:	libgomp-devel
BuildRequires:	numa-devel >= 2.0.2
BuildRequires:	torque-devel >= 2.3.7
BuildRequires:	zlib-devel
%if %cuda
Requires:		nvidia-cuda-toolkit
BuildRequires:	nvidia-cuda-toolkit-devel, nvidia-current-devel
%endif
Conflicts:	mpich, mpich2, lam

%description
OpenMPI is a project combining technologies and resources from
several other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in
order to build the best MPI library available.

This package contains all of the tools necessary to compile, link, and
run OpenMPI jobs.

%package -n %{libname}
Summary:	Shared libraries for OpenMPI
Group:		Development/Other
Provides:	lib%{name} = %{version}-%{release}
Obsoletes:	%{mklibname %name 1.2} < 1.4.3

%description -n %{libname}
OpenMPI is a project combining technologies and resources from
several other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in
order to build the best MPI library available.

This package contains the shared libraries needed by programs linked
against OpenMPI.

%package -n %{develname}
Summary:	Development files for OpenMPI
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel  = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname -d %{name} %{oldmajor}
Conflicts:	lam-devel, mpich1-devel, mpich2-devel
Obsoletes:	%{mklibname -d %name 1.2} < 1.4.3

%description -n %{develname}
OpenMPI is a project combining technologies and resources from
several other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in
order to build the best MPI library available.

This package contains the libraries and header files needed to
compile applications against OpenMPI.

%package -n %{name}-doc
Summary:	Documentation for OpenMPI
Group:		Development/Other
BuildArch:	noarch

%description -n %{name}-doc
OpenMPI is a project combining technologies and resources from
several other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in
order to build the best MPI library available.

This package contains documentation and development man pages 
for OpenMPI.

%prep
%setup -q -n %{name}-%{version}

%build

# Disable libtoolize because it messes up the generated libtool
# in OpenMPI 1.2:
%define __libtoolize /bin/true
%define _disable_ld_no_undefined 1
export CFLAGS='-fPIC'
%configure2_5x --enable-shared --enable-static --with-threads=posix --with-tm
%make

%install
%makeinstall_std
%__rm -rf %{buildroot}%{_libdir}/debug
rm -f %{buildroot}/%{_datadir}/config.log
#rm -f %{buildroot}/%{_datadir}/omp.h
%__rm -f %{buildroot}%{_datadir}/libtool
%__mv %{buildroot}%{_sysconfdir}/openmpi-totalview.tcl %{buildroot}%{_datadir}/openmpi/doc

%files
%doc README LICENSE NEWS AUTHORS examples/
%config(noreplace) %{_sysconfdir}/*
%{_datadir}/openmpi
%{_bindir}/*
%{_mandir}/man1/*
# TODO: these files should be placed in a better place (e.g. in %{_datadir}/openmpi (fix Makefiles?))
%{_datadir}/FILTER.SPEC
%{_datadir}/GROUPS.SPEC
%{_datadir}/METRICS.SPEC
%{_datadir}/vtcc-wrapper-data.txt
%{_datadir}/vtCC-wrapper-data.txt
%{_datadir}/vtcxx-wrapper-data.txt
%{_datadir}/vtc++-wrapper-data.txt
%{_datadir}/vtf77-wrapper-data.txt
%{_datadir}/vtf90-wrapper-data.txt
%{_datadir}/vtfort-wrapper-data.txt
%if %cuda
%{_datadir}/vtnvcc-wrapper-data.txt
%endif

%files -n %{libname} 
%{_libdir}/*.so.*
%{_libdir}/%{name}/*.so

%files -n %{develname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.mod
%{_datadir}/omp.h
%{_libdir}/*.a
%{_libdir}/%{name}/*.a
%{_libdir}/pkgconfig/*.pc

%files -n %{name}-doc
%{_mandir}/man3/*
%{_mandir}/man7/*
%dir %{_datadir}/vampirtrace
%dir %{_datadir}/vampirtrace/doc
%{_datadir}/vampirtrace/doc/*
