#include <stdio.h>
#include <dlfcn.h>
typedef int (*encrypt_fn)(int);
int main(void) {
    void *handle = dlopen("./libcrypto_demo.so", RTLD_NOW);
    if (!handle) { fprintf(stderr, "dlopen failed: %s\n", dlerror()); return 1; }
    dlerror();
    encrypt_fn fn = (encrypt_fn)dlsym(handle, "encrypt_value");
    const char *err = dlerror();
    if (err) { fprintf(stderr, "dlsym failed: %s\n", err); dlclose(handle); return 1; }
    printf("Runtime-loaded library: encrypted=%d\n", fn(12345));
    dlclose(handle);
    return 0;
}
