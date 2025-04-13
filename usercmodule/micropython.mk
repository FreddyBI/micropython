CFBI_MOD_DIR := $(USERMOD_DIR)

# Add all C files to SRC_USERMOD.
SRC_USERMOD += $(CFBI_MOD_DIR)/cfbi.c

# We can add our module folder to include paths if needed
# This is not actually needed in this CFBI.
CFLAGS_USERMOD += -I$(CFBI_MOD_DIR)
