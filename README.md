# import-log 


# Français :
Préésentation

Un script en python qui vous permet d'importé tous vos log de vos VM/Serveur distant de maniere simple et automatisé

## Configuration :

* 1° : Il vous faut ajouté votre clé ssh sur le serveur distant si ce n'est deja fait :
https://blog.microlinux.fr/cle-ssh/

* 2° : Crée un fichier dans le dossier SRV portant le nom de votre serveur (et sans extension).

* 3° : Le seveur doit etre joignable a partir de ce meme nom de fichier que vous vener de crée (si son nom est different de celui joignable sur le reseau vous pouvez l'ajouté dans le fichier /etc/hosts (ex: 192.168.1.2 serveur).

* 4° : Pour finir il vous faut configurer les divers option suivante dans le fichier python si necessaire selon vos besoin (Ligne 9 a 12).


