all = lib
TARGET = util
SHVER = 1
OS = $(shell uname)

all: lib 
	make -C liblinear
	make -C liblinear/python

lib: ${TARGET}.o
	if [ "$(OS)" = "Darwin" ]; then \
		SHARED_LIB_FLAG="-dynamiclib -Wl,-install_name,${TARGET}.so.$(SHVER)"; \
	else \
		SHARED_LIB_FLAG="-shared -Wl,-soname,${TARGET}.so.$(SHVER)"; \
	fi; \
	gcc $${SHARED_LIB_FLAG} ${TARGET}.o -o ${TARGET}.so.1

${TARGET}.o: ${TARGET}.c
	gcc -fPIC -Iliblinear -O3 -c -o ${TARGET}.o ${TARGET}.c

clean:
	rm -rf ${TARGET}.o ${TARGET}.so.1 *pyc
	make -C liblinear clean
