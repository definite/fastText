%define _epel   %{?epel:%{epel}}%{!?epel:0}

Name:       fasttext
Version:    0.9.2
Release:    3%{?dist}
Summary:    Efficient learning of word representations and sentence classification

License:    MIT
URL:        https://github.com/facebookresearch/fastText
Source0:    https://github.com/facebookresearch/fastText/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:    https://fasttext.cc/docs/en/language-identification.html
Source2:    https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
Source3:    https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz
# Enable to install %%{_libdir} instead of hardcoded lib directory
Patch0:     enable-install-lib64.patch
# Respect CMake CXXFLAGS set by %%cmake (Needed for hardening with -fPIC)
Patch1:     respect-cmake-cxxflags.patch
Patch2:     uint64_t-and-sign.patch

BuildRequires:    cmake
%if %{_epel} == 7
BuildRequires:    devtoolset-7-gcc
BuildRequires:    devtoolset-7-gcc-c++
%else
BuildRequires:    gcc
BuildRequires:    gcc-c++
%endif
Requires:   %{name}-libs = %{version}-%{release}

%description
The fastText is a library for efficient learning of
word representations and sentence classification.

%package libs
Summary:    Runtime libraries for fastText

%description libs
This package contains the libraries for fastText.

%package model-lid-176-bin
Summary:    Language model lid.176.bin from fasttext.cc
Requires:   %{name} = %{version}-%{release}
License:    CC-BY-SA-3.0
BuildArch:  noarch

%description model-lid-176-bin
Contains a Language model, lid.176.bin, which is faster and slightly more
accurate, but has a file size of 126MB.

%package model-lid-176-ftz
Summary:    Language model lid.176.ftz from fasttext.cc
Requires:   %{name} = %{version}-%{release}
License:    CC-BY-SA-3.0
BuildArch:  noarch

%description model-lid-176-ftz
Contains a Language model, lid.176.ftz, which is the compressed version 
of the model, with a file size of 917kB.

%package devel
Summary:    Libraries and header files for fastText
Requires:    %{name}-libs = %{version}-%{release}

%description devel
This package contains header files to develop a software using fastText.

%package -n python3-%{name}
BuildRequires:    python3-devel
## f44 does not seem to include pybind11
BuildRequires:    pybind11-devel
BuildRequires:    python3-pybind11
Summary:    fasttext Python3 module

%description -n python3-%{name}
fastText python3 provides python binding for efficient learning of
word representations and sentence classification.


%prep
%autosetup -p1 -n fastText-%{version}
cp -p %{SOURCE1} .

%generate_buildrequires
%pyproject_buildrequires

%build
%if %{_epel} == 7
. /opt/rh/devtoolset-7/enable
%endif
export CXXFLAGS="%build_cxxflags -fPIC"
%cmake .
V=1 %cmake_build

%pyproject_wheel

%install
%cmake_install
find %{buildroot}%{_libdir} -name '*.a' -delete

%pyproject_install
%pyproject_save_files -l %{name}

mkdir -p %{buildroot}/%{_datadir}/%{name}/
cp %{SOURCE2} %{buildroot}/%{_datadir}/%{name}/
cp %{SOURCE3} %{buildroot}/%{_datadir}/%{name}/

%files
%doc README.md
%{_bindir}/fasttext

%ldconfig_scriptlets libs

%files libs
%license LICENSE
%doc CODE_OF_CONDUCT.md CONTRIBUTING.md README.md
%{_libdir}/libfasttext.so.0

%files  model-lid-176-bin
%doc   language-identification.html
%{_datadir}/%{name}/lid.176.bin

%files  model-lid-176-ftz
%doc   language-identification.html
%{_datadir}/%{name}/lid.176.ftz

%files devel
%{_includedir}/%{name}/
%{_libdir}/libfasttext.so
%{_libdir}/pkgconfig/fasttext.pc

%files -n python3-%{name} -f %{pyproject_files}
%{python3_sitearch}/%{name}_*.so

%changelog
* Mon Oct 20 2025 Ding-Yi Chen <dingyichen@gmail.com> - 0.9.2-3
- Fix the build errors around uint64_t not defined.
- Rename the data subpackage as model-lid-176-bin
- Add model-lid-176-ftz
- Add python3 subpackage

* Tue Oct 07 2025 Ding-Yi Chen <dingyichen@gmail.com> - 0.9.2-2
- Fix the build errors around uint64_t not defined.
- Include a prebuilt model.

* Thu Oct 01 2020 Kentaro Hayashi <kenhys@gmail.com> - 0.9.2-1
- New upstream release

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 1 2019 Kentaro Hayashi <hayashi@clear-code.com> - 0.9.1-1
- initial packaging
