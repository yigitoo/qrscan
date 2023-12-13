all: default

default: run

run:
	python3 qrscan.py

install:
	pip3 install -r requirements.txt

TODO := 0
ifeq ($(TODO),)
build:
	PYTHON BUILD THINGS

test:
	PYTHON TEST THINGS
endif

.PHONY: all default run build test install
