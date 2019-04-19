import pytest
from random import randrange

import ai
import piskvorky


# Testy funkce tah_pocitace
def test_tah_PC_na_plne_pole():
    '''
    Test funkce tah_pocitace: po tahu počítače na plné pole dojde
    k vyvolání vyjímky ValueError.
    '''
    with pytest.raises(ValueError):
        ai.tah_pocitace('oxoxoxo', 'x')
        ai.tah_pocitace('a', 'x')
        ai.tah_pocitace('11111111111111111111111111111', 'x')


def test_tah_PC_na_pole_delky_0():
    '''
    Test funkce tah_pocitace: funkce vyvolá vyjímku ValueError,
    pokud dostane pole s délkou 0.
    '''
    with pytest.raises(ValueError):
        ai.tah_pocitace('', 'x')


def test_tah_PC_ruzna_delka_pole():
    '''
    Test funkce tah_pocitace: program se umí vyrovnat s různou délkou hracího
    pole = nedojde k chybě, po tahu počítače se nezmění délka hracího pole
    a nové hrací pole bude obsahovat 1 znak symbolu "x" a zbytek bude prázdný.
    '''
    for delka_pole in range(1, 10000):
        pole = ai.tah_pocitace('-'*delka_pole, 'o')
        assert len(pole) == delka_pole
        assert pole.count('x') == 1
        assert pole.count('-') == delka_pole - 1


def test_tah_PC_nespravny_symbol():
    '''
    Test funkce tah_pocitace: funkce vyvolá vyjímku ValueError,
    pokud dostane jako symbol_hrac něco jiného než "x" nebo "o".
    '''
    for symbol_hrac in 'aBXO10-_*.':
        with pytest.raises(ValueError):
            ai.tah_pocitace('----------', symbol_hrac)


def test_tah_PC_blok_zleva_nebo_zprava():
    '''
    Test funkce tah_pocitace: pocitac najde symbol hráče a zablokuje ho zleva
    nebo zprava.
    '''
    pole = ai.tah_pocitace('---o---o--', 'o')
    assert pole == '--xo---o--' or pole == '---ox--o--'

    pole = ai.tah_pocitace('--xox--o--', 'o')
    assert pole == '--xox-xo--' or pole == '--xox--ox-'

    pole = ai.tah_pocitace('--xo---o--', 'o')
    assert pole == '--xox--o--'

    pole = ai.tah_pocitace('--xox-xo--', 'o')
    assert pole == '--xox-xox-'

    pole = ai.tah_pocitace('---ox--o--', 'o')
    assert pole == '--xox--o--'

    pole = ai.tah_pocitace('--xox--ox-', 'o')
    assert pole == '--xox-xox-'


def test_tah_PC_blok_ostatni():
    '''
    Test funkce tah_pocitace: řeší jiné situace než v předchozím textu tedy
    v hracím poli není situce typu -o- xo- -ox
    '''
    pole = ai.tah_pocitace('o---------', 'o')
    assert pole == 'ox--------'

    pole = ai.tah_pocitace('---------o', 'o')
    assert pole == 'x--------o'

    pole = ai.tah_pocitace('---xox----', 'o')
    assert pole == 'x--xox----'

    pole = ai.tah_pocitace('xoxxox-oxo', 'o')
    assert pole == 'xoxxoxxoxo'

    pole = ai.tah_pocitace('0123456789-', 'o')
    assert pole == '0123456789x'


def test_tah_PC_zapln_pole():
    '''
    Test funkce tah_pocitace: při opakovaném tahu počítač zaplní celé pole
    '''
    pole = '----------'
    for i in range(10):
        pole = ai.tah_pocitace(pole, 'o')
    assert pole == 'xxxxxxxxxx'


# Testy funkce tah
def test_tah_symbol_na_spravna_pozice():
    '''
    Test funkce tah: funkce vrátí herní pole se symbolem na správné pozici
    '''
    pole = ai.tah('----------', 0, 'x')
    assert pole == 'x---------'

    pole = ai.tah('----------', 9, 'o')
    assert pole == '---------o'

    pole = ai.tah('AAAAAAAAAA', 2, 'x')
    assert pole == 'AAxAAAAAAA'


def test_tah_vyjimka():
    '''
    Test funkce tah: funkce vyvolá výjimku:
    --> ValueError - když dostane prázné pole nebo když jako symbol dostane
                    více znaků,
    --> IndexError - když má zapsat symbol na pozici mimo pole, když
                    jako pozice INT,
    --> TypeError - když dostane jako symbol, který má zapsat INT místo STR
    '''
    with pytest.raises(ValueError):
        ai.tah('', 0, 'x')
        ai.tah('---', 0, 'abc')

    with pytest.raises(IndexError):
        ai.tah('---', 10, 'x')
        ai.tah('---------', 'A', 'x')
        ai.tah('---------', 10.5, 'x')

    with pytest.raises(TypeError):
        ai.tah('---------', 0, 5)
        ai.tah('---------', 0, 10.5)


