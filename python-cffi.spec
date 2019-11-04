%define pypi_name cffi
%define _disable_lto 1
%define _disable_ld_as_needed 1

# we don't want to provide private python extension libs
%global __provides_exclude_from ^(%{python2_sitearch}|%{python_sitearch})/.*\\.so$

Name:		python-%{pypi_name}
Version:	1.13.2
Release:	1
Group:		Development/Python
Summary:	Foreign Function Interface for Python calling C code

License:	MIT
URL:		http://cffi.readthedocs.org/
Source0:	https://files.pythonhosted.org/packages/2d/bf/960e5a422db3ac1a5e612cb35ca436c3fc985ed4b7ed13a1b4879006f450/cffi-1.13.2.tar.gz
Source100:	%{name}.rpmlintrc

Patch0:		cffi-1.11.5-link-libdl.patch

BuildRequires:	python-sphinx
BuildRequires:	pkgconfig(libffi)

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
%autosetup -p1 -n %{pypi_name}-%{version}

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

cp -a . %{py2dir}
find %{py2dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'

%build
#export CC=gcc
#export CXX=g++

pushd %{py2dir}
CFLAGS="%{optflags}" LDFLAGS="%{optflags}" %{__python2} setup.py build
popd

CFLAGS="%{optflags}" LDFLAGS="%{optflags}" %{__python} setup.py build

cd doc
make html
rm build/html/.buildinfo
cd -
%install
pushd %{py2dir}
CFLAGS="%{optflags}" LDFLAGS="%{optflags}" %{__python2} setup.py install --skip-build --root %{buildroot}
popd

CFLAGS="%{optflags}" LDFLAGS="%{optflags}" %{__python} setup.py install --skip-build --root %{buildroot}

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
