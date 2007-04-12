%define name 	openmpi
%define version	1.1.4
%define release 1

%define major	1
%define libname %mklibname %{name} %{major}

Summary: 	A powerful implementation of MPI
Name:		%{name}
Version: 	%{version}
Release: 	%mkrel %{release}
License: 	BSD
Group: 		Development/Other
Source: 	http://www.open-mpi.org/software/ompi/v1.1/downloads/openmpi-%{version}.tar.bz2
Url: 		http://www.open-mpi.org
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root
Requires:	%{libname} = %{version}
BuildRequires:	gcc-gfortran
Conflicts:	mpich, mpich2, lam

%description
OpenMPI is a project combining technologies and resources from
several other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in
order to build the best MPI library available.

This package contains all of the tools necessary to compile, link, and run
OpenMPI jobs.

%package -n %{libname}
Summary:	Shared libraries for OpenMPI
Group:		Development/Other
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
OpenMPI is a project combining technologies and resources from
several other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in
order to build the best MPI library available.

This package contains the shared libraries needed by programs linked against
OpenMPI.

%package -n %{libname}-devel
Summary:	Development files for OpenMPI
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel  = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Conflicts:	lam-devel, mpich1-devel, mpich2-devel

%description -n %{libname}-devel
OpenMPI is a project combining technologies and resources from
several other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in
order to build the best MPI library available.

This package contains the static libraries and header files needed to
compile applications against OpenMPI.

%prep
%__rm -rf %{buildroot}
%setup -q -n %{name}-%{version}

%build

%configure
%make

%install
%make install DESTDIR=%{buildroot}
%__rm -rf %{buildroot}%{_libdir}/debug
%__mv %{buildroot}%{_sysconfdir}/openmpi-totalview.tcl %{buildroot}%{_datadir}/openmpi/doc

%clean
%__rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%post -n %{libname}-devel -p /sbin/ldconfig

%postun -n %{libname}-devel -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%doc README INSTALL LICENSE
%{_sysconfdir}/*
%{_datadir}/openmpi
%{_bindir}/ompi_info
%{_bindir}/orted
%{_bindir}/orterun
%{_bindir}/opalCC
%{_bindir}/opalc++
%{_bindir}/opalcc
%{_bindir}/ortec++
%{_bindir}/ortecc
%{_bindir}/orteCC
%{_bindir}/mpirun
%{_bindir}/mpiexec
%{_bindir}/mpicc
%{_bindir}/mpiCC
%{_bindir}/mpic++
%{_bindir}/mpicxx
%{_bindir}/mpif77
%{_bindir}/mpif90
%{_bindir}/opal_wrapper
%{_mandir}/man1/*

%files -n %{libname} 
%defattr(-, root, root, -)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-, root, root, -)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/%{name}/*
%{_libdir}/*.mod


