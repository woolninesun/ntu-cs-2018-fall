#!/usr/bin/env python3

FLAG = [
      37,    5,  118,   90, -112,  -13,  -34,    7,
     106,  102, -115,  -20,  -51,    0,   80,   84,
    -115,   -3,  -34,    2,  121,   84,  -87,    -8
]

for i in range( len(FLAG) ):
    FLAG[i] = chr( ( FLAG[i] ^ ( i * 42 + 1 ^ 0x42 ) ) & 0xff )

print(''.join(FLAG))
