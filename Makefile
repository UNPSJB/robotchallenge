.PHONY: docs help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
if not sys.argv[1].startswith('http'):
	try:
		from urllib import pathname2url
	except:
		from urllib.request import pathname2url
	path = "file://" + pathname2url(os.path.abspath(sys.argv[1]))
else:
	path = sys.argv[1]

webbrowser.open(path)
endef
export BROWSER_PYSCRIPT


define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"


# define PYTHON_SELECTOR
# # Busca el binario de python que tenga Kivy, primero el del sistema
# # Y luego un virtualenv que se llame kivy
# import sys
# import os

# try:
# 	import kivy
# 	print(sys.executable)
# except ImportError:
# 	venv_path = os.path.expanduser("~/.virtualenvs/kivy/bin/python")
# 	print(venv_path)
# endef
# export PYTHON_SELECTOR
# PYTHON_BIN := $(shell python -c "$$PYTHON_SELECTOR")

help:	## Imprime ayuda
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

debug:
	echo $(PYTHON_BIN)
	$(PYTHON_BIN)
run:	## Ejecuta localmente el proyecto
	python src/main.py

push: 	## Carga el código al telefono
	$(eval PWD=$(shell pwd))
	$(eval BASENAME=$(shell basename $(PWD)))
	$(eval DESTINATION=/storage/emulated/legacy/)
	cd src && \
	for file in *.py *.kv data/* android.txt; do \
		echo $$file ; \
		adb push $$file $(DESTINATION)kivy/$(BASENAME)/$$file ; \
	done

abrir_github:	## Abre el sitio de Github
	$(BROWSER) https://github.com/UNPSJB/robotchallenge

descargar_platform_tools:	##
	https://dl.google.com/android/repository/platform-tools-latest-windows.zip
	https://dl.google.com/android/repository/platform-tools-latest-linux.zip
	https://dl.google.com/android/repository/platform-tools-latest-darwin.zip
