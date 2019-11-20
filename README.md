 # Information général

NFC-FUZZING est un framework de fuzzing construit pour fuzz applications NFC, basé sur le NFC type 3. 


 # Exigences
 ## Configuration matérielle requise
 
  * [PN532 Breakout Board](http://www.adafruit.com/product/364) ou [PN532 Controller Shield for Arduino(https://www.adafruit.com/product/789)
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

Ce qui devrait donner ce type de résultat : 
![alt text](https://raw.githubusercontent.com/mahff/NFC-FUZZING/i/nlog.png)

# Installation 
Après avoir installé toutes les dépendances, il suffit de cloner ce projet git sur votre ordinateur. 
>$ git clone https://github.com/mahff/NFC-FUZZING

