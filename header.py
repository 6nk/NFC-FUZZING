import random
import re


class Header():

    def __init__(self):
        self.tnf = 0
        self.len_tnf = 0
        self.payload_length = 0
        self.ndef_data = bytearray()
        self. header = {
            'MB' : 1, 'ME' : 1, 'CR' : 0, 'SR' : 1, 'IL' : 0, 'TNF' : '{0:03b}'.format(self.getlenTNF())
        }

    # TODO: Finir la génération du header

    def protocol(self, data,fuzz=None): # RECORD TYPE
        # TODO prendre en compte le type 02 et
        if fuzz == None:
            uri = self.URI_Identifier(data)
            smartp = self.SmartPoster(data)
            if not data or data is " ":
                self.len_tnf = len(bytes([0]))
                return bytes([1,len(data), self.len_tnf]) + bytes([0])
            elif uri :
                self.tnf = bytes([85])
                self.len_tnf = len(self.tnf)
                return bytes([1,len(data), self.len_tnf]) + uri
            elif smartp :
                self.tnf = bytes([83,112])
                self.len_tnf = len(self.tnf)
                return bytes([1,len(data), self.len_tnf]) + smartp
            else :
                txt = self.text(data, "fr")
                self.tnf = txt
                self.len_tnf = len(bytes([84]))
                return bytes([1,len(data), self.len_tnf]) + txt

        rand = random.randint(0, 255)
        return bytes([rand])

    def payload_length(self, data, fuzz=None):
        if fuzz == None:
            return len(data)
        else:
            rand = random.randint(0, 255)
            return bytes([rand])

    def URI_Identifier(self, data):
        URI_Identifier_Code = {'http://www.' : 1, 'https://www.' : 2, 'http://' : 3, 'https://' : 4,
         'tel:' : 5, 'mailto:' : 6, 'ftp://anonymous:anonymous@' : 7, 'ftp://ftp.' : 8,
         'ftps://' : 9, 'sftp://' : 10, 'smb://' : 11, 'nfs://' : 12, 'ftp://' : 13,
         'dav://' : 14, 'news:' : 15, 'telnet://' : 16, 'imap:' : 17, 'rtsp://' : 18,
         'urn:' : 19, 'pop:' : 20, 'sip:' : 21, 'sips:' : 22, 'tftp:' : 23, 'btspp://' : 24,
         'btl2cap://' : 25, 'btgoep://' : 26, 'tcpobex://' : 27, 'irdaobex://' : 28,
         'file://' : 29, 'urn:epc:id:' : 30, 'urn:epc:tag:' : 31, 'urn:epc:pat:' : 32,
         'urn:epc:raw:' : 33, 'urn:epc:' : 34, 'urn:nfc:' : 35}

        if re.search(r'^(?:(?:\+|00)[0-9]+[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})', data):
            return bytes([URI_Identifier_Code['tel:']])
        for key, value in URI_Identifier_Code.items():
            if key in data:
                return bytes([value])
        return None

    def get(self):
        return self.tnf

    def SmartPoster(self, data):
        if data.startswith("SP"):
            return bytes([83, 112])
        # How to simulate it ???
        return None

    def text(self, data, language):
        # TODO : add encoding and language bytes
        # encoding = 0 if UTF-8 and 1 if UTF-16
        # en => 65 6E
        return bytes([84, len(language)]) + language.encode()

    def getlenTNF(self):
        return self.len_tnf

    def bitstring_to_bytes(self, s):
        return int(s, 2).to_bytes(len(s) // 8, byteorder='big')

    def setMB(self):
        self.header['MB'] =  random.randint(0, 255)
    def setME(self):
        self.header['ME'] = random.randint(0, 255)
    def setCR(self):
        self.header['CR'] = random.randint(0, 255)
    def setSR(self):
        self.header['SR'] = random.randint(0, 255)
    def setME(self):
        self.header['IL'] = random.randint(0, 255)
    def setTNF(self):
        rand = random.randint(0,255)
        self.header['TNF'] = '{0:03b}'.format(rand)

    def getNdef_data(self, data):
        # Nous allons partir du principe qu'un message NDEF n'est pas tronqué
        # Il sera donc envoyé en entier.
        if len(data) < 1024 :
            protocol = self.protocol(data)
            header = ''.join(str(value) for key,value in self.header.items())
            self.ndef_data = bytearray(self.bitstring_to_bytes(header)) + protocol + bytearray(data.encode("UTF-8"))
            print(self.ndef_data)
            return self.ndef_data

Header().getNdef_data("salut")
