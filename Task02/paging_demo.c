#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define PAGE_SIZE 1024
#define PAGES 8
int page_table[PAGES] = {5, 2, -1, 7, 0, -1, 3, -1};

static void translate(unsigned a) {
    unsigned p = a / PAGE_SIZE, d = a % PAGE_SIZE;
    printf("%5u -> page %u offset %5u : ", a, p, d);
    if (p >= PAGES) puts("invalid address");
    else if (page_table[p] == -1) puts("page fault");
    else printf("physical %u\n", (unsigned)page_table[p] * PAGE_SIZE + d);
}
static void fragmentation(void) {
    unsigned sizes[] = {1200, 4097, 8192, 777, 16385, 3000, 5500, 999, 21000, 42};
    const int n = (int)(sizeof sizes / sizeof sizes[0]);
    const unsigned ps[] = {1024, 4096, 2u * 1024u * 1024u};
    puts("Internal fragmentation for sample process sizes:");
    for (int j=0; j<3; j++) {
        unsigned long long waste=0;
        for (int i=0; i<n; i++) waste += (ps[j] - sizes[i] % ps[j]) % ps[j];
        printf("page size %u bytes: total unused bytes=%llu (n=%d)\n", ps[j], waste, n);
    }
}
static void tlb(void) {
    const double mem=100.0, lookup=10.0;
    const double ratios[]={0.80,0.95,0.99};
    puts("EAT with serial TLB lookup, hit: lookup+memory, miss: lookup+2*memory:");
    for(int i=0;i<3;i++) {
        double r=ratios[i], eat=r*(lookup+mem)+(1-r)*(lookup+2*mem);
        printf("hit ratio %.0f%%: %.2f ns\n",r*100,eat);
    }
    printf("Without TLB (one-level page table): %.2f ns\n",2*mem);
}
int main(void) {
    unsigned logical[]={0,1500,3100,6200,9000,2049};
    puts("Address translation (PAGE_SIZE=1024):");
    for(int i=0;i<6;i++) translate(logical[i]);
    fragmentation(); tlb();
    return 0;
}
