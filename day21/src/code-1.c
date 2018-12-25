unsigned long run(unsigned long a)
{
    unsigned long b, c, d, e;
    b = c = d = e = 0;

    e = 123;
    
    while (1) {
        e = e & 456;
        if (e == 72) { break; }
    }
    e = 0;
    
    do {
        d = e | 65536;
        e = 733884;

L8: // Instr(Bani, 3, 255, 1)
        b = d & 255;
        e = e + b;
        e = e & 16777215;
        e = e * 65899;
        e = e & 16777215;
        b = (256 > d);
        if (b) { return; } 
    
        b = 0;

L18: // Instr(Addi, 1, 1, 2)

        c = b + 1;
        c = ((b + 1) * 256);
        c = (c > d);
        if (d <= c) { b = b + 1; goto L18;} else { d = b; goto L8; }
    
    }  while (e != a);
}