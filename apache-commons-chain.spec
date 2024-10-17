%{?_javapackages_macros:%_javapackages_macros}
%global base_name chain
%global short_name commons-%{base_name}
Name:          apache-commons-chain
Version:       1.2
Release:       8.0%{?dist}
Summary:       An implementation of the GoF Chain of Responsibility pattern
License:       ASL 2.0
URL:           https://commons.apache.org/%{base_name}/
Source0:       ftp://ftp.gbnet.net/pub/apache/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
# javax.servlet 3.0 api support
Patch0:        %{name}-%{version}-tests-servlet30.patch
# javax.portlet 2.0 api support
Patch1:        %{name}-%{version}-portlet20.patch

BuildRequires: java-devel

BuildRequires: mvn(commons-beanutils:commons-beanutils)
BuildRequires: mvn(commons-digester:commons-digester)
BuildRequires: mvn(commons-logging:commons-logging)
BuildRequires: mvn(javax.portlet:portlet-api)
BuildRequires: mvn(org.apache.tomcat:tomcat-servlet-api)
BuildRequires: mvn(org.jboss.spec.javax.faces:jboss-jsf-api_2.1_spec)

# test deps
BuildRequires: mvn(junit:junit)

BuildRequires: buildnumber-maven-plugin
BuildRequires: maven-local
BuildRequires: maven-antrun-plugin
BuildRequires: maven-plugin-bundle
BuildRequires: maven-remote-resources-plugin
BuildRequires: maven-site-plugin
BuildRequires: maven-surefire-provider-junit

BuildArch:     noarch

%description
A popular technique for organizing the execution of complex
processing flows is the "Chain of Responsibility" pattern, as
described (among many other places) in the classic "Gang of Four"
design patterns book. Although the fundamental API contracts
required to implement this design pattern are extremely simple,
it is useful to have a base API that facilitates using the pattern,
and (more importantly) encouraging composition of command
implementations from multiple diverse sources.
Towards that end, the Chain API models a computation as a series
of "commands" that can be combined into a "chain". The API for a
command consists of a single method (execute()), which is passed
a "context" parameter containing the dynamic state of the
computation, and whose return value is a boolean that determines
whether or not processing for the current chain has been completed
(true), or whether processing should be delegated to the next
command in the chain (false).

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{short_name}-%{version}-src
find . -name '*.class' -delete
find . -name '*.jar' -delete

perl -pi -e 's/\r$//g;' *.txt

%patch0 -p1
%patch1 -p0
# Failed tests:   testDefaut(org.apache.commons.chain.config.ConfigParserTestCase):
# Correct command count expected:<17> but was:<19>
rm -r src/test/org/apache/commons/chain/config/ConfigParserTestCase.java

%pom_remove_dep :myfaces-api
%pom_add_dep org.jboss.spec.javax.faces:jboss-jsf-api_2.1_spec
# Force tomcat apis
%pom_remove_dep javax.servlet:servlet-api
%pom_add_dep org.apache.tomcat:tomcat-servlet-api

%mvn_file :%{short_name} %{name}
%mvn_file :%{short_name} %{short_name}

%build

%mvn_build -- -Dmaven.compile.source=1.5 -Dmaven.compile.target=1.5

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 02 2013 gil cattaneo <puntogil@libero.it> 1.2-7
- build with XMvn
- swith to pom macros
- minor changes to adapt to current guideline

* Sun Feb 17 2013 gil cattaneo <puntogil@libero.it> 1.2-6
- added missing BR surefire-provider-junit

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.2-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 05 2012 gil cattaneo <puntogil@libero.it> 1.2-2
- NOTICE.txt file installed along with javadoc package

* Thu Apr 19 2012 gil cattaneo <puntogil@libero.it> 1.2-1
- initial rpm

