#!/usr/bin/env python3
import binascii

bstring='145c69fdc3c648f0846e8c366e6578564f047f1c'
b_array = bytearray(binascii.unhexlify(bstring))
b_array.reverse()
print(b_array)
b_array0 = bytearray(binascii.hexlify(b_array))
print(b_array0)
