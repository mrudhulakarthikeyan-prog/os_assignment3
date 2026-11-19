CC=gcc
CFLAGS=-std=c11 -Wall -Wextra -O2
all: bank_static bank_dynamic bank_dlopen libcrypto_demo.so maps_demo
crypto.o: crypto.c
	$(CC) $(CFLAGS) -c crypto.c
bank_static: main.c crypto.o
	$(CC) $(CFLAGS) -o $@ main.c crypto.o
libcrypto_demo.so: crypto.c
	$(CC) $(CFLAGS) -fPIC -shared -o $@ crypto.c
bank_dynamic: main.c libcrypto_demo.so
	$(CC) $(CFLAGS) -o $@ main.c -L. -lcrypto_demo -Wl,-rpath,'$$ORIGIN'
bank_dlopen: main_dlopen.c
	$(CC) $(CFLAGS) -o $@ main_dlopen.c -ldl
run: all
	./bank_static
	LD_LIBRARY_PATH=. ./bank_dynamic
	./bank_dlopen
	@echo "--- file sizes ---"
	ls -lh bank_static bank_dynamic libcrypto_demo.so
	@echo "--- linked shared libraries ---"
	ldd ./bank_dynamic
	@echo "--- current process maps (sample) ---"
	./maps_demo
maps_demo: maps_demo.c
	$(CC) $(CFLAGS) -o $@ maps_demo.c
clean:
	rm -f bank_static bank_dynamic bank_dlopen libcrypto_demo.so crypto.o maps_demo
