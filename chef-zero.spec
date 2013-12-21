#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Self-contained, easy-setup, fast-start in-memory Chef server for testing and solo setup purposes
Name:		chef-zero
Version:	1.7.2
Release:	0.1
License:	Apache v2.0
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{name}-%{version}.gem
# Source0-md5:	884fb6ca2e75ae515ffec97f1fc77793
URL:		https://github.com/opscode/chef-zero
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
BuildRequires:	sed >= 4.0
%if %{with tests}
BuildRequires:	ruby-rake
BuildRequires:	ruby-rspec
%endif
Requires:	ruby-hashie < 3
Requires:	ruby-hashie >= 2.0
Requires:	ruby-json
Requires:	ruby-mixlib-log < 2
Requires:	ruby-mixlib-log >= 1.3
Requires:	ruby-moneta < 0.7.0
Requires:	ruby-rack
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Self-contained, easy-setup, fast-start in-memory Chef server for
testing and solo setup purposes.

%prep
%setup -q
%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*

%build
# write .gemspec
%__gem_helper spec

%if %{with tests}
rspec
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{_bindir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}

# install gemspec
install -d $RPM_BUILD_ROOT%{ruby_specdir}
cp -p %{name}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/chef-zero
%{ruby_vendorlibdir}/chef_zero.rb
%{ruby_vendorlibdir}/chef_zero
%{ruby_specdir}/%{name}-%{version}.gemspec
