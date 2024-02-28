BRCM_SAI = libsaibcm_5.0.0.12_amd64.deb
$(BRCM_SAI)_URL = "https://sonicstorage.blob.core.windows.net/public/bcmsai/5.0/master/libsaibcm_5.0.0.12_amd64.deb"

BRCM_SAI_DEV = libsaibcm-dev_5.0.0.12_amd64.deb
$(eval $(call add_derived_package,$(BRCM_SAI),$(BRCM_SAI_DEV)))
$(BRCM_SAI_DEV)_URL = "https://sonicstorage.blob.core.windows.net/public/bcmsai/5.0/master/libsaibcm-dev_5.0.0.12_amd64.deb"

# SAI module for DNX Asic family
BRCM_DNX_SAI = libsaibcm_dnx_5.0.0.12_amd64.deb
$(BRCM_DNX_SAI)_URL = "https://sonicstorage.blob.core.windows.net/public/bcmsai/5.0/master/libsaibcm_dnx_5.0.0.12_amd64.deb"

SONIC_ONLINE_DEBS += $(BRCM_SAI)
SONIC_ONLINE_DEBS += $(BRCM_DNX_SAI)
$(BRCM_SAI_DEV)_DEPENDS += $(BRCM_SAI)
$(eval $(call add_conflict_package,$(BRCM_SAI_DEV),$(LIBSAIVS_DEV)))
