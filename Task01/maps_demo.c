#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main(void) {
    printf("PID=%ld; inspect mappings in /proc/%ld/maps\n", (long)getpid(), (long)getpid());
    FILE *fp = fopen("/proc/self/maps", "r");
    if (!fp) { perror("fopen"); return 1; }
    char line[512];
    int n = 0;
    while (fgets(line, sizeof line, fp) && n++ < 18) fputs(line, stdout);
    fclose(fp);
    return 0;
}
