#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <unistd.h>
int encrypt_value(int value);
int main(void) {
    printf("PID=%ld encryption-check=%d\n", (long)getpid(), encrypt_value(12345));
    fflush(stdout);
    sleep(20);
    return 0;
}
