CC=gcc
CFLAGS=-std=c11 -Wall -Wextra -O2
all: mlock_demo memory_plan
mlock_demo: mlock_demo.c
	$(CC) $(CFLAGS) -o $@ $<
memory_plan: memory_plan.c
	$(CC) $(CFLAGS) -o $@ $<
run: all
	./mlock_demo
	./memory_plan
clean:
	rm -f mlock_demo memory_plan
