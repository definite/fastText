%define _epel   %{?epel:%{epel}}%{!?epel:0}

Name:       fasttext
Version:    0.9.2
Release:    2%{?dist}
Summary:    Efficient learning of word representations and sentence classification

License:    MIT
URL:        https://github.com/facebookresearch/fastText
Source0:    https://github.com/facebookresearch/fastText/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:    https://fasttext.cc/docs/en/language-identification.html
Source2:    https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
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

%package data
Summary:    Language model lid.176.bin from fasttext.cc
Requires:   %{name} = %{version}-%{release}
License:    CC-BY-SA-3.0
BuildArch:  noarch

%description data
Contains a Language model, lid.176.bin, which is faster and slightly more
accurate, but has a file size of 126MB.

%package devel
Summary:    Libraries and header files for fastText
Requires:    %{name}-libs = %{version}-%{release}

%description devel
This package contains header files to develop a software using fastText.

%prep
%autosetup -p1 -n fastText-%{version}
cp -p %{SOURCE1} .

%build
%if %{_epel} == 7
. /opt/rh/devtoolset-7/enable
%endif
export CXXFLAGS="%build_cxxflags -fPIC"
%cmake .
V=1 %cmake_build

%install
%cmake_install
find %{buildroot}%{_libdir} -name '*.a' -delete

mkdir -p %{buildroot}/%{_datadir}/%{name}/
cp %{SOURCE2} %{buildroot}/%{_datadir}/%{name}/

%files
%{_bindir}/fasttext

%ldconfig_scriptlets libs

%files libs
%license LICENSE
%doc CODE_OF_CONDUCT.md CONTRIBUTING.md README.md
%{_libdir}/libfasttext.so.0

%files data
%doc   language-identification.html
%{_datadir}/%{name}

%files devel
%{_includedir}/%{name}/
%{_libdir}/libfasttext.so
%{_libdir}/pkgconfig/fasttext.pc

%changelog
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
