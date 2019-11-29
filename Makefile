PY=python3
FILE=descriptor.py
INDENTOR=indent
TARGET=test.c

all:
	$(PY) $(FILE) | $(INDENTOR) > $(TARGET);cat $(TARGET)

clean:
	rm -rf $(TARGET)