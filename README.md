 # Information général

NFC-FUZZING est un framework de fuzzing construit pour fuzz applications NFC, basé sur le NFC type 3. 


 # Exigences
 ## Configuration matérielle requise
 
  * [PN532 Breakout Board](http://www.adafruit.com/product/364) ou [PN532 Controller Shield for Arduino] (https://www.adafruit.com/product/789)
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
 
 ##### NB : Certains Smartphone android requierent java : [default-jdk] 
 >$ sudo apt install default-jdk
