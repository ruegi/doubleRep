# -*- coding: utf-8 -*-
"""
Created on 2020-02-14

@author: rg

Modul bitsNbytes

ermöglicht einige Umrechnungs und Darstellungs-Routinen

rg, ab 05.2021

"""
from math import log as logarit

def format_size(flen: int)->str:
    # konveriert eine Byte-Größe (als int) in einen String mit Suffix byte, KB, MB etc.
    #
        """Human friendly file size"""
        unit_list = list(zip(['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB'], [0, 3, 3, 3, 3, 3]))
        if flen > 1:
            exponent = min(int(logarit(flen, 1024)), len(unit_list) - 1)
            quotient = float(flen) / 1024 ** exponent
            unit, num_decimals = unit_list[exponent]
            s = '{:{width}.{prec}f} {}'.format(quotient, unit, width=8, prec=num_decimals )
            s = s.replace(".", ",")
            return s
        elif flen == 1:
            return '  1 byte'
        else: # flen == 0
            return ' 0 bytes'

if __name__ == '__main__':
    print(f"format_size(241) = {format_size(241)}")
    print(f"format_size(51249) = {format_size(51249)}")
    print(f"format_size(1234500678899) = {format_size(12345006789)}")

