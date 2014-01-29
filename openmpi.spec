%define mpi_major 1
%define mpifh_major 2
%define trace_major 0
%define openpal_major 6
%define vt_major 0
%define libmpi %mklibname mpi %{mpi_major}
%define libmpicxx %mklibname mpi_cxx %{mpi_major}
%define libmpifh %mklibname mpi_mpifh %{mpifh_major}
%define libmpiuse %mklibname mpi_usempi %{mpi_major}
%define libtrace %mklibname ompitrace %{trace_major}
%define libopenpal %mklibname open-pal %{openpal_major}
%define libopenrte %mklibname open-rte %{openpal_major}
%define libotf %mklibname open-trace-format %{mpi_major}
%define libotfaux %mklibname otfaux %{trace_major}
%define libvt %mklibname vt %{vt_major}
%define libvthyb %mklibname vt-hyb %{vt_major}
%define libvtmpi %mklibname vt-mpi %{vt_major}
%define libvtmpiunify %mklibname vt-mpi-unify %{vt_major}
%define libvtmt %mklibname vt-mt %{vt_major}
%define devname %mklibname %{name} -d

Summary:	A powerful implementation of MPI
Name:		openmpi
Version:	1.7.3
Release:	1
License:	BSD
Group:		Development/Other
Url:		http://www.open-mpi.org
Source0:	http://www.open-mpi.org/software/ompi/v1.6/downloads/%{name}-%{version}.tar.bz2
Patch0:		openmpi-1.7.3-sfmt.patch
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gcc-gfortran
BuildRequires:	binutils-devel
BuildRequires:	gomp-devel
BuildRequires:	libibverbs-devel
BuildRequires:	numa-devel
BuildRequires:	torque-devel
BuildRequires:	pkgconfig(zlib)
Requires:	%{devname} = %{EVRD}
Conflicts:	mpich
Conflicts:	mpich2
Conflicts:	lam
Conflicts:	%{_lib}openmpi1 < 1.7.5

%description
OpenMPI is a project combining technologies and resources from
several other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in
order to build the best MPI library available.

This package contains all of the tools necessary to compile, link, and
run OpenMPI jobs.

%files
%doc README LICENSE NEWS AUTHORS examples/
%config(noreplace) %{_sysconfdir}/*
%{_bindir}/*
%{_datadir}/%{name}/
%{_mandir}/man1/*
%{_libdir}/%{name}/*.so

#----------------------------------------------------------------------------

%package -n %{libmpi}
Summary:	Shared library for OpenMPI
Group:		System/Libraries
Conflicts:	%{_lib}openmpi1 < 1.7.5
Obsoletes:	%{_lib}openmpi1 < 1.7.5

%description -n %{libmpi}
This package contains shared library needed by programs linked against OpenMPI.

%files -n %{libmpi}
%{_libdir}/libmpi.so.%{mpi_major}*

#----------------------------------------------------------------------------

%package -n %{libmpicxx}
Summary:	Shared library for OpenMPI
Group:		System/Libraries
Conflicts:	%{_lib}openmpi1 < 1.7.5

%description -n %{libmpicxx}
This package contains shared library needed by programs linked against OpenMPI.

%files -n %{libmpicxx}
%{_libdir}/libmpi_cxx.so.%{mpi_major}*

#----------------------------------------------------------------------------

%package -n %{libmpifh}
Summary:	Shared library for OpenMPI
Group:		System/Libraries
Conflicts:	%{_lib}openmpi1 < 1.7.5

%description -n %{libmpifh}
This package contains shared library needed by programs linked against OpenMPI.

%files -n %{libmpifh}
%{_libdir}/libmpi_mpifh.so.%{mpifh_major}*

#----------------------------------------------------------------------------

%package -n %{libmpiuse}
Summary:	Shared library for OpenMPI
Group:		System/Libraries
Conflicts:	%{_lib}openmpi1 < 1.7.5

%description -n %{libmpiuse}
This package contains shared library needed by programs linked against OpenMPI.

%files -n %{libmpiuse}
%{_libdir}/libmpi_usempi.so.%{mpi_major}*

#----------------------------------------------------------------------------

%package -n %{libtrace}
Summary:	Shared library for OpenMPI
Group:		System/Libraries
Conflicts:	%{_lib}openmpi1 < 1.7.5

%description -n %{libtrace}
This package contains shared library needed by programs linked against OpenMPI.

%files -n %{libtrace}
%{_libdir}/libompitrace.so.%{trace_major}*

#----------------------------------------------------------------------------

%package -n %{libopenpal}
Summary:	Shared library for OpenMPI
Group:		System/Libraries
Conflicts:	%{_lib}openmpi1 < 1.7.5

%description -n %{libopenpal}
This package contains shared library needed by programs linked against OpenMPI.

%files -n %{libopenpal}
%{_libdir}/libopen-pal.so.%{openpal_major}*

#----------------------------------------------------------------------------

%package -n %{libopenrte}
Summary:	Shared library for OpenMPI
Group:		System/Libraries
Conflicts:	%{_lib}openmpi1 < 1.7.5

%description -n %{libopenrte}
This package contains shared library needed by programs linked against OpenMPI.

%files -n %{libopenrte}
%{_libdir}/libopen-rte.so.%{openpal_major}*

#----------------------------------------------------------------------------

%package -n %{libotf}
Summary:	Shared library for OpenMPI
Group:		System/Libraries
Conflicts:	%{_lib}openmpi1 < 1.7.5

%description -n %{libotf}
This package contains shared library needed by programs linked against OpenMPI.

%files -n %{libotf}
%{_libdir}/libopen-trace-format.so.%{mpi_major}*

#----------------------------------------------------------------------------

%package -n %{libotfaux}
Summary:	Shared library for OpenMPI
Group:		System/Libraries
Conflicts:	%{_lib}openmpi1 < 1.7.5

%description -n %{libotfaux}
This package contains shared library needed by programs linked against OpenMPI.

%files -n %{libotfaux}
%{_libdir}/libotfaux.so.%{trace_major}*

#----------------------------------------------------------------------------

%package -n %{libvt}
Summary:	Shared library for OpenMPI
Group:		System/Libraries
Conflicts:	%{_lib}openmpi1 < 1.7.5

%description -n %{libvt}
This package contains shared library needed by programs linked against OpenMPI.

%files -n %{libvt}
%{_libdir}/libvt.so.%{vt_major}*

#----------------------------------------------------------------------------

%package -n %{libvthyb}
Summary:	Shared library for OpenMPI
Group:		System/Libraries
Conflicts:	%{_lib}openmpi1 < 1.7.5

%description -n %{libvthyb}
This package contains shared library needed by programs linked against OpenMPI.

%files -n %{libvthyb}
%{_libdir}/libvt-hyb.so.%{vt_major}*

#----------------------------------------------------------------------------

%package -n %{libvtmpi}
Summary:	Shared library for OpenMPI
Group:		System/Libraries
Conflicts:	%{_lib}openmpi1 < 1.7.5

%description -n %{libvtmpi}
This package contains shared library needed by programs linked against OpenMPI.

%files -n %{libvtmpi}
%{_libdir}/libvt-mpi.so.%{vt_major}*

#----------------------------------------------------------------------------

%package -n %{libvtmpiunify}
Summary:	Shared library for OpenMPI
Group:		System/Libraries
Conflicts:	%{_lib}openmpi1 < 1.7.5

%description -n %{libvtmpiunify}
This package contains shared library needed by programs linked against OpenMPI.

%files -n %{libvtmpiunify}
%{_libdir}/libvt-mpi-unify.so.%{vt_major}*

#----------------------------------------------------------------------------

%package -n %{libvtmt}
Summary:	Shared library for OpenMPI
Group:		System/Libraries
Conflicts:	%{_lib}openmpi1 < 1.7.5

%description -n %{libvtmt}
This package contains shared library needed by programs linked against OpenMPI.

%files -n %{libvtmt}
%{_libdir}/libvt-mt.so.%{vt_major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for OpenMPI
Group:		Development/Other
Requires:	%{libmpi} = %{EVRD}
Requires:	%{libmpicxx} = %{EVRD}
Requires:	%{libmpifh} = %{EVRD}
Requires:	%{libmpiuse} = %{EVRD}
Requires:	%{libtrace} = %{EVRD}
Requires:	%{libopenpal} = %{EVRD}
Requires:	%{libopenrte} = %{EVRD}
Requires:	%{libotf} = %{EVRD}
Requires:	%{libotfaux} = %{EVRD}
Requires:	%{libvt} = %{EVRD}
Requires:	%{libvthyb} = %{EVRD}
Requires:	%{libvtmpi} = %{EVRD}
Requires:	%{libvtmpiunify} = %{EVRD}
Requires:	%{libvtmt} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Conflicts:	lam-devel
Conflicts:	mpich1-devel
Conflicts:	mpich2-devel

%description -n %{devname}
OpenMPI is a project combining technologies and resources from
several other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in
order to build the best MPI library available.

This package contains the libraries and header files needed to
compile applications against OpenMPI.

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.mod
%{_libdir}/*.a
%{_libdir}/%{name}/*.a
%{_libdir}/pkgconfig/*.pc
%exclude %{_datadir}/vampirtrace/doc/
%{_datadir}/vampirtrace/

#----------------------------------------------------------------------------

%package doc
Summary:	Documentation for OpenMPI
Group:		Development/Other
BuildArch:	noarch

%description doc
OpenMPI is a project combining technologies and resources from
several other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in
order to build the best MPI library available.

This package contains documentation and development man pages 
for OpenMPI.

%files doc
%{_mandir}/man3/*
%{_mandir}/man7/*
%dir %{_datadir}/vampirtrace/doc
%{_datadir}/vampirtrace/doc/*

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p1

%build
# Disable libtoolize because it messes up the generated libtool
# in OpenMPI 1.2:
%define __libtoolize /bin/true
%define _disable_ld_no_undefined 1
export CFLAGS='-fPIC'
%configure2_5x \
	--enable-shared \
	--enable-static \
	--with-threads=posix \
	--with-tm
%make

%install
%makeinstall_std

mv %{buildroot}%{_sysconfdir}/openmpi-totalview.tcl %{buildroot}%{_datadir}/openmpi/doc

