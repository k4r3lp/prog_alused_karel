height = 5


for i in range(height):
    stars = "*" * (i + 1)
    print(stars)

def kool(height):
    for i in range(height):
        spaces = " " * (height - i)
        stars = "*" * (i + 1)
        print(spaces, stars)
kool(7)

def kool2(height, sumbol):
    for i in range(height):
        spaces = " " * (height - i)
        print(spaces, sumbol * (i * 2 -1))
kool2(7, "*")


#def kool3(korgus, sumbol):
#   for i in range(korgus):
#        print((korgus - i) * " " + (i * 2 - 1) * sumbol)
#kool3(6, "*")



#def kool3(korgus, sumbol):
#    for i in range(korgus):
#        print((korgus - i) * " " + (i * 2 + 1) * sumbol, " " * (5 - i) + "|" +  (korgus - i) * " " + (i * 2 + 1) * sumbol)
#kool3(6, "*")

def kool3(korgus, sumbol):
    for i in range(korgus):
        print((korgus - i) * " " + (i * 2 + 1) * sumbol, " " * (5 - i) + "|" +  " " * (height -5) + " " * (i +1) + (7 -i -1) * sumbol + (6 -i -1) * sumbol)
kool3(6, "*")