#include <stdio.h>

unsigned int part(unsigned int b, unsigned int d) {
  unsigned int a, c, e;
  a = 0;
  
  for (e = 1; e <= b; e++) {   
    for (c = 1; c <= b; c++) {
      if (b == e * c) { 
        a += e; 
      }
    }
  }

  return a;
}

int main() {
  printf("part 1: %u\n", part(909, 73));
  printf("part 2: %u\n", part(10551309, 10550400));
  return 0;
}