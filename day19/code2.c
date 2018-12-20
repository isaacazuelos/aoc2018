#include <stdio.h>

unsigned long part(int part) {
  //            0  1  3  4  5 with ip in reg 2
  unsigned long a, b, c, d, e;
  a = b = c = d = e = 0;

  if (part == 2) { 
    d = 10550400;
    b = 10551309; 
  } else {
    d = 73;  // 73
    b = 909 ;  // 909
  }

  e = 1;
  
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
  printf("part_1: %lu\n", part(1));
  printf("part_2: %lu\n", part(2));
  return 0;
}