CC=gcc
CFLAGS=-std=c11 -Wall -Wextra -O2
all: raid_calc
raid_calc: raid_calc.c
	$(CC) $(CFLAGS) -o $@ $<
run: raid_calc
	./raid_calc
	@echo "--- block devices ---"
	lsblk
	@echo "--- partitions (may require sudo for full detail) ---"
	sudo -n fdisk -l 2>/dev/null || fdisk -l 2>/dev/null || true
	@echo "--- swap ---"
	swapon --show
clean:
	rm -f raid_calc
