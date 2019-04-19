from ai import tah_pocitace, tah


def vyhodnot(pole):
    '''
    Funkce vyhodnotí hrací pole a vrátí znak:
            'x' --> Vyhrál hráč s křížky
            'o' --> Vyhrál hráč s kolečky
            '!' --> Remíza, hrací pole plné, nikdo nevyhrál
            '-' --> Ještě se hraje
    '''
    if len(pole) == 0:
        raise ValueError('Pro vyhodnocení zadáno prázdné pole.')

    if 'xxx' in pole:
        return 'x'
    if 'ooo' in pole:
        return 'o'
    if '-' not in pole:
        return '!'
    else:
        return '-'


def tah_hrace(pole, symbol_hrac, hrac_zadal):
    '''
    Vrátí herní pole po tahu hráče.
    '''
    if len(pole) == 0 or pole.count('-') == 0 or symbol_hrac not in ['x', 'o']:
        raise ValueError('Chyba: Bylo zadáno pole s délkou O, nebo je pole plné, nebo byl zadán jiný herní symbol.')
    try:
        hrac_zadal = int(hrac_zadal)
        if pole[hrac_zadal-1] == '-':
            return tah(pole, hrac_zadal-1, symbol_hrac), 'ok'
        else:
            return pole, 'Pole {} je obsazené, vyber si jiné'.format(hrac_zadal)
    except ValueError:
        return pole, 'Nezadal jsi číslo, ale text, zkus to znovu.'
    except IndexError:
        return pole, 'Nezadal jsi číslo od 1 do {}, zkus to znovu.'.format(len(pole))


def hra():
    '''
    Hra Piškvorky 1D. Na začátku vytvořeno hrací pole, postupně hraje
    uživatel a počítač. Vyhrává ten, kdo první získá 3 své symboly vedle sebe.
    Remíza nastane, když je pole zaplněno.
    '''
    while True:
        try:
            velikost_pole = int(input('Hrajeme 1D-PIŠKORKY. Zadej délku herního pole (od 6 do 50): '))
            if 6 <= velikost_pole <= 50:
                break
        except ValueError:
            pass
    pole = '-'*velikost_pole
    print('Tohle je herní pole.')
    print(pole)
    kolo = 1
    while True:
        symbol_hrac = input('Vyber si křížky "x" nebo kolečka "o": ')
        if symbol_hrac == 'x' or symbol_hrac == 'o':
            break
        else:
            print('Nezadal jsi "x" nebo "o". Zkus to znovu.')
    while True:
        if kolo % 2 == 0:
            pole = tah_pocitace(pole, symbol_hrac)
        else:
            while True:
                hrac_zadal = input('Zadej číslo pole, kde chceš hrát: ')
                pole, vysledek = tah_hrace(pole, symbol_hrac, hrac_zadal)
                if vysledek == 'ok':
                    break
                else:
                    print(vysledek)
        print('{}. kolo: {}'.format(kolo, pole))
        if vyhodnot(pole) == symbol_hrac:  # podle výstupu z funkce "vyhodnot" se vypíše na obrazovku
            print('Vyhrál jsi. Gratuluji.')
            break
        elif vyhodnot(pole) in 'xo':
            print('Vyhrál počítač. Smůla, zkus to znovu.')
            break
        elif vyhodnot(pole) == '!':
            print('Remíza, hrací pole plné, nikdo nevyhrál.')
            break
        else:  # pokud nikdo nevyhrál a na poli jsou volná místa, hraje se dál
            kolo += 1
