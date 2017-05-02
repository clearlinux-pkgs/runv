Name     : runv
Version  : 0.5.0
Release  : 4
URL      : https://github.com/hyperhq/runv/archive/v0.5.0.tar.gz
Source0  : https://github.com/hyperhq/runv/archive/v0.5.0.tar.gz
Summary  : runV is a hypervisor-based runtime for OCF.
Group    : Development/Tools
License  : Apache-2.0
BuildRequires : go
BuildRequires : glibc-staticdev

%global gopath /usr/lib/golang
%global library_path github.com/hyperhq/

%description
runV is compatible with OCF. However, due to the difference between hypervisors and containers,
the following sections of OCF do not apply to runV:
  Namespace
  Capability
  Device
  linux and mount fields in OCI specs are ignored

%package dev
Summary: dev components for the runv package.
Group: Development

%description dev
dev components for the runv package.

%prep
%setup -q -n runv-0.5.0

%build
mkdir -p src/%{library_path}/
ln -s $(pwd) src/%{library_path}/runv
./autogen.sh
%configure --without-xen
export GOPATH=$(pwd):%{gopath}
make V=1 %{?_smp_mflags}

%install
rm -rf %{buildroot}
install -d -p %{buildroot}%{_bindir}
install -p -m 755 %{name} %{buildroot}%{_bindir}
# Copy all *.go, *.s and *.proto files
install -d -p %{buildroot}%{gopath}/src/%{library_path}/
for ext in go s proto; do
	for file in $(find . -iname "*.$ext" | grep -v "^./Godeps") ; do
		install -d -p %{buildroot}%{gopath}/src/%{library_path}/$(dirname $file)
		cp -pav $file %{buildroot}%{gopath}/src/%{library_path}/$file
	done
done

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}

%files dev
%defattr(-,root,root,-)
%{gopath}/src/%{library_path}/*
