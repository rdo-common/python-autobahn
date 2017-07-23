# Cannot build doc as of this moment. Construction requires unpackaged python2
# only deps.
%global with_doc 0
%global pypi_name autobahn
%global project_owner crossbario
%global github_name autobahn-python
%global commit 9ad7878e0ce2afcd3117aa5059365a74623eadfd
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global _docdir_fmt %{name}

Name:           python-%{pypi_name}
Version:        17.7.1
Release:        1.git%{shortcommit}%{?dist}
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
BuildRequires:  python-mock >= 1.3.0
BuildRequires:  pytest >= 2.6.4
BuildRequires:  python-six >= 1.10.0
BuildRequires:  python2-txaio >= 2.2.1
BuildRequires:  python-trollius >= 2.0
BuildRequires:  python-futures >= 3.0.4
BuildRequires:  python-unittest2 >= 1.1.0
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
Requires:       python-twisted >= 15.5
Requires:       python-zope-interface >= 4.1.3
Requires:       python-trollius >= 2.0
Requires:       python-futures >= 3.0.4
Requires:       python2-ujson >= 1.33
Requires:       python2-wsaccel >= 0.6.2
Requires:       python-snappy >= 0.5
Requires:       python-lz4 >= 0.7.0
Requires:       python-msgpack >= 0.4.6
Requires:       python-six >= 1.10.0
Requires:       python2-txaio >= 2.5.1
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
BuildRequires:  python3-mock >= 1.3.0
BuildRequires:  python3-pytest >= 2.8.6
BuildRequires:  python3-pytest-asyncio
BuildRequires:  python3-six >= 1.10.0
BuildRequires:  python3-txaio >= 2.2.1
BuildRequires:  python3-unittest2 >= 1.1.0
Requires:       python3-zope-interface >= 3.6
Requires:       python3-ujson >= 1.33
Requires:       python3-wsaccel >= 0.6.2
Requires:       python3-snappy >= 0.5
Requires:       python3-lz4 >= 0.2.1
Requires:       python3-msgpack >= 0.4.6
Requires:       python3-six >= 1.10.0
Requires:       python3-txaio >= 2.5.1
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
PYTHONPATH=$(pwd) py.test-%{python3_version} --pyargs autobahn
# Skip Python 3 only tests
rm -f autobahn/asyncio/test/test_asyncio_websocket.py
PYTHONPATH=$(pwd) py.test-%{python2_version} --pyargs autobahn


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
* Sun Jul 23 2017 Julien Enselme <jujens@jujens.eu> - 17.7.1-1.git9ad7878
- Update to 17.7.1

* Sat Jul 01 2017 Julien Enselme <jujens@jujens.eu> - 17.6.2-1.gitbc2a1b3
- Update to 17.6.2

* Sat Jun 10 2017 Julien Enselme <jujens@jujens.eu> - 17.6.1-1.gite69b314
- Update to 17.6.1

* Sun May 07 2017 Julien Enselme <jujens@jujens.eu> - 17.5.1-1.git73bcac2
- Update to 17.5.1

* Tue Apr 18 2017 Julien Enselme <jujens@jujens.eu> - 0.18.2-1.git731228a
- Update to 0.18.2

* Wed Apr 05 2017 Julien Enselme <jujens@jujens.eu> - 0.18.1-1.gitfd7ec41
- Update to 0.18.1

* Tue Feb 28 2017 Julien Enselme <jujens@jujens.eu> - 0.17.2-1.git0eef8c7
- Update to 0.17.2

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-2.git81d9276
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

*  Mon Dec 26 2016 Julien Enselme <jujens@jujens.eu> - 0.17.0-1.git81d9276
- Update to 0.17.0

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.16.0-3.gitade9eb5
- Rebuild for Python 3.6

* Sat Oct 01 2016 Julien Enselme <jujens@jujens.eu> - 0.16.0-2.gitade9eb5
- Fix tests for pytest3

* Sun Sep 18 2016 Julien Enselme <jujens@jujens.eu> - 0.16.0-1.gitade9eb5
- Update to 0.16.0

* Mon Jul 25 2016 Julien Enselme <jujens@jujens.eu> - 0.15.0-1.git43b57f8
- Update to 0.15.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.0-2.git81f693d
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon May 16 2016 Julien Enselme <jujens@jujens.eu> - 0.14.0-1.git81f693d
- Update to 0.14.0

* Sat Feb 27 2016 Julien Enselme <jujens@jujens.eu> - 0.12.1-1.git22b1183
- Update to 0.12.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.7-3.gita69e704
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

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
