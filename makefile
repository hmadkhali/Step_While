PY=python3
MAIN=main
DIR=$(PWD)
.SUFFIXES: .py
FILES = \
	code.py
All: 
	echo " $(PY) $(DIR)/$(FILES) " \"'$$1'\" > while-ss
	chmod 777 while-ss
