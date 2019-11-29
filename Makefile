PY=python3
FILE=descriptor.py
FORMATTER=indent
TARGET=test.c

all:
	$(PY) $(FILE) | $(FORMATTER) > $(TARGET)

clean:
	rm -rf $(TARGET)