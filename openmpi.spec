%define oldmajor 1
%define major	 0
%define libname  %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary: 	A powerful implementation of MPI
Name:		openmpi
Version: 	1.4.3
Release: 	%mkrel 1
License: 	BSD
Group: 		Development/Other
Source0: 	http://www.open-mpi.org/software/ompi/v1.4/downloads/openmpi-%{version}.tar.bz2
Patch0:		format_string.patch
Url: 		http://www.open-mpi.org
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root
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
Obsoletes:	%{mklibname %name 1.2} < 1.4.3

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
Conflicts:	lam-devel, mpich1-devel, mpich2-devel
Obsoletes:	%{mklibname -d %name 1.2} < 1.4.3

%description -n %{develname}
OpenMPI is a project combining technologies and resources from
several other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in
order to build the best MPI library available.

This package contains the libraries and header files needed to
compile applications against OpenMPI.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0 

%build

# Disable libtoolize because it messes up the generated libtool
# in OpenMPI 1.2:
%define __libtoolize /bin/true
%define _disable_ld_no_undefined 1
%configure2_5x --enable-shared --enable-static --with-threads=posix --with-tm
%make

%install
%__rm -rf %{buildroot}
%makeinstall_std
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
%{_datadir}/vtcxx-wrapper-data.txt
%{_datadir}/vtf77-wrapper-data.txt
%{_datadir}/vtf90-wrapper-data.txt
%dir %{_datadir}/vampirtrace
%dir %{_datadir}/vampirtrace/doc
%{_datadir}/vampirtrace/doc/ChangeLog
%{_datadir}/vampirtrace/doc/LICENSE
%{_datadir}/vampirtrace/doc/UserManual.html
%{_datadir}/vampirtrace/doc/UserManual.pdf
%{_datadir}/vampirtrace/doc/opari/ChangeLog
%{_datadir}/vampirtrace/doc/opari/LICENSE
%{_datadir}/vampirtrace/doc/opari/Readme.html
%{_datadir}/vampirtrace/doc/opari/lacsi01.pdf
#%{_datadir}/vampirtrace/doc/opari/lacsi01.ps.gz
%{_datadir}/vampirtrace/doc/opari/opari-logo-100.gif
%{_datadir}/vampirtrace/doc/otf/ChangeLog
%{_datadir}/vampirtrace/doc/otf/LICENSE
%{_datadir}/vampirtrace/doc/otf/otftools.pdf
%{_datadir}/vampirtrace/doc/otf/specification.pdf

%files -n %{libname} 
%defattr(-, root, root, -)
%{_libdir}/*.so.%{major}*
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
%{_mandir}/man7/*
