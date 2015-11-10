# Cannot build doc as of this moment. Construction requires unpackaged python2
# only deps.
%global with_doc 0
%global pypi_name autobahn
%global project_owner tavendo
%global github_name AutobahnPython
%global commit a69e7048b86643644a1d8b68dfeec97f9162a4cd
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global _docdir_fmt %{name}

Name:           python-%{pypi_name}
Version:        0.10.7
Release:        2.git%{shortcommit}%{?dist}
Summary:        Python networking library for WebSocket and WAMP

License:        MIT
URL:            https://pypi.python.org/pypi/%{pypi_name}
# pypi release doen't include README, nor doc, so using github instead
# See: https://github.com/tavendo/AutobahnPython/issues/429
Source0:        https://github.com/%{project_owner}/%{github_name}/archive/%{commit}/%{github_name}-%{commit}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-pep8
BuildRequires:  python-flake8
BuildRequires:  python-mock >= 1.0.1
BuildRequires:  pytest >= 2.6.4
BuildRequires:  python-six
BuildRequires:  python2-txaio
BuildRequires:  python-trollius
BuildRequires:  python-unittest2
%if 0%{with_doc}
BuildRequires:  python-scour # No python 3, https://github.com/oberstet/scour/issues/4
BuildRequires:  scons
BuildRequires:  python-taschenmesser # No python 3, https://github.com/oberstet/taschenmesser/issues/3
BuildRequires:  python-sphinx
BuildRequires:  python-sphinx-theme-bootstrap # Not packaged yet
BuildRequires:  python-sphinxcontrib-spelling # Not packaged yet
BuildRequires:  python-repoze-sphinx-autointerface
BuildRequires:  python-pyenchant
%endif # End with_doc

%description
Autobahn a networking library that is part of the Autobahn project and provides
implementations of
* The WebSocket Protocol http://tools.ietf.org/html/rfc6455_
* The Web Application Messaging Protocol (WAMP) http://wamp.ws
for Twisted and asyncio on Python 2 & 3 and for writing servers and clients.


%package -n     python2-%{pypi_name}
Requires:       python-twisted >= 11.1
Requires:       python-zope-interface >= 3.6
Requires:       python-trollius >= 0.1.2
Requires:       python-futures >= 2.1.5
Requires:       python2-ujson >= 1.33
Requires:       python2-wsaccel >= 0.6.2
Requires:       python-snappy >= 0.5
Requires:       python-lz4 >= 0.2.1
Requires:       python-msgpack >= 0.4.0
Requires:       python-six
Requires:       python2-txaio
Summary:        Python networking library for WebSocket and WAMP
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
Autobahn a networking library that is part of the Autobahn project and provides
implementations of
* The WebSocket Protocol http://tools.ietf.org/html/rfc6455_
* The Web Application Messaging Protocol (WAMP) http://wamp.ws
for Twisted and asyncio on Python 2 & 3 and for writing servers and clients.


%package -n     python3-%{pypi_name}
Summary:        Python networking library for WebSocket and WAMP
BuildArch:      noarch
BuildRequires:  python3-devel >= 3.4
BuildRequires:  python3-pep8
BuildRequires:  python3-flake8
BuildRequires:  python3-mock >= 1.0.1
BuildRequires:  python3-pytest >= 2.6.4
BuildRequires:  python3-six
BuildRequires:  python3-txaio
BuildRequires:  python3-unittest2
Requires:       python3-zope-interface >= 3.6
Requires:       python3-ujson >= 1.33
Requires:       python3-wsaccel >= 0.6.2
Requires:       python3-snappy >= 0.5
Requires:       python3-lz4 >= 0.2.1
Requires:       python3-msgpack >= 0.4.0
Requires:       python3-six
Requires:       python3-txaio
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
Autobahn a networking library that is part of the Autobahn project and provides
implementations of
* The WebSocket Protocol http://tools.ietf.org/html/rfc6455_
* The Web Application Messaging Protocol (WAMP) http://wamp.ws
for Twisted and asyncio on Python 2 & 3 and for writing servers and clients.


%if 0%{with_doc}
%package doc
Summary:        Python networking library for WebSocket and WAMP

%description doc
Autobahn a networking library that is part of the Autobahn project and provides
implementations of
* The WebSocket Protocol http://tools.ietf.org/html/rfc6455_
* The Web Application Messaging Protocol (WAMP) http://wamp.ws
for Twisted and asyncio on Python 2 & 3 and for writing servers and clients.

HTML documentation
%endif # with doc


%prep
%setup -qn %{github_name}-%{commit}

# Remove upstream's egg-info
rm -rf %{pypi_name}.egg-info


%build
%py2_build
%py3_build

%if 0%{with_doc}
# Build doc
cd doc && make build_no_network
%endif


%install
%py2_install
%py3_install


%check
py.test-%{python3_version} --pyargs autobahn
py.test-%{python2_version} --pyargs autobahn


%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst DEVELOPERS.md
%{python2_sitelib}/%{pypi_name}-%{version}*-py%{python2_version}.egg-info/
%{python2_sitelib}/%{pypi_name}/
%dir %{python2_sitelib}/twisted
%dir %{python2_sitelib}/twisted/plugins
%{python2_sitelib}/twisted/plugins/autobahn*.py*

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst DEVELOPERS.md
%{python3_sitelib}/%{pypi_name}-%{version}*-py%{python3_version}.egg-info/
%{python3_sitelib}/%{pypi_name}/
%dir %{python3_sitelib}/twisted
%dir %{python3_sitelib}/twisted/plugins
%dir %{python3_sitelib}/twisted/plugins/__pycache__
%{python3_sitelib}/twisted/plugins/autobahn*.py
%{python3_sitelib}/twisted/plugins/__pycache__/autobahn*.py*

%if 0%{with_doc}
%files doc
%license LICENSE
%doc doc/_build
%endif


%changelog
* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.7-2.gita69e704
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sun Sep 6 2015 Julien Enselme <jujens@jujens.eu> - 0.10.7-1.gita69e7048
- Update to 0.10.7

* Sun Sep 6 2015 Julien Enselme <jujens@jujens.eu> - 0.10.6-1.gitb35d99f1
- Update to 0.10.6

* Sat Aug 15 2015 Julien Enselme <jujens@jujens.eu> - 0.10.5-1.git3fce8ac
- Update to 0.10.5.post-2

* Wed Aug 5 2015 Julien Enselme <jujens@jujens.eu> - 0.10.4-3.git29f8acc
- Build python2 and python3 in the same dir
- Update dependencies
- Put python2 package in a subpackage
- Add provides
- Correct %%files section

* Fri Jul 24 2015 Julien Enselme <jujens@jujens.eu> - 0.10.4-2.git29f8acc
- Surround doc package with if
- Remove %%py3dir macro
- Add CFLAGS in %%build

* Sat Jul 18 2015 Julien Enselme <jujens@jujens.eu> - 0.10.4-1.git29f8acc
- Initial packaging
