CC=gcc
CFLAGS=-std=c11 -Wall -Wextra -O2

.PHONY: all clean
all:
	$(MAKE) -C Task01
	$(MAKE) -C Task02
	$(MAKE) -C Task03
	$(MAKE) -C Task04
	$(MAKE) -C Task05
	$(MAKE) -C Task06
	$(MAKE) -C Task07

clean:
	@for d in Task01 Task02 Task03 Task04 Task05 Task06 Task07; do $(MAKE) -C $$d clean; done
