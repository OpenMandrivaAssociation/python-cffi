%define pypi_name cffi
%bcond_with test

# we don't want to provide private python extension libs
%global __provides_exclude_from ^%{python_sitearch}/.*\\.so$

Name:		python-%{pypi_name}
Version:	2.0.0
Release:	2
Group:		Development/Python
Summary:	Foreign Function Interface for Python calling C code
License:	MIT
URL:		https://cffi.readthedocs.org/
Source0:	https://files.pythonhosted.org/packages/source/c/cffi/%{pypi_name}-%{version}.tar.gz
Source100:	%{name}.rpmlintrc

BuildRequires:	make
BuildRequires:	python-sphinx
BuildRequires:	pkgconfig(libffi)
BuildRequires:	pkgconfig(python)
BuildRequires:	python-setuptools
BuildRequires:	python-pkg-resources
BuildRequires:	python-cython
BuildRequires:	python-cparser
BuildRequires:	python%{pyver}dist(pip)
%if %{with test}
BuildRequires:	python%{pyver}dist(py)
BuildRequires:	python%{pyver}dist(pytest)
%endif

%description
Foreign Function Interface for Python calling C code.
The aim of this project is to provide a convenient and 
reliable way of calling C code from Python. 
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

%build
%py_build

cd doc
make html
rm build/html/.buildinfo
cd -

%install
%py_install

%if %{with test}
%check
python setup.py test
%endif

%files
%{python_sitearch}/%{pypi_name}
%{python_sitearch}/%{pypi_name}-%{version}*.*-info
%{python_sitearch}/*.so

%files doc
%doc doc/build/html