# Testy funkce vyhodnot
def test_vyhodnot_pole():
    '''
    Test funkce vyhodnot: test různých situací a kontrola, že funkce vrátí
    správný symbol:
                'x' --> Výhra - v poli je "xxx"
                'o' --> Výhra - v poli je "ooo"
                '!' --> Remíza, hrací pole plné = není tam "-", nikdo nevyhrál
                '-' --> Nikdo zatím nevyhrál a v poli jsou zatím volná pole,
                        tj. tam alespoň jednou "-"
    '''
    situace_x = ['---xxx---', 'xx-xx-xxx', 'xxx------', 'jklionxxx', 'xoxoxxxoo', '......xxx', '123456xxx', 'xxx', '      xxx']
    situace_o = ['---ooo---', 'oo-oo-ooo', 'ooo------', 'jklixnooo', 'oxoxoooxx', '______ooo', '654321ooo', 'ooo', '      ooo']
    situace_remiza = ['oxoxoxoxo', 'ooxxooxxo', '.........', 'abcdefghijkl', 'XXXPPPOOO', 'x', 'o', '      ']
    situace_hra_pokracuje = ['---------', 'xx-x-o-oo-', 'xoxoxoxox-', 'XXX------', '------OOO', '-', '      -', 'xXx------', 'o0o---oOo']

    for pole in situace_x:
        assert piskvorky.vyhodnot(pole) == 'x'
    for pole in situace_o:
        assert piskvorky.vyhodnot(pole) == 'o'
    for pole in situace_remiza:
        assert piskvorky.vyhodnot(pole) == '!'
    for pole in situace_hra_pokracuje:
        assert piskvorky.vyhodnot(pole) == '-'


def test_vyhodnot_specialni_pole():
    '''
    Test funkce vyhodnot: test různých polí,
    které mohou být zadány jako argument.
    '''
    a = '--xXxO......123-------'
    situace = [a, 'x'*3+'-'*6, str(123456789), ' '*10000]

    for pole in situace:
        assert piskvorky.vyhodnot(pole) in ['x', 'o', '!', '-']

    with pytest.raises(TypeError):
        piskvorky.vyhodnot(10)
        piskvorky.vyhodnot(10.5)

    with pytest.raises(ValueError):
        piskvorky.vyhodnot('')


# Testy funkce tah_hrace
def test_tah_hrace_ruzna_delka_pole():
    '''
    Test funkce tah_hrace: testuje tah hráče na různě velké hrací pole, tah
    hráče je generován náhodně
    '''
    for delka_pole in range(1, 10000):
        pole, vysledek = piskvorky.tah_hrace('-'*delka_pole, 'x', randrange(1, delka_pole+1))
        assert len(pole) == delka_pole
        assert pole.count('x') == 1
        assert pole.count('-') == delka_pole - 1


def test_tah_hrace_na_volnou_pozici():
    '''
    Test funkce tah_hrace: testuje tah hráče na volnou pozici - musí
    vrátit jako výsledek pole a řetězec "ok"
    '''
    pole, vysledek = piskvorky.tah_hrace('abc---abc', 'o', 5)
    assert pole == 'abc-o-abc'
    assert len(pole) == 9
    assert vysledek == 'ok'


def test_tah_hrace_na_obsazenou_pozici():
    '''
    Test funkce tah_hrace: testuje tah hráče na obsazenou pozici - musí vrátit
    původní pole a řetězec 'Pole {} je obsazené, vyber si jiné'
    '''
    pole, vysledek = piskvorky.tah_hrace('abc---abc', 'o', 1)
    assert pole == 'abc---abc'
    assert vysledek == 'Pole 1 je obsazené, vyber si jiné'


def test_tah_hrace_vyjimky():
    '''
    Test funkce tah_hrace: testuje tah hráče po zadání STR místo INT
    jako pozice, kam chce umístit svůj symbol nebo pokud hraje mimo
    herní pole.
    '''
    pole, vysledek = piskvorky.tah_hrace('abc---abc', 'o', 'blbost')
    assert pole == 'abc---abc'
    assert vysledek == 'Nezadal jsi číslo, ale text, zkus to znovu.'

    pole, vysledek = piskvorky.tah_hrace('abc---abc', 'o', 25)
    assert pole == 'abc---abc'
    assert vysledek == 'Nezadal jsi číslo od 1 do 9, zkus to znovu.'


def test_tah_hrace_na_pole_delky_O():
    '''
    Test funkce teh_hrace: testuje tah hráče na pole délky 0
    '''
    with pytest.raises(ValueError):
        piskvorky.tah_hrace('', 'x', 1)


def test_tah_hrace_na_plne_pole():
    '''
    Test funkce tah_hrace: po tahu hráče na plné pole (= znamená, že zde
    není žádné "-") dojde k vyvolání výjimky
    '''
    with pytest.raises(ValueError):
        piskvorky.tah_hrace('xoxoxoxoxoxoxox', 'x', 1)
        piskvorky.tah_hrace('               ', 'x', 1)
        piskvorky.tah_hrace('123456789', 'x', 5)


def test_tah_hrace_dalsi_pripady_vyjimek():
    '''
    Test funkce tah_hrace: testuje nesmyslně zadané argumenty a vyvolání
    vyjímek (další, které nebyly zachyceny výše)
    '''
    with pytest.raises(TypeError):
        piskvorky.tah_hrace(10, 'x', 1)
        piskvorky.tah_pocitace(10.5, 'x', 1)

    with pytest.raises(ValueError):
        piskvorky.tah_hrace('---------', 'X', 1)
        piskvorky.tah_hrace('---------', '', 1)
        piskvorky.tah_hrace('---------', 'abc', 1)
