#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int conflicts(int queens[], n) {
    int c = 0;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            if (i != j && abs(queens[i-1]-queens[j-1]) == abs(i-j)) {
                c++;
            }
        }
    }
    return c;
}

int main()
{
    int n = 8;
    
    
    
}