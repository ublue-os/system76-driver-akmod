%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%global tag master
%global ref heads
%endif

Name:     system76-driver-kmod
Version:  {{{ git_dir_version }}}
Release:  1%{?dist}
Summary:  akmod module for System76 laptops
License:  GPLv2
URL:      https://github.com/pop-os/system76-dkms

Source:   %{url}/archive/refs/%{ref}/%{tag}.tar.gz

BuildRequires: kmodtool

%description
Kernel module for controlling the hotkeys and fans on some System76 laptops.

%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%prep
%setup -c system76-dkms-${tag}

for kernel_version  in %{?kernel_versions} ; do
  mkdir -p _kmod_build_${kernel_version%%___*}
  cp -a system76-dkms-master/src system76-dkms-master/Kbuild system76-dkms-master/Makefile _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version  in %{?kernel_versions} ; do
  make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} VERSION=v%{version} modules
done

%install
for kernel_version in %{?kernel_versions}; do
 mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 install -D -m 755 _kmod_build_${kernel_version%%___*}/src/system76.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/system76.ko
done
%{?akmod_install}

install -D -m 0644 system76-dkms-master/lib/udev/hwdb.d/99-system76-dkms.hwdb %{buildroot}%{_libdir}/udev/hwdb.d/99-system76.hwdb

%files
%{_libdir}/udev/hwdb.d/99-system76.hwdb

%changelog
{{{ git_dir_changelog }}}
