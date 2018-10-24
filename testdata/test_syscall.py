#!/usr/bin/env python3
from ontology.interop.System.Runtime import *
from ontology.interop.Ontology.Runtime import *

def main():
    time = GetTime()
    hash_160 = hash160("0000000")
    hash_256 = hash256("1111111")
    Addr = Base58ToAddress('AFmseVrdL9f9oyCzZefL9tG6UbvhUMqNMV')
    BASE58 = AddressToBase58(Addr)
    throw_if_null(BASE58 == 'AFmseVrdL9f9oyCzZefL9tG6UbvhUMqNMV')
    hash_random = GetRandomHash()
