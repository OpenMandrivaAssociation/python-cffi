%define pypi_name cffi
%define _disable_lto 1
%define _disable_ld_as_needed 1

# we don't want to provide private python extension libs
%global __provides_exclude_from ^(%{python2_sitearch}|%{python_sitearch})/.*\\.so$

Name:		python-%{pypi_name}
Version:	1.14.4
Release:	2
Group:		Development/Python
Summary:	Foreign Function Interface for Python calling C code
License:	MIT
URL:		http://cffi.readthedocs.org/
Source0:	https://files.pythonhosted.org/packages/66/6a/98e023b3d11537a5521902ac6b50db470c826c682be6a8c661549cb7717a/cffi-1.14.4.tar.gz
Source100:	%{name}.rpmlintrc
Patch0:		cffi-1.11.5-link-libdl.patch
BuildRequires:	python-sphinx
BuildRequires:	pkgconfig(libffi)
BuildRequires:	pkgconfig(python)
BuildRequires:	python-setuptools
BuildRequires:	python-pkg-resources
BuildRequires:	python-cython
BuildRequires:	python-cparser

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
%set_build_flags
%py_build

cd doc
make html
rm build/html/.buildinfo
cd -

%install
%py_install

%files
%{python_sitearch}/%{pypi_name}
%{python_sitearch}/%{pypi_name}-%{version}-py*.egg-info
%{python_sitearch}/*.so

%files doc
%doc doc/build/html
