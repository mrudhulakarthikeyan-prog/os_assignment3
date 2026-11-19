CC=gcc
CFLAGS=-std=c11 -Wall -Wextra -O2
all: paging_demo
paging_demo: paging_demo.c
	$(CC) $(CFLAGS) -o $@ $<
run: paging_demo
	./paging_demo
	@echo "--- Linux page size ---"
	getconf PAGESIZE
clean:
	rm -f paging_demo
