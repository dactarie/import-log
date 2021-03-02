f = open('srv/cible1', 'r')

nbr_ligne = 0
for line in f:
    nbr_ligne += 1

print('Nombre de lignes: ', + nbr_ligne)
