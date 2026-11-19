CC=gcc
CFLAGS=-std=c11 -Wall -Wextra -O2
all: segment_demo segfault_demo
segment_demo: segment_demo.c
	$(CC) $(CFLAGS) -o $@ $<
segfault_demo: segfault_demo.c
	$(CC) $(CFLAGS) -o $@ $<
run: segment_demo
	./segment_demo
clean:
	rm -f segment_demo segfault_demo
