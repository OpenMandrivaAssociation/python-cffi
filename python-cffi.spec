%define pypi_name cffi
# we don't want to provide private python extension libs
%define _exclude_files_from_autoprov %{python_sitearch}/.*\\.so\\|%{python3_sitearch}/.*\\.so
%define py3dir py3

Name:           python-%{pypi_name}
Version:        0.8.6
Release:        1
Group:          Development/Python
Summary:        Foreign Function Interface for Python calling C code

License:        MIT
URL:            http://cffi.readthedocs.org/
Source0:        https://pypi.python.org/packages/source/c/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
 
BuildRequires:  python-sphinx
BuildRequires:  ffi-devel

BuildRequires:  pkgconfig(python2)
BuildRequires:  python2-setuptools
BuildRequires:  python2-cython
BuildRequires:  python2-pycparser
 
BuildRequires:  pkgconfig(python3)
BuildRequires:  python-setuptools
BuildRequires:  python-cython
BuildRequires:  python-pycparser
 

%description
Foreign Function Interface for Python calling C code.
The aim of this project is to provide a convenient and 
reliable way of calling C code from Python. 
The interface is based on LuaJIT’s FFI 

%package -n     python2-%{pypi_name}
Summary:        Foreign Function Interface for Python calling C code
 

%description -n python2-%{pypi_name}
Foreign Function Interface for Python 3 calling C code.
The aim of this project is to provide a convenient and 
reliable way of calling C code from Python 3. 
The interface is based on LuaJIT’s FFI 

%package doc
Summary:        Documentation for CFFI
Group:          Development/Python
BuildArch:      noarch

%description doc
Documentation for CFFI, the Foreign Function Interface for Python.

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'


%build
pushd %{py3dir}
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
popd

CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build
pushd doc
make html
rm build/html/.buildinfo
popd



%install
pushd %{py3dir}
%{__python} setup.py install --skip-build --root %{buildroot}
popd

%{__python2} setup.py install --skip-build --root %{buildroot}


%files
%{python_sitearch}/%{pypi_name}
%{python_sitearch}/%{pypi_name}-%{version}-py?.?.egg-info
%{python_sitearch}/*.so


%files -n python3-%{pypi_name}
%{python2_sitearch}/%{pypi_name}
%{python2_sitearch}/%{pypi_name}-%{version}-py?.?.egg-info
%{python2_sitearch}/*.so

%files doc
%doc doc/build/html


