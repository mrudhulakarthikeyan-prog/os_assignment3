#include <stdio.h>
int main(void){
 const double total=2048.0, control=128.0, ml=1536.0, logging=128.0, reserve=256.0;
 printf("Edge device RAM budget (MB): %.0f\n",total);
 printf("Control task: %.0f MB (pre-fault and lock with mlock)\n",control);
 printf("ML task: %.0f MB (paging may be tolerated only if timing allows)\n",ml);
 printf("Logging: %.0f MB; OS/reserve: %.0f MB\n",logging,reserve);
 printf("Planned total: %.0f MB; remaining: %.0f MB\n",control+ml+logging+reserve,total-(control+ml+logging+reserve));
 printf("Adding a 500 MB task exceeds the budget by %.0f MB; reduce ML working set, offload work, or add RAM.\n",
        control+ml+logging+reserve+500-total);
 return 0;
}
