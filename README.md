 # Information générale

NFC-FUZZING est un framework de fuzzing construit pour fuzz applications NFC, basé sur le NFC type 3.


 # Exigences
 ## Configuration matérielle requise

  * [PN532 Breakout Board](http://www.adafruit.com/product/364) ou [PN532 Controller Shield for Arduino](https://www.adafruit.com/product/789)
  * [FTDI Cable](http://www.adafruit.com/products/70)

## Dépendances

  * [nfcpy](https://nfcpy.readthedocs.io/en/latest/)
  * [adb](http://developer.android.com/tools/help/adb.html)
  * [Libusb](https://pypi.org/project/libusb/)
  * [pyserial](https://pyserial.readthedocs.io/en/latest/index.html)
  * [pure-python-adb](https://pypi.org/project/pure-python-adb/)

  Pour l'installation de ces différentes dépendances, il vous suffit de taper:
  >$ sudo pip install [nom_package]

 ###### NB : Il faut au préalable avoir installer [python3-pip](https://pip.pypa.io/en/stable/installing/), avec :
 >$ sudo apt install python3-pip pour une distribution linux basé sur Debian.

 ###### NB : Certains Smartphone android requierent java: default-jdk
 >$ sudo apt install default-jdk

 # Montage
 * Préparer Adafruit PN532 RFID/NFC Shield
 Ce montage est réalisé en utilisant l'UART et peut fonctionner à la fois avec [PN532 Breakout Board](http://www.adafruit.com/product/364) et [PN532 Controller Shield for Arduino(https://www.adafruit.com/product/789)

Pour utiliser UART sur Adafruit PN532 RFID/NFC Shield, procédez comme suit :

 * SEL0 doit être OUVERT et SEL1 FERMÉ.
 * Faire fondre une goutte de soudure pour faire un pont entre les pastilles de cuivre à SEL1.
 ###### NB : Une fois cette opération effectuée, le module NFC ne fonctionnera plus avec Arduino, puisque le module NFC n'est plus configuré pour communiquer avec SPI ou I2C. Si vous voulez revenir à l'utilisation du bouclier NFC avec l'arduino, vous devrez annuler les modifications que vous avez apportées à SEL1.
 ###### NB : Sur la version de l'Adafruit PN532 RFID/NFC Shield v1.0. SEL0 et SEL1 sont inversés sur la sérigraphie, donc SEL0 est en fait SEL1 et vice versa.

* Connecter le câble FTDI au module NFC
 #### Méthode 1:
  - Connecter 5V de la carte FTDI à 5V sur le 5V du module NFC.
  - Connecter GNG de la carte FTDI au GND du module NFC.
  - Connecter TX de la carte FTDI à SS sur le module NFC.
  - Connecter RX de la carte FTDI à MOSI sur le module NFC.
 #### Méthode 2:
  - Connecter 5V de la carte FTDI à 5V sur le 5V du module NFC.
  - Connecter GNG de la carte FTDI au GND du module NFC.
  - Connecter TX de la carte FTDI à SCL sur le module NFC.
  - Connecter RX de la carte FTDI à SDA sur le module NFC.
 #### Connecter le câble FTDI à l'ordinateur

# Détecter le module NFC
### Installation de [libnfc](https://github.com/nfc-tools/libnfc)
On peut utiliser [libnfc](https://github.com/nfc-tools/libnfc) comme outil permettant de s'assurer que le module NFC est correctement reconnu par l'ordinateur.
* Pour ce faire, on installe [libnfc](https://github.com/nfc-tools/libnfc/releases/tag/libnfc-1.7.0) :
>$ wget https://github.com/nfc-tools/libnfc/releases/download/libnfc-1.7.0/libnfc-1.7.0.tar.bz2
* Ensuite, on dézippe l'archive :
>$ tar -xvjf libnfc-1.7.0.tar.bz2

>$ cd cd libnfc-1.7.0

### Configuration
* Taper :
>$ ./configure --prefix=/usr --sysconfdir=/etc
* Créer le dossier de configuration :
>$ sudo mkdir /etc/nfc/
* Créer le fichier de configuration :
>$ sudo nano /etc/nfc/libnfc.conf
* Et ajouter ceci dans le fichier :

```# Allow intrusive auto-detection (default: false)
# Warning: intrusive auto-detection can seriously disturb other devices
# This option is not recommended, user should prefer to add manually his device.
allow_intrusive_scan = true

# Set log level (default: error)
# Valid log levels are (in order of verbosity): 0 (none), 1 (error), 2 (info), 3 (debug)
# Note: if you compiled with --enable-debug option, the default log level is "debug"
log_level = 1

# Manually set default device (no default)
# To set a default device, you must set both name and connstring for your device
# Note: if autoscan is enabled, default device will be the first device available in device list.
device.name = "_PN532_UART"
device.connstring = "pn532_uart:/dev/ttyUSB0"
```

### Compiler nfclib
Pour compiler libnfc, il vous suffit d'entrer les commandes suivantes :
>$ sudo make clean

>$ sudo make install all

### Tester
Avec libnfc construit et correctement configuré, vous pouvez exécuter la commande suivante pour obtenir l'ID unique des étiquettes, en plaçant une carte NFC sur le module :
>$ cd examples

>$ sudo ./nfc-poll

Ce qui devrait donner un résultat similaire :

```
nfc-poll uses libnfc 1.7.1
NFC reader: pn532_uart:/dev/ttyUSB0 opened
NFC device will poll during 30000 ms (20 pollings of 300 ms for 5 modulations)
ISO/IEC 14443A (106 kbps) target:
    ATQA (SENS_RES): 00  42  
       UID (NFCID1): 02  c4  00  45  02  d0  e3  
      SAK (SEL_RES): 20  
                ATS: 78  00  50  02  
nfc_initiator_target_is_present: Target Released
Waiting for card removing...done.
```
### Erreurs rencontrées
Durant ce projet, je suis tombé sur quatre types d'erreurs en utilisant libnfc, notamment les fonctionnalités nfc-poll et nfc nfc-list :
##### Erreur 1
```
Exemple de rendu
```
Depuis la version 3.1 du noyau Linux, certans modules ne sont plus pris en charge pour utiliser libnfc. Une des solutions consiste à empêcher le noyau de charger automatiquement ces modules, en les blacklistant dans un fichier conf modprobe. Ce fichier est fourni dans l'archive libnfc :

>$ sudo cp contrib/linux/blacklist-libnfc.conf /etc/modprobe.d/blacklist-libnfc.conf
##### Erreur 2
```
nfc-poll uses libnfc 1.7.1
error	libnfc.driver.pn532_uart	pn53x_check_communication error
nfc-poll: ERROR: Unable to open NFC device.
```
Cette erreur est souvent dûe au fait que le module est mal connecté, je vous invite à relire la partie concernant le montage.
##### Erreur 3
```
nfc-poll uses libnfc 1.7.1
error	libnfc.driver.pn532_uart	Invalid serial port: /dev/ttyUSB0
nfc-poll: ERROR: Unable to open NFC device.
```
Les droits d'accès au fichier du port série : /dev/ttyUSB0 est à l'origine de ce problème. Un simple [chmod] sur le dit port série résoudra l'erreur :
>$ sudo chmod 777 /dev/ttyUSB0
##### Erreur 4
```
nfc-list uses libnfc 1.7.1
error libnfc.driver.pn532_uart  Unable to claim USB interface (Device or resource busy)
nfc-list: ERROR: Unable to open NFC device: pn532_uart:/dev/ttyUSB0
```
La bibliothéque libnfc n'a pas suffisamment de temps pour communiquer avec le module NFC et renvoit cette erreur. L'une des solutions et l'ajout de résistances de 220 Ohm ou 500 Ohm entre :
  - Le TX de la carte FTDI et [SS] ou [SCL] du module NFC.
  - Le RX de la carte FTDI et [MOSI] ou [SDA] du module NFC.
L'autre solution consiste à regarder si il n'existe pas plusieurs modules dans la liste des modules du noyau chargés en mémoire :
>$ sudo lsmod

On regarde les modules pn5xx, éventuellement avec :

>$ sudo lsmod | grep "pn"

Si il s'avère qu'il y a bien plusieurs modules, il suffit de se référer à la solution de l'erreur 1 et bloquer les modules non souhaités.


# Installation
Après avoir installé toutes les dépendances, il suffit de cloner ce projet git sur votre ordinateur.
>$ git clone https://github.com/mahff/NFC-FUZZING

# Configuration du téléphone
Il y a quelques réglages sur android qui font du fuzzing une expérience beaucoup plus agréable.

* Activez le débogage USB via les " Options du développeur ". Si vous ne voyez pas cette option, allez dans " À propos du téléphone " et appuyez plusieurs fois sur le " Numéro de compilation ".

* Activez "Rester éveillé" dans les "Options du développeur".

* Réglez "Verrouillage de l'écran" sur Aucun sous "Sécurité".

# Configuration de la ST25R3911B-DISCO
À partir de [STSW-ST25R001](https://www.st.com/content/st_com/en/products/embedded-software/st25-nfc-rfid-software/stsw-st25r001.html), installer le logiciel de contrôle de la carte, en suivant les instructions. Un tutorial de la prise en main du logiciel est disponible sur [youtube](https://www.youtube.com/watch?v=PjM-Fs2lo3c). 

# Architecture du code
.
 * [data](./data)
   * [Browser](./data/Browser)
   * [Dialer](./data/Dialer)
   * [Maps](./data/Maps)
   * [Maps-AAR](./data/Maps-AAR)
   * [Maps](./data/Maps)
   * [Play](./data/Play)
   * [Smart-Poster1](./data/Smart-Poster1)
   * [SMS](./data/SMS)
   * [Text1](./data/Text1)
 * [docs](./docs)
 * [adb.py](./adb.py)
 * [emulate.py](./emulate.py)
 * [\_\_init\_\_.py](./__init__.py)
 * [mFuzz.py](./mFuzz.py)
 * [NdefGeneration.py](./NdefGeneration.py)
 * [sendAndroid.py](./sendAndroid.py)
 * [README.md](./README.md)
1 dossier, 17 files

# Usage
Pour utiliser le fuzzer, il suffit de connecter les différents éléments à l’ordinateur, à savoir le module NFC, lesmartphone ou le ST25R3911B. Ensuite, dans un terminal taper :

### Mode émulation 
>$ python \_\_init\_\_.py -p PAYLOAD -emulate. 

Permet d'émuler et tester le bon fonctionnement de la génération du message NDEF et l'envoie du message

### Mode normale
>$ python \_\_init\_\_.py -p PAYLOAD -normal. 

A pour but de vérifier l'envoie du message. 
### Mode fuzzing
>$ python \_\_init\_\_.py -p PAYLOAD -fuzz [-adb]. 

Permet de lancer 10 fuzzing à la suite. On peut mettre l'option -adb pour récupérer l'historique d'événements du smartphone android. 
### Mode fuzzing du champ
>$  python \_\_init\_\_.py -p PAYLOAD -field CHAMP [-adb]. 

Permet de lancer 10 fuzzing d'un des en-têtes à la suite. On peut mettre l'option -adb pour récupérer l'historique d'événements du smartphone android.
### Mode boucle
>$ python \_\_init\_\_.py -loop NOMBRE [-adb]. 

Fuzzer N fois le message NDEF à partir d'un jeu de données valide. On peut mettre l'option -adb pour récupérer l'historique d'événements du smartphone android. 


# Mail
[AMHIYEN Mahfoud](mailto:mahfoudamhiyen?subject=[GitHub]%20Fuzz%20NFC)
