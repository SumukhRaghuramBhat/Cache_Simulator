#include<stdio.h>

#define M 1000
#define N 2000

void main(void)
{
    long arr[M][N] = {0}, i= 0, j=0, k=0;
   
        for(i = 0; i< M; i++)
        {
            for(j = 0; j< N; j++)
            {
            
                arr[i][j] += 2;
            }
        }
}
