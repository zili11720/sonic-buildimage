BRCM_SAI = libsaibcm_3.5.3.8_amd64.deb
$(BRCM_SAI)_URL = "https://sonicstorage.blob.core.windows.net/public/bcmsai/3.5/jessie/libsaibcm_3.5.3.8_amd64.deb"

BRCM_SAI_DEV = libsaibcm-dev_3.5.3.8_amd64.deb
$(eval $(call add_derived_package,$(BRCM_SAI),$(BRCM_SAI_DEV)))
$(BRCM_SAI_DEV)_URL = "https://sonicstorage.blob.core.windows.net/public/bcmsai/3.5/jessie/libsaibcm-dev_3.5.3.8_amd64.deb"

SONIC_ONLINE_DEBS += $(BRCM_SAI)
$(BRCM_SAI_DEV)_DEPENDS += $(BRCM_SAI)
$(eval $(call add_conflict_package,$(BRCM_SAI_DEV),$(LIBSAIVS_DEV)))
