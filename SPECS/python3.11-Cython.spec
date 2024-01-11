%global __python3 /usr/bin/python3.11
%global python3_pkgversion 3.11

# RHEL: Tests disabled during build due to missing dependencies
%bcond_with tests

# This bcond allows to ship a non-compiled version
# Slower, but sometimes necessary with alpha Python versions
%bcond_without cython_compile

Name:           python%{python3_pkgversion}-Cython
Version:        0.29.32
Release:        2%{?dist}
Summary:        Language for writing Python extension modules

License:        ASL 2.0
URL:            http://www.cython.org
Source:         https://github.com/cython/cython/archive/%{version}/Cython-%{version}.tar.gz

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-rpm-macros
BuildRequires:  python%{python3_pkgversion}-setuptools

%if %{with tests}
BuildRequires:  gcc-c++
BuildRequires:  python%{python3_pkgversion}-numpy
BuildRequires:  python%{python3_pkgversion}-jedi
%endif

%if %{with cython_compile}
BuildRequires:  gcc
%global python3_site %{python3_sitearch}
%else
BuildArch:      noarch
%global python3_site %{python3_sitelib}
%endif

%py_provides    python%{python3_pkgversion}-cython

# A small templating library is bundled in Cython/Tempita
# Upstream version 0.5.2 is available from https://pypi.org/project/Tempita
# but the bundled copy is patched and reorganized.
# Upstream homepage is inaccessible.
Provides:       bundled(python%{python3_pkgversion}dist(tempita))

%global _description %{expand:
The Cython language makes writing C extensions for the Python language as easy
as Python itself. Cython is a source code translator based on Pyrex,
but supports more cutting edge functionality and optimizations.

The Cython language is a superset of the Python language (almost all Python
code is also valid Cython code), but Cython additionally supports optional
static typing to natively call C functions, operate with C++ classes and
declare fast C types on variables and class attributes.
This allows the compiler to generate very efficient C code from Cython code.

This makes Cython the ideal language for writing glue code for external C/C++
libraries, and for fast C modules that speed up the execution of Python code.}

%description %{_description}

%prep
%autosetup -n cython-%{version} -p1


%build
%py3_build -- %{!?with_cython_compile:--no-cython-compile}

%install
%py3_install -- %{!?with_cython_compile:--no-cython-compile}

# Rename unversioned binaries
mv %{buildroot}%{_bindir}/cython{,-%{python3_version}}
mv %{buildroot}%{_bindir}/cygdb{,-%{python3_version}}
mv %{buildroot}%{_bindir}/cythonize{,-%{python3_version}}


%if %{with tests}
%check
%{__python3} runtests.py -vv --no-pyregr %{?_smp_mflags} \
  %ifarch %{ix86}
  --exclude run.parallel  # https://github.com/cython/cython/issues/2807
  %endif

%endif


%files -n python%{python3_pkgversion}-Cython
%license LICENSE.txt
%doc *.txt Demos Doc Tools
%{_bindir}/cython-%{python3_version}
%{_bindir}/cygdb-%{python3_version}
%{_bindir}/cythonize-%{python3_version}
%{python3_site}/Cython-*.egg-info/
%{python3_site}/Cython/
%{python3_site}/pyximport/
%pycached %{python3_site}/cython.py

%changelog
* Mon Feb 13 2023 Charalampos Stratakis <cstratak@redhat.com> - 0.29.32-2
- Bump release for gating

* Thu Oct 20 2022 Charalampos Stratakis <cstratak@redhat.com> - 0.29.32-1
- Initial package
- Fedora contributions by:
      Alex Cobb <alex.cobb@smart.mit.edu>
      Bill Nottingham <notting@fedoraproject.org>
      Charalampos Stratakis <cstratak@redhat.com>
      David Malcolm <dmalcolm@redhat.com>
      Dennis Gilmore <dennis@ausil.us>
      Gwyn Ciesla <gwync@protonmail.com>
      Ignacio Vazquez-Abrams <ivazquez@fedoraproject.org>
      Igor Gnatenko <ignatenkobrain@fedoraproject.org>
      Jesse Keating <jkeating@fedoraproject.org>
      Kevin Fenzi <kevin@fedoraproject.org>
      Marcel Plch <mplch@redhat.com>
      Miro Hrončok <miro@hroncok.cz>
      nbecker <ndbecker2@gmail.com>
      Neal D. Becker <ndbecker2@gmail.com>
      Orion Poplawski <orion@cora.nwra.com>
      Peter Robinson <pbrobinson@fedoraproject.org>
      Petr Viktorin <pviktori@redhat.com>
      Robert Kuska <rkuska@redhat.com>
      Scott Talbert <swt@techie.net>
      serge-sans-paille <sguelton@redhat.com>
      Thomas Spura <thomas.spura@gmail.com>
      Tomáš Hrnčiar <thrnciar@redhat.com>
      Toshio くらとみ <toshio@fedoraproject.org>
