CC=gcc
CFLAGS=-std=c11 -Wall -Wextra -O2
all: vm_access cow_demo
vm_access: vm_access.c
	$(CC) $(CFLAGS) -o $@ $<
cow_demo: cow_demo.c
	$(CC) $(CFLAGS) -o $@ $<
run: all
	./vm_access 32
	./cow_demo
	@echo "--- /usr/bin/time -v sample ---"
	/usr/bin/time -v ./vm_access 32 2>&1 | tail -n 12
clean:
	rm -f vm_access cow_demo
