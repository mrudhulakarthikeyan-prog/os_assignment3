#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <unistd.h>
int main(int argc,char **argv) {
    size_t mb=(argc>1)?(size_t)strtoul(argv[1],NULL,10):32;
    if(mb<1 || mb>512){fprintf(stderr,"Choose memory between 1 and 512 MB.\n");return 2;}
    size_t bytes=mb*1024u*1024u, page=(size_t)sysconf(_SC_PAGESIZE);
    volatile unsigned char *p=calloc(bytes,1);
    if(!p){perror("calloc");return 1;}
    struct timespec a,b; clock_gettime(CLOCK_MONOTONIC,&a);
    for(size_t i=0;i<bytes;i+=page) p[i]=(unsigned char)(i/page);
    clock_gettime(CLOCK_MONOTONIC,&b);
    double sec=(b.tv_sec-a.tv_sec)+(b.tv_nsec-a.tv_nsec)/1e9;
    printf("Touched %zu MB sequentially in %.6f seconds; page size=%zu bytes\n",mb,sec,page);
    for(size_t i=bytes;i>page;i-=page) p[i-page]^=1;
    puts("Reverse page-order pass completed.");
    free((void *)p); return 0;
}
