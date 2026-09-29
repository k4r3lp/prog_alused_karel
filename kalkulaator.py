def summa(a, b):
    return a + b
def lahutamine(a, b):
    return a - b
def korrutamine(a, b):
    return a * b
def jagamine(a, b):
    return a / b


x = int(input("Sisesta esimene arv: "))
tehe = input("Sisesta tehte tüüp: ")
y = int(input("Sisesta teine arv: "))

operaatorid = {
    "+": summa,
    "-": lahutamine,
    "*": korrutamine,
    "/": jagamine}
if tehe in operaatorid:
    print("Tulemus:", operaatorid[tehe](x, y))
else:
    print("Sisestasite mittesobiva tehte!")


