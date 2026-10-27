#def print_maatriks(matrix):
#    for el in matrix:
#        print(el)

#def print_peadiagonaal(matrix):
#    suurus = len(matrix)
#    for el in range(suurus):
#        print(matrix[el][el])

def print_korvaldiagonaal(matrix):
    suurus = len(matrix)
    for el in range(suurus):
        print(matrix[el][suurus - 1 - el])


maatriks = [[1,2,3],
            [4, 5, 6],
            [7, 8, 9]]

#print_maatriks(maatriks)
#print(print_peadiagonaal(maatriks))
print(print_korvaldiagonaal(maatriks))