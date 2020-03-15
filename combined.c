#include<stdio.h>

#define M 20000
#define N 50000

void row();
void column();

void main()
{
 row();
 column();
}

void row(void)
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

void column(void)
{
    long arr[M][N] = {0}, i = 0, j= 0, k = 0;
    
        for(j = 0; j< M; j++)
        {
            for(i = 0; i< N; i++)
            {
                arr[i][j] += 2;
            }
        }
}
