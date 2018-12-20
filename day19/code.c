#include <stdio.h>

unsigned long part_2() {
  //            0  1  3  4  5 with ip in reg 2
  unsigned long a, b, c, d, e;
  a = b = c = d = e = 0;
  a = 0;

l00:
  goto l17;
l01:
  e = 1;
l02:
  c = 1;
l03:
  d = e * c;
l04:
  d = (b == d);
l05:
  if (d) { goto l07; } else { goto l06; }
l06:
  goto l08;
l07:
  a = e + a;
l08:
  c += 1;
l09:
  d = (c > b);
l10:
  if (d) { goto l12; } else { goto l11; }
l11:
  goto l03;
l12:
  e += 1;
l13:
  d = (e > b);
l14:
  if (d) { goto l16; } else { goto l15; }
l15:
  goto l02;
l16:
  return a;

  // Below builds the smaller input for part 1
  
l17:
  b += 2;  // 0 + 2 = 2
l18:
  b *= 2;  // 2 * 2 = 4
l19:
  b *= 19;  // 2 * 8 = 0 weird
l20:
  b *= 11; // 0
l21:
  d += 3;  // 3
l22:
  d *= 22; // 66
l23:
  d += 7;  // 73
l24:
  b += d;  // 73
l25: // addr 2 0 2
  
  // this is to distinguish part 1 from 2:
  // so `a == 0` or `a == 1`

  
  switch (a + 25) {
    case 25: goto l26; break;
    case 26: goto l27; break;
    case 27: goto l28; break;
    case 28: goto l29; break;
    case 29: goto l30; break;
    case 30: goto l31; break;
    case 31: goto l32; break;
    case 32: goto l33; break;
    case 33: goto l34; break;
    case 34: goto l35; break;
    default: return a; break;
  }
     
l26:
  // Here's the branch away for part 1, 
  // so the inputs are smaller.
  goto l01;
l27:
  d = 27;
l28:
  d *= 28;
l29:
  d += 29;
l30:
  d *= 30;
l31:
  d *= 14;
l32:
  d *= 32;
l33:
  b += d;
l34:
  // Hide that `a` determines the input
  a = 0;
l35:
  goto l01;
}

int main() {
  printf("part_2: %lu\n", part_2());
  return 0;
}