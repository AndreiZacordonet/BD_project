import datetime


def lungime(c):
    if len(str(c)) == 13:
        return True
    else:
        return False


def aflare_sex(c):
    prima_cifra = int(c[0])
    if prima_cifra == 9:
        print('Persoana straina')
        return True
    elif prima_cifra == 7:
        print('Sex barbatesc, persoana străina rezidenta în România')
        return True
    elif prima_cifra == 8:
        print('Sex femeiesc, persoana străina rezidenta în România')
        return True
    elif prima_cifra % 2 == 1:
        print('Sex barbatesc')
        return True
    elif prima_cifra % 2 == 0:
        print('Sex femeiesc')
        return True
    else:
        return False


def data(cnp):
    an = cnp[1:3]
    luna = cnp[3:5]
    zi = cnp[5:7]
    try:
        print(datetime.datetime.strptime(f'{an}{luna}{zi}', '%y%m%d'))
        return True
    except:
        print('data invalida')
        return False


def validare_judet(cnp):
    x = int(cnp[7:9])
    if x in range(1, 47):
        return True
    else:
        return False


def NNN(cnp):
    x = int(cnp[9:12])
    if x in range(1, 999):
        return True


def cifra_control(cnp):
    c = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]
    CNP = list(cnp)
    s = 0
    for i in range(12):
        s = s + c[i] * int(CNP[i])
    if s % 11 == 10:
        control = 1
    else:
        control = s % 11
    if int(cnp[12]) == control:
        return True
    else:
        return False


def Validare_CNP():
    cnp = str(input('Introdu CNP: '))
    c = 0
    while c == 0:
        c = lungime(cnp)
        if c == 1:
            c = aflare_sex(cnp)
            if c == 1:
                c = data(cnp)
                if c == 1:
                    c = validare_judet(cnp)
                    c = validare_judet(cnp)

                    if c == 1:
                        c = cifra_control(cnp)
                        if c == 1:
                            print('CNP corect!')
                        else:
                            print('cifra control gresita')
                            cnp = input('CNP gresit. Introdu CNP: ')
                            c = 0
                    else:
                        print('judet inexistent')
                        cnp = input('CNP gresit. Introdu CNP: ')
                        c = 0
                else:
                    cnp = input('CNP gresit. Introdu CNP: ')
                    c = 0
            else:
                print('prima cifra gresita')
                cnp = input('CNP gresit. Introdu CNP: ')
                c = 0
        else:
            print('lungime gresita')
            cnp = input('CNP gresit. Introdu CNP: ')
            c = 0


Validare_CNP()
