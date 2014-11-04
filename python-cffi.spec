%define pypi_name cffi
# we don't want to provide private python extension libs
%define _exclude_files_from_autoprov %{python_sitearch}/.*\\.so\\|%{python3_sitearch}/.*\\.so

Name:           python-%{pypi_name}
Version:        0.8.6
Release:        %mkrel 4
Group:          Development/Python
Summary:        Foreign Function Interface for Python calling C code

License:        MIT
URL:            http://cffi.readthedocs.org/
Source0:        https://pypi.python.org/packages/source/c/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
 
BuildRequires:  python-devel
BuildRequires:  python-sphinx
BuildRequires:  python-setuptools
BuildRequires:  libffi-devel
BuildRequires:  python-cython
BuildRequires:  python-pycparser
 
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-cython
BuildRequires:  python3-pycparser
 

%description
Foreign Function Interface for Python calling C code.
The aim of this project is to provide a convenient and 
reliable way of calling C code from Python. 
The interface is based on LuaJIT’s FFI 

%package -n     python3-%{pypi_name}
Summary:        Foreign Function Interface for Python calling C code
 

%description -n python3-%{pypi_name}
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
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd

CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
pushd doc
make html
rm build/html/.buildinfo
popd



%install
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd

%{__python} setup.py install --skip-build --root %{buildroot}


%files
%{python_sitearch}/%{pypi_name}
%{python_sitearch}/%{pypi_name}-%{version}-py?.?.egg-info
%{python_sitearch}/*.so


%files -n python3-%{pypi_name}
%{python3_sitearch}/%{pypi_name}
%{python3_sitearch}/%{pypi_name}-%{version}-py?.?.egg-info
%{python3_sitearch}/*.so

%files doc
%doc doc/build/html



%changelog
* Wed Oct 15 2014 umeabot <umeabot> 0.8.6-4.mga5
+ Revision: 739808
- Second Mageia 5 Mass Rebuild

* Sat Sep 27 2014 tv <tv> 0.8.6-3.mga5
+ Revision: 728178
- rebuild for missing pythoneggs deps

  + umeabot <umeabot>
    - Mageia 5 Mass Rebuild

* Mon Aug 11 2014 philippem <philippem> 0.8.6-1.mga5
+ Revision: 661684
- update to 0.8.6

* Sat May 31 2014 pterjan <pterjan> 0.8.1-3.mga5
+ Revision: 629733
- Rebuild for new Python

* Sat May 31 2014 pterjan <pterjan> 0.8.1-2.mga5
+ Revision: 628495
- Rebuild for new Python

* Wed Mar 05 2014 philippem <philippem> 0.8.1-1.mga5
+ Revision: 600060
- Update to 0.8.1

* Tue Oct 22 2013 umeabot <umeabot> 0.7.2-3.mga4
+ Revision: 543234
- Mageia 4 Mass Rebuild

* Tue Oct 15 2013 pterjan <pterjan> 0.7.2-2.mga4
+ Revision: 498217
- Rebuild to add different pythonegg provides for python 2 and 3

* Mon Oct 07 2013 philippem <philippem> 0.7.2-1.mga4
+ Revision: 492705
- imported package python-cffi

