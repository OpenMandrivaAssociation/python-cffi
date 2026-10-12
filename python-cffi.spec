%define pypi_name cffi
%bcond_with test
%bcond_with docs

# we don't want to provide private python extension libs
%global __provides_exclude_from ^%{python_sitearch}/.*\\.so$

Name:		python-%{pypi_name}
Version:	2.1.1
Release:	2
Group:		Development/Python
Summary:	Foreign Function Interface for Python calling C code
License:	MIT
URL:		https://cffi.readthedocs.org/
Source0:	https://files.pythonhosted.org/packages/source/c/cffi/%{pypi_name}-%{version}.tar.gz
Source100:	%{name}.rpmlintrc

%if %{with docs}
BuildRequires:	make
BuildRequires:	python%{pyver}dist(sphinx)
%endif
BuildRequires:	pkgconfig(libffi)
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(cython)
BuildRequires:  python%{pyver}dist(pycparser)
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

%if %{with docs}
%package doc
Summary:	Documentation for CFFI
Group:		Development/Python
BuildArch:	noarch

%description doc
Documentation for CFFI, the Foreign Function Interface for Python.
%endif

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py_build

%if %{with docs}
cd doc
make html
rm build/html/.buildinfo
cd -
%endif

%install
%py_install

%if %{with test}
%check
python setup.py test
%endif

%files
%{_bindir}/%{pypi_name}-gen-src
%{python_sitearch}/%{pypi_name}
%{python_sitearch}/%{pypi_name}-%{version}*.*-info
%{python_sitearch}/*.so

%if %{with docs}
%files doc
%doc doc/build/html
%endif
