#include <stdio.h>
int main(void) {
    volatile int *p = (volatile int *)0;
    puts("About to access a null address; a segmentation fault is expected.");
    fflush(stdout);
    *p = 42;
    return 0;
}
