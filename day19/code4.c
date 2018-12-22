#include <stdio.h>

unsigned int part(unsigned int b) {
  unsigned int a, c, e;
  a = 0;
  
  for (e = 1; e <= b; e++) {
    if (b % e == 0) { 
      a += e; 
    }
  }

  return a;
}

int main() {
  printf("part 1: %u\n", part(909));
  printf("part 2: %u\n", part(10551309));
  return 0;
}