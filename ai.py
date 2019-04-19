from random import randrange


def tah_pocitace(pole, symbol_hrac):
    '''
    Vrátí herní pole po tahu počítače.
    '''
    if symbol_hrac == 'x':
        symbol_pocitac = 'o'
    else:
        symbol_pocitac = 'x'

    index_vyskytu = 0
    velikost_pole = len(pole)

    if '-' not in pole or velikost_pole == 0 or symbol_hrac not in ['x', 'o']:
        raise ValueError('Chyba - plné pole, velikost pole = 0 nebo neznámy herní symbol')

    while True:
        # počítač najde symbol protihráče a zablokuje ho zleva či zprava, podle toho, kde je místo
        # když je místo na obou stranách, je volba počítače dána náhodou
        try:
            pozice_symbolu_protihrace = pole.index(symbol_hrac, index_vyskytu)
            if pozice_symbolu_protihrace != 0 and pole[pozice_symbolu_protihrace-1] == '-' and \
            pole[pozice_symbolu_protihrace+1] == '-':
                y = randrange(2)
                if y == 0:
                    return tah(pole, pozice_symbolu_protihrace-1, symbol_pocitac)
                else:
                    return tah(pole, pozice_symbolu_protihrace+1, symbol_pocitac)
            elif pozice_symbolu_protihrace != 0 and pole[pozice_symbolu_protihrace-1] == '-':
                return tah(pole, pozice_symbolu_protihrace-1, symbol_pocitac)
            elif pozice_symbolu_protihrace != 0 and pole[pozice_symbolu_protihrace+1] == '-':
                return tah(pole, pozice_symbolu_protihrace+1, symbol_pocitac)
            else:
                index_vyskytu = pozice_symbolu_protihrace+1
        except ValueError: # nastane, když první tah hráče bude na pole s indexem 0
            cislo_policka = pole.index('-')
            return tah(pole, cislo_policka, symbol_pocitac)
        except IndexError: # nastane, když první tah hráče bude na poslední pole
            cislo_policka = pole.index('-')
            return tah(pole, cislo_policka, symbol_pocitac)


def tah(pole, cislo_policka, symbol):
    '''
    Vrátí herní pole se symbolem umístěným na danou pozici
    '''
    if len(pole) == 0 or len(symbol) != 1:
        raise ValueError('Chyba: Pole má velikost 0 nebo zadaný symbol není jeden znak.')
    if cislo_policka not in range(len(pole)):
        raise IndexError('Chyba: Zadaná pozice je mimo hrací pole.')

    return pole[:cislo_policka] + symbol + pole[cislo_policka+1:]
