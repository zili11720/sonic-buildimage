SHELL = /bin/bash
.ONESHELL:
.SHELLFLAGS += -e

REDIS_VERSION = 3.2.13
REDIS_VERSION_FULL = $(REDIS_VERSION)-1~bpo8+1

MAIN_TARGET = redis-server_$(REDIS_VERSION_FULL)_amd64.deb
DERIVED_TARGETS = redis-tools_$(REDIS_VERSION_FULL)_amd64.deb \
		  redis-sentinel_$(REDIS_VERSION_FULL)_amd64.deb

$(addprefix $(DEST)/, $(MAIN_TARGET)): $(DEST)/% :
	wget -O redis_$(REDIS_VERSION).orig.tar.gz -N "https://sonicstorage.blob.core.windows.net/public/redis/redis_$(REDIS_VERSION).orig.tar.gz"
	wget -O redis_$(REDIS_VERSION_FULL).dsc -N "https://sonicstorage.blob.core.windows.net/public/redis/redis_$(REDIS_VERSION_FULL).dsc"
	wget -O redis_$(REDIS_VERSION_FULL).debian.tar.xz -N "https://sonicstorage.blob.core.windows.net/public/redis/redis_$(REDIS_VERSION_FULL).debian.tar.xz"
	dpkg-source -x redis_$(REDIS_VERSION_FULL).dsc

	pushd redis-$(REDIS_VERSION)
	DEB_BUILD_OPTIONS=nocheck dpkg-buildpackage -us -uc -b -j$(SONIC_CONFIG_MAKE_JOBS) --admindir $(SONIC_DPKG_ADMINDIR)
	popd

	mv $(DERIVED_TARGETS) $* $(DEST)/

$(addprefix $(DEST)/, $(DERIVED_TARGETS)): $(DEST)/% : $(DEST)/$(MAIN_TARGET)
