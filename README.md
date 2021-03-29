# import-log 


# Français :
Présentation

Un script en python qui vous permet d'importé tous vos log de vos VM/Serveur distant de maniere simple et automatisé.

## Configuration :

* 1° : Il vous faut ajouté votre clé ssh sur le serveur distant si ce n'est deja fait  (ex : https://blog.microlinux.fr/cle-ssh/)

* 2° : Crée un fichier dans le dossier SRV portant le nom de votre serveur (et sans extension).


* 3° : Le seveur doit etre joignable a partir de ce meme nom de fichier que vous vener de crée (si son nom est different de celui joignable sur le reseau vous pouvez l'ajouté dans le fichier /etc/hosts (ex: 192.168.1.2 serveur).

* 4° : Pour finir il vous faut configurer les divers options suivante dans le fichier python si necessaire selon vos besoin (Ligne 9 a 12).

Notes :
* Malgré un script totalement fonctionnel il subsistent encore un bug principale : il n'est pas capable de transferer de gros fichier, en effet le module Paramiko n'est pas tres adapté dans le cas d'une création d'archive. il semblerais que celui ci met fin a la comande des lors que celle ci est bien executé. il vaut donc mieux ne pas depasser quelques MO (au total) afin de pouvoir reussir a importé une archive complete.
* Le module Scan rapide vous permettra de faire un premier scan rapide des fichier importé et de vous notifier des lors q'un certain mot apparait plusieurs fois.

Ajout a venir :
* Gestion des droits sur les fichiers importés.
* correction du bug de l'import de gros fichier (<10Mo).
* 