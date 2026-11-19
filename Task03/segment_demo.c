#include <stdio.h>
#include <unistd.h>
typedef struct { const char *name; int base; int limit; } Segment;
int main(void) {
    Segment s[]={{"code",1000,499},{"data",5000,999},{"stack",9000,499}};
    int tests[][2]={{0,10},{0,499},{0,500},{1,250},{1,999},{1,1000},{2,64},{2,499}};
    puts("Segment translation (segment, offset):");
    for(unsigned i=0;i<sizeof tests/sizeof tests[0];i++) {
        int id=tests[i][0], off=tests[i][1];
        if(off<0 || off>=s[id].limit) printf("(%d,%d) %s: protection fault (limit=%d)\n",id,off,s[id].name,s[id].limit);
        else printf("(%d,%d) %s -> physical %d\n",id,off,s[id].name,s[id].base+off);
    }
    printf("PID=%ld; first entries of /proc/self/maps:\n",(long)getpid());
    FILE *f=fopen("/proc/self/maps","r"); char line[512]; int n=0;
    if(f){while(fgets(line,sizeof line,f)&&n++<12) fputs(line,stdout); fclose(f);}
    return 0;
}
