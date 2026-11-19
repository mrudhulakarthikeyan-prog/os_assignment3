CC=gcc
CFLAGS=-std=c11 -Wall -Wextra -O2
all: replacement_demo locality_demo
replacement_demo: replacement_demo.c
	$(CC) $(CFLAGS) -o $@ $<
locality_demo: locality_demo.c
	$(CC) $(CFLAGS) -o $@ $<
run: all
	./replacement_demo
	./locality_demo
clean:
	rm -f replacement_demo locality_demo locality.csv
