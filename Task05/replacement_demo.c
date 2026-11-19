#include <stdio.h>
#define MAXF 8
int find(const int f[],int n,int page){for(int i=0;i<n;i++)if(f[i]==page)return i;return -1;}
int fifo(const int r[],int len,int frames){
 int f[MAXF],used=0,next=0,faults=0;
 for(int i=0;i<len;i++){if(find(f,used,r[i])>=0)continue;faults++;
 if(used<frames)f[used++]=r[i];else{f[next]=r[i];next=(next+1)%frames;}}
 return faults;
}
int lru(const int r[],int len,int frames){
 int f[MAXF],last[MAXF],used=0,faults=0;
 for(int i=0;i<len;i++){
  int k=find(f,used,r[i]); if(k>=0){last[k]=i;continue;} faults++;
  int slot;
  if(used<frames)slot=used++;
  else{slot=0;for(int j=1;j<frames;j++)if(last[j]<last[slot])slot=j;}
  f[slot]=r[i];last[slot]=i;
 }
 return faults;
}
int optimal(const int r[],int len,int frames){
 int f[MAXF],used=0,faults=0;
 for(int i=0;i<len;i++){if(find(f,used,r[i])>=0)continue;faults++;
 if(used<frames){f[used++]=r[i];continue;}
 int victim=0,farthest=-1;
 for(int j=0;j<frames;j++){int next=len;for(int t=i+1;t<len;t++)if(r[t]==f[j]){next=t;break;}
 if(next>farthest){farthest=next;victim=j;}}
 f[victim]=r[i];}
 return faults;
}
int main(void){
 int r[]={7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1};
 int b[]={1,2,3,4,1,2,5,1,2,3,4,5};
 for(int fr=3;fr<=4;fr++)printf("%d frames: FIFO %d, LRU %d, Optimal %d\n",fr,fifo(r,20,fr),lru(r,20,fr),optimal(r,20,fr));
 printf("Belady string, FIFO: 3 frames %d faults, 4 frames %d faults\n",fifo(b,12,3),fifo(b,12,4));
 return 0;
}
