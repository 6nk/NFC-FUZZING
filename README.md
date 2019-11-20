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
  
 ##### NB : Il faut au préalable avoir installer [python3-pip](https://pip.pypa.io/en/stable/installing/), avec :
 >$ sudo apt install python3-pip pour une distribution linux basé sur Debian. 
 
 ##### NB : Certains Smartphone android requierent java: default-jdk
 >$ sudo apt install default-jdk

# Installation 
Après avoir installé toutes les dépendances, il suffit de cloner ce projet git sur votre ordinateur. 
>$ git clone https://github.com/mahff/NFC-FUZZING

# Détecter le module NFC
### Installation de [libnfc](https://github.com/nfc-tools/libnfc)
On peut utiliser [libnfc](https://github.com/nfc-tools/libnfc) comme outil permettant de s'assurer que le module NFC est correctement reconnu par l'ordinateur. 
Pour ce faire, on installe [libnfc](https://github.com/nfc-tools/libnfc/releases/tag/libnfc-1.7.0) : 
>$ wget https://github.com/nfc-tools/libnfc/releases/download/libnfc-1.7.0/libnfc-1.7.0.tar.bz2
Ensuite, on dézippe l'archive :
>$ tar -xvjf libnfc-1.7.0.tar.bz2
>$ cd cd libnfc-1.7.0

### Configuration 
Taper : 
>$ ./configure --prefix=/usr --sysconfdir=/etc
Créer le dossier de configuration : 
>$ sudo mkdir /etc/nfc/
Créer le fichier de configuration :
>$ sudo nano /etc/nfc/libnfc.conf
Et ajouter ceci dans le fichier :
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
#device.name = "_PN532_SPI"
#device.connstring = "pn532_spi:/dev/spidev0.0:500000"
#device.name = "_PN532_I2c"
#device.connstring = "pn532_i2c:/dev/i2c-1"
device.name = "_PN532_UART"
device.connstring = "pn532_uart:/dev/ttyUSB0" 
```




