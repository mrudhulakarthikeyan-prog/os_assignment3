#include <stdio.h>
int encrypt_value(int value);
int main(void) {
    int input = 12345;
    printf("Bank application: input=%d encrypted=%d\n", input, encrypt_value(input));
    return 0;
}
