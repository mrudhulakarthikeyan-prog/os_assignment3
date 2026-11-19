#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define N 100000
#define MAXF 10
static int faults_lru(const int *r,int n,int cap){
 int f[MAXF],last[MAXF],used=0,miss=0;
 for(int i=0;i<n;i++){int k=-1;for(int j=0;j<used;j++)if(f[j]==r[i])k=j;
 if(k>=0){last[k]=i;continue;}miss++;int s;
 if(used<cap)s=used++;else{s=0;for(int j=1;j<cap;j++)if(last[j]<last[s])s=j;}
 f[s]=r[i];last[s]=i;}return miss;
}
int main(void){
 int *r=malloc(N*sizeof *r);if(!r)return 1;
 srand(42);for(int i=0;i<N;i++)r[i]=(i%10<8)?rand()%12:rand()%100;
 FILE *o=fopen("locality.csv","w");if(!o){perror("fopen");free(r);return 1;}
 fprintf(o,"frames,lru_faults\n");
 for(int f=3;f<=10;f++){int x=faults_lru(r,N,f);fprintf(o,"%d,%d\n",f,x);printf("%d frames: LRU faults=%d\n",f,x);}
 fclose(o);free(r);puts("Wrote locality.csv (mixed strong-locality/random reference workload).");return 0;
}
