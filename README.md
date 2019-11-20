Information général
===================
NFC-FUZZING est un framework de fuzzing construit pour fuzz applications NFC, basé sur le NFC type 3. 


Exigences
============
  # Configuration matérielle requise
  * [PN532 Breakout Board](http://www.adafruit.com/product/364) ou [PN532 Controller Shield for Arduino] (https://www.adafruit.com/product/789)
  * [FTDI Cable](http://www.adafruit.com/products/70)
  # Dépendances 
  * [nfcpy](https://nfcpy.readthedocs.io/en/latest/)
  * [adb](http://developer.android.com/tools/help/adb.html) 
  * [Libusb](https://pypi.org/project/libusb/)
  * [pyserial](https://pyserial.readthedocs.io/en/latest/index.html)
  * [pure-python-adb](https://pypi.org/project/pure-python-adb/)
  
  Pour l'installation de ces différentes dépendances, il suffit de :
  >$ sudo pip install [nom_package]
