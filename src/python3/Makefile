.ONESHELL:
SHELL = /bin/bash
.SHELLFLAGS += -e

PYTHON_VER=3.6.0
PYTHON_DEB_VER=1
PYTHON_PNAME=python3.6

MAIN_TARGET = lib$(PYTHON_PNAME)-minimal_$(PYTHON_VER)-$(PYTHON_DEB_VER)_amd64.deb
DERIVED_TARGETS = lib$(PYTHON_PNAME)-stdlib_$(PYTHON_VER)-$(PYTHON_DEB_VER)_amd64.deb \
				  lib$(PYTHON_PNAME)_$(PYTHON_VER)-$(PYTHON_DEB_VER)_amd64.deb \
				  $(PYTHON_PNAME)-minimal_$(PYTHON_VER)-$(PYTHON_DEB_VER)_amd64.deb \
				  $(PYTHON_PNAME)_$(PYTHON_VER)-$(PYTHON_DEB_VER)_amd64.deb \
				  lib$(PYTHON_PNAME)-dev_$(PYTHON_VER)-$(PYTHON_DEB_VER)_amd64.deb
				  #$(PYTHON_PNAME)-dev_$(PYTHON_VER)-$(PYTHON_DEB_VER)_amd64.deb

$(addprefix $(DEST)/, $(MAIN_TARGET)): $(DEST)/% :
	## Obtaining the python3
	wget 'https://sonicstorage.blob.core.windows.net/public/$(PYTHON_PNAME)_$(PYTHON_VER).orig.tar.xz' -O $(PYTHON_PNAME)_$(PYTHON_VER).orig.tar.xz
	wget 'https://sonicstorage.blob.core.windows.net/public/$(PYTHON_PNAME)_$(PYTHON_VER)-$(PYTHON_DEB_VER).debian.tar.xz' -O $(PYTHON_PNAME)_$(PYTHON_VER)-$(PYTHON_DEB_VER).debian.tar.xz
	wget 'https://sonicstorage.blob.core.windows.net/public/$(PYTHON_PNAME)_$(PYTHON_VER)-$(PYTHON_DEB_VER).dsc' -O $(PYTHON_PNAME)_$(PYTHON_VER)-$(PYTHON_DEB_VER).dsc

	## Build
	dpkg-source -x $(PYTHON_PNAME)_$(PYTHON_VER)-$(PYTHON_DEB_VER).dsc
	pushd $(PYTHON_PNAME)-$(PYTHON_VER)
	mk-build-deps

	# put a lock here because dpkg does not allow installing packages in parallel
	while true; do
	if mkdir $(DEST)/dpkg_lock &> /dev/null; then
	{ echo here && (sudo dpkg -i $(PYTHON_PNAME)-build-deps_$(PYTHON_VER)-$(PYTHON_DEB_VER)_amd64.deb || sudo apt-get install -f) && rm -d $(DEST)/dpkg_lock && break; } || { rm -d $(DEST)/dpkg_lock && exit 1 ; }
	fi
	done

	dpkg-buildpackage -rfakeroot -us -uc -b -j$(SONIC_CONFIG_MAKE_JOBS) --admindir $(SONIC_DPKG_ADMINDIR)
	popd

	cp $(DERIVED_TARGETS) $* $(DEST)/

$(addprefix $(DEST)/, $(DERIVED_TARGETS)): $(DEST)/% : $(DEST)/$(MAIN_TARGET)
