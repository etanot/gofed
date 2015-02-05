%global commit		9f2c51e270b93d30b133e7f8bc060719432b3a19
%global shortcommit	%(c=%{commit}; echo ${c:0:7})

Name:		go2fed
Version:	0
Release:	1%{?dist}
Summary:	Tool for development of golang devel packages
License:	GPLv2+
URL:		https://github.com/ingvagabund/GolangPackageGenerator
Source0:	https://github.com/ingvagabund/GolangPackageGenerator/archive/%{commit}/gpg-%{shortcommit}.tar.gz

Requires: python >= 2.7.5, bash, wget, rpmdevtools, rpmlint
Requires: fedpkg, koji, coreutils, rpm-build, openssh-clients, tar
Requires: python-PyGithub, bash-completion

%description
Tool to automize packaging of golang devel source codes.
The main goal is to automatize packaging (spec file generator),
dependency discovering, testing (scratch builds), to prepare package review.
If possible, all in one command.

%prep
%setup -q -n GolangPackageGenerator-%{commit}

%build

%install
# copy bash completition
mkdir -p %{buildroot}/etc/bash_completion.d/
./gen_bash_completion.sh %{name} > %{buildroot}/etc/bash_completion.d/%{name}
# copy man page
mkdir -p %{buildroot}/usr/share/man/man1
cp man/go2fed-help.1 %{buildroot}/usr/share/man/man1/go2fed.1
# copy scripts
mkdir -p %{buildroot}/usr/share/%{name}
cp *.sh %{buildroot}/usr/share/%{name}/.
cp *.py %{buildroot}/usr/share/%{name}/.
# copy config
mkdir -p %{buildroot}/usr/share/%{name}/config
cp config/go2fed.conf %{buildroot}/usr/share/%{name}/config/.
# copy golang list and native imports
cp golang.list golang.imports %{buildroot}/usr/share/%{name}/.
# copy the tool script
cp %{name} %{buildroot}/usr/share/%{name}/.

%post
# make a symlink to go2fed
ln -s /usr/share/%{name}/%{name} /usr/bin/%{name}

%preun
rm /usr/bin/%{name}

%files
%doc README.md LICENSE
%config /usr/share/%{name}/config/go2fed.conf
/etc/bash_completion.d/%{name}
/usr/share/%{name}
/usr/share/man/man1/go2fed.1.gz

%changelog
* Fri Oct 24 2014 jchaloup <jchaloup@redhat.com>
- Initial package


