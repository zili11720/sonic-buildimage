SHELL = /bin/bash
.ONESHELL:
.SHELLFLAGS += -e

MAIN_TARGET = libsnmp-base_$(SNMPD_VERSION_FULL)_all.deb
DERIVED_TARGETS = snmptrapd_$(SNMPD_VERSION_FULL)_amd64.deb \
		  snmp_$(SNMPD_VERSION_FULL)_amd64.deb \
		  snmpd_$(SNMPD_VERSION_FULL)_amd64.deb \
		  libsnmp30_$(SNMPD_VERSION_FULL)_amd64.deb \
		  libsnmp30-dbg_$(SNMPD_VERSION_FULL)_amd64.deb \
		  libsnmp-dev_$(SNMPD_VERSION_FULL)_amd64.deb \
		  libsnmp-perl_$(SNMPD_VERSION_FULL)_amd64.deb \
		  python-netsnmp_$(SNMPD_VERSION_FULL)_amd64.deb \
		  tkmib_$(SNMPD_VERSION_FULL)_all.deb

$(addprefix $(DEST)/, $(MAIN_TARGET)): $(DEST)/% :
	rm -rf net-snmp-$(SNMPD_VERSION)

	# download debian net-snmp
	wget -NO net-snmp_$(SNMPD_VERSION_FULL).dsc "https://sonicstorage.blob.core.windows.net/public/net-snmp_5.7.3+dfsg-1.5.dsc"
	wget -NO net-snmp_$(SNMPD_VERSION).orig.tar.xz "https://sonicstorage.blob.core.windows.net/public/net-snmp_5.7.3+dfsg.orig.tar.xz"
	wget -NO net-snmp_$(SNMPD_VERSION_FULL).debian.tar.xz "https://sonicstorage.blob.core.windows.net/public/net-snmp_5.7.3+dfsg-1.5.debian.tar.xz"
	dpkg-source -x net-snmp_$(SNMPD_VERSION_FULL).dsc

	pushd net-snmp-$(SNMPD_VERSION)
	git init
	git add -f *
	git commit -m "unmodified snmpd source"

	# Apply patches
	stg init
	stg import -s ../patch-$(SNMPD_VERSION)/series

	dpkg-buildpackage -rfakeroot -b -d -us -uc -j$(SONIC_CONFIG_MAKE_JOBS) --admindir $(SONIC_DPKG_ADMINDIR)
	popd

	mv $(DERIVED_TARGETS) $* $(DEST)/

$(addprefix $(DEST)/, $(DERIVED_TARGETS)): $(DEST)/% : $(DEST)/$(MAIN_TARGET)
