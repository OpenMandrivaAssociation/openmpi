%define name	 openmpi
%define version	 1.2.6
%define release  1

%define oldmajor 1
%define major	 1.2
%define libname  %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary: 	A powerful implementation of MPI
Name:		%{name}
Version: 	%{version}
Release: 	%mkrel %{release}
License: 	BSD
Group: 		Development/Other
Source: 	http://www.open-mpi.org/software/ompi/v%{major}/downloads/openmpi-%{version}.tar.bz2
Url: 		http://www.open-mpi.org
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root
Requires:	%{libname} = %{version}, %{develname} = %{version}
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
Obsoletes:	%mklibname %{name} %{oldmajor}

%description -n %{libname}
OpenMPI is a project combining technologies and resources from
several other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in
order to build the best MPI library available.

This package contains the shared libraries needed by programs linked against
OpenMPI.

%package -n %{develname}
Summary:	Development files for OpenMPI
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel  = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname -d %{name} %{oldmajor}
Obsoletes:	%mklibname -d %{name} %{major}
Conflicts:	lam-devel, mpich1-devel, mpich2-devel

%description -n %{develname}
OpenMPI is a project combining technologies and resources from
several other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in
order to build the best MPI library available.

This package contains the libraries and header files needed to
compile applications against OpenMPI.

%prep
%__rm -rf %{buildroot}
%setup -q -n %{name}-%{version}

%build

# Disable libtoolize because it messes up the generated libtool
# in OpenMPI 1.2:
%define __libtoolize /bin/true

%configure2_5x --enable-shared --enable-static
%make

%install
%make install DESTDIR=%{buildroot}
%__rm -rf %{buildroot}%{_libdir}/debug
%__mv %{buildroot}%{_sysconfdir}/openmpi-totalview.tcl %{buildroot}%{_datadir}/openmpi/doc

%clean
%__rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(-, root, root, -)
%doc README INSTALL LICENSE NEWS LICENSE AUTHORS examples/
%{_sysconfdir}/*
%{_datadir}/openmpi
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{libname} 
%defattr(-, root, root, -)
%{_libdir}/*.so.*
%{_libdir}/%{name}/*.so

%files -n %{develname}
%defattr(-, root, root, -)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/*.mod
%{_libdir}/%{name}/*.la
%{_libdir}/*.a
%{_libdir}/%{name}/*.a
%{_mandir}/man3/*
