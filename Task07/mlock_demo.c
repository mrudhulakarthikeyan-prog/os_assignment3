#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/mman.h>
#include <unistd.h>
#define MB (8u*1024u*1024u)
static double elapsed(struct timespec a,struct timespec b){return (b.tv_sec-a.tv_sec)+(b.tv_nsec-a.tv_nsec)/1e9;}
static void loop(volatile unsigned char *p,size_t n,const char *label){
 struct timespec a,b;long max_ns=0;clock_gettime(CLOCK_MONOTONIC,&a);
 for(int k=0;k<200;k++){struct timespec x,y;clock_gettime(CLOCK_MONOTONIC,&x);
 for(size_t i=0;i<n;i+=4096)p[i]++;
 clock_gettime(CLOCK_MONOTONIC,&y);long ns=(y.tv_sec-x.tv_sec)*1000000000L+y.tv_nsec-x.tv_nsec;if(ns>max_ns)max_ns=ns;}
 clock_gettime(CLOCK_MONOTONIC,&b);
 printf("%s: total %.6f s; worst measured pass %.0f us\n",label,elapsed(a,b),max_ns/1000.0);
}
int main(void){
 size_t n=MB;volatile unsigned char *p=calloc(n,1);if(!p){perror("calloc");return 1;}
 loop(p,n,"Without mlock");
 if(mlock((const void *)p,n)==0){loop(p,n,"With mlock");munlock((const void *)p,n);}
 else perror("mlock (may be restricted by RLIMIT_MEMLOCK)");
 free((void *)p);return 0;
}
