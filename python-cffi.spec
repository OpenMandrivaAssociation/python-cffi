%define pypi_name cffi
%define _disable_lto 1
%define _disable_ld_as_needed 1

# we don't want to provide private python extension libs
%define _exclude_files_from_autoprov %{python2_sitearch}/.*\\.so\\|%{python3_sitearch}/.*\\.so

Name:		python-%{pypi_name}
Version:	1.11.5
Release:	1
Group:		Development/Python
Summary:	Foreign Function Interface for Python calling C code

License:	MIT
URL:		http://cffi.readthedocs.org/
Source0:	https://pypi.python.org/packages/10/f7/3b302ff34045f25065091d40e074479d6893882faef135c96f181a57ed06/cffi-%{version}.tar.gz
Source100:	%{name}.rpmlintrc
BuildRequires:	python-sphinx
BuildRequires:	ffi-devel

BuildRequires:	pkgconfig(python2)
BuildRequires:	python2-setuptools
BuildRequires:	python2-pkg-resources
BuildRequires:	python2-cython
BuildRequires:	python2-cparser

BuildRequires:	pkgconfig(python3)
BuildRequires:	python-setuptools
BuildRequires:	python-pkg-resources
BuildRequires:	python-cython
BuildRequires:	python-cparser

%description
Foreign Function Interface for Python calling C code.
The aim of this project is to provide a convenient and 
reliable way of calling C code from Python. 
The interface is based on LuaJIT’s FFI 

%package -n python2-%{pypi_name}
Summary:	Foreign Function Interface for Python calling C code

%description -n python2-%{pypi_name}
Foreign Function Interface for Python 3 calling C code.
The aim of this project is to provide a convenient and 
reliable way of calling C code from Python 3. 
The interface is based on LuaJIT’s FFI 

%package doc
Summary:	Documentation for CFFI
Group:		Development/Python
BuildArch:	noarch

%description doc
Documentation for CFFI, the Foreign Function Interface for Python.

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

cp -a . %{py2dir}
find %{py2dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'

%build
export CC=gcc
export CXX=g++

pushd %{py2dir}
CFLAGS="%{optflags}" %{__python2} setup.py build build_ext --libraries="dl"
CFLAGS="%{optflags}" %{__python2} setup.py build
popd

CFLAGS="%{optflags}" %{__python} setup.py build build_ext --libraries="dl"
CFLAGS="%{optflags}" %{__python} setup.py build

pushd doc
make html
rm build/html/.buildinfo
popd

%install
pushd %{py2dir}
%{__python2} setup.py install --skip-build --root %{buildroot}
popd

%{__python} setup.py install --skip-build --root %{buildroot}

%files
%{python_sitearch}/%{pypi_name}
%{python_sitearch}/%{pypi_name}-%{version}-py?.?.egg-info
%{python_sitearch}/*.so

%files -n python2-%{pypi_name}
%{python2_sitearch}/%{pypi_name}
%{python2_sitearch}/%{pypi_name}-%{version}-py?.?.egg-info
%{python2_sitearch}/*.so

%files doc
%doc doc/build/html
