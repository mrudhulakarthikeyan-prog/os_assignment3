#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/resource.h>
static void report(const char *label) {
    struct rusage r; getrusage(RUSAGE_SELF,&r);
    printf("%s: max RSS=%ld KB, minor faults=%ld, major faults=%ld\n",
           label,r.ru_maxrss,r.ru_minflt,r.ru_majflt); fflush(stdout);
}
int main(void) {
    size_t n=8*1024*1024;
    unsigned char *p=malloc(n);
    if(!p){perror("malloc");return 1;}
    for(size_t i=0;i<n;i+=4096)p[i]=1;
    report("Parent before fork");
    pid_t pid=fork();
    if(pid<0){perror("fork");free(p);return 1;}
    if(pid==0){for(size_t i=0;i<n;i+=4096)p[i]=2; report("Child after writes"); _exit(0);}
    waitpid(pid,NULL,0); report("Parent after child"); free(p); return 0;
}
