#include <stdio.h>
int main(void){
 const double disk=4.0; const int n=6;
 printf("Assuming %d disks of %.1f TB each (decimal TB):\n",n,disk);
 printf("RAID 0: %.1f TB usable; no redundancy\n",n*disk);
 printf("RAID 1: %.1f TB usable (mirrored pairs); survives one disk per mirror pair\n",(n/2)*disk);
 printf("RAID 5: %.1f TB usable; survives one disk failure\n",(n-1)*disk);
 printf("RAID 6: %.1f TB usable; survives two disk failures\n",(n-2)*disk);
 printf("RAID 10: %.1f TB usable; survives at least one failure, depending on mirror pair\n",(n/2)*disk);
 return 0;
}
