# Fichier Makefile pour installer les bibliothèques Python requises et les modules externes

# Définir l'interpréteur Python à utiliser
PYTHON := /chemin/interpréteur/python

# Définir les bibliothèques requises
LIBRARIES := numpy scipy json

# Définir les modules externes
EXTERNAL_MODULES := readgssi matplotlib PyQt6

# Targets
all: install_external install_libraries

install_external:
	@echo "Installing external Python modules..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install $(EXTERNAL_MODULES)
	@echo "External modules installation completed."

install_libraries:
	@echo "Installing required Python libraries..."
	$(PYTHON) -m pip install $(LIBRARIES)
	@echo "Libraries installation completed."

.PHONY: install_external install_libraries

