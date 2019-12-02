import random
import re


class NdefGeneration():

    def __init__(self):
        self.len_tnf = 0
        self.payload = ''
        self.payload_length = 0
        self.ndef_payload = bytearray()
        self.header = {
            'MB' : 1, 'ME' : 1, 'CR' : 0, 'SR' : 1, 'IL' : 0, 'TNF' : '{0:03b}'.format(0)
        }


    def getTNF(self):
        return self.header['TNF']

    def setTNF(self, tnf):
        print("Set tnf",tnf)
        if isinstance(tnf, int):
            self.header['TNF'] = '{0:03b}'.format(tnf)
        return None

    def getPayload_length(self):
        return self.payload_length

    def setPayload_length(self, payload):
        self.payload_length = payload

    def getlenTNF(self):
        return self.len_tnf

    def setlenTNF(self, len):
        self.len_tnf = len

    def Well_Known(self, payload):
        self.payload = payload
        self.setPayload_length(payload)
        uri = self.Well_known_URI(payload)
        text = self.Well_Known_Text(payload, "fr")
        sp = self.Well_known_URI(payload)
        if uri :
            print(uri)
            return bytes([1,self.getPayload_length()]) + bytes([85]) + uri

        elif text:
            self.header['TNF'] = '{0:03b}'.format(1)
            return bytes([1,self.getPayload_length()+len("en")+1]) + text
        return None

    def Well_known_URI(self, payload):
        Well_known_URI_Code = {'http://www.' : 1, 'https://www.' : 2, 'http://' : 3, 'https://' : 4,
         'tel:' : 5, 'mailto:' : 6, 'ftp://anonymous:anonymous@' : 7, 'ftp://ftp.' : 8,
         'ftps://' : 9, 'sftp://' : 10, 'smb://' : 11, 'nfs://' : 12, 'ftp://' : 13,
         'dav://' : 14, 'news:' : 15, 'telnet://' : 16, 'imap:' : 17, 'rtsp://' : 18,
         'urn:' : 19, 'pop:' : 20, 'sip:' : 21, 'sips:' : 22, 'tftp:' : 23, 'btspp://' : 24,
         'btl2cap://' : 25, 'btgoep://' : 26, 'tcpobex://' : 27, 'irdaobex://' : 28,
         'file://' : 29, 'urn:epc:id:' : 30, 'urn:epc:tag:' : 31, 'urn:epc:pat:' : 32,
         'urn:epc:raw:' : 33, 'urn:epc:' : 34, 'urn:nfc:' : 35}

        if re.search(r'^(?:(?:\+|00)[0-9]+[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})', payload):
            self.setPayload_length(len(payload)+1)
            return bytes([Well_known_URI_Code['tel:']])
        for key, value in Well_known_URI_Code.items():
            if key in payload:
                self.payload = payload.replace(key, "")
                self.setPayload_length(len(payload)-len(key)+1)
                return bytes([value])
        return None

    def Well_Known_Text(self, payload, language):
        # TODO : add encoding and language bytes
        # encoding = 0 if UTF-8 and 1 if UTF-16
        # en => 65 6E
        self.setPayload_length(len(payload))
        return bytes([84, len(language)]) + language.encode()

    def Well_Known_SP(self, payload):
        pass

    def MIME(self, payload):
        pass


    def Absolute_URI(self, payload):
        tmp = re.search(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*', payload)
        if tmp:
            return bytes([3, len(payload)])
        return None

    def Unknow(self, payload):
        pass

    def External(self, payload):
        pass

    def Unchanged(self, payload):
        pass

    def setRandMB(self):
        self.header['MB'] =  random.randint(0, 255)
    def setRandME(self):
        self.header['ME'] = random.randint(0, 255)
    def setRandCR(self):
        self.header['CR'] = random.randint(0, 255)
    def setRandSR(self):
        self.header['SR'] = random.randint(0, 255)
    def setRandME(self):
        self.header['IL'] = random.randint(0, 255)
    def setRandTNF(self):
        rand = random.randint(0,255)
        self.header['TNF'] = '{0:03b}'.format(rand)

    def Empty(self, payload):
        if not payload or payload is " ":

            return bytes([1,len(payload)])
        return None

    def bitstring_to_bytes(self, s):
        return int(s, 2).to_bytes(len(s) // 8, byteorder='big')

    def getNdef_payload(self, payload):
        # Nous allons partir du principe qu'un message NDEF n'est pas tronqué
        # Il sera donc envoyé en entier.
        if len(payload) < 1024 :

            empty = self.Empty(payload)
            well_known = self.Well_Known(payload)
            # mime = self.MIME(payload)
            # uri = self.Absolute_URI(payload)
            # external = self.External(payload)
            # unchanged = self.Unchanged(payload)

            if not payload or payload is " ":
                self.setTNF(0)
                header = ''.join(str(value) for key,value in self.header.items())
                self.ndef_payload = bytearray(self.bitstring_to_bytes(header)) + empty + bytearray(self.payload.encode("UTF-8"))

            elif well_known and not uri:
                self.setTNF(1)
                header = ''.join(str(value) for key,value in self.header.items())
                print(self.header)
                print(header)
                self.ndef_payload = bytearray(self.bitstring_to_bytes(header)) + well_known + bytearray(self.payload.encode("UTF-8"))

            # elif mime :
            #     self.setTNF(2)
            #     header = ''.join(str(value) for key,value in self.header.items())
            #     self.ndef_payload = bytearray(self.bitstring_to_bytes(header)) + mime + bytearray(self.payload.encode("UTF-8"))
            #
            elif uri :
                self.setTNF(3)
                header = ''.join(str(value) for key,value in self.header.items())
                self.ndef_payload = bytearray(self.bitstring_to_bytes(header)) + uri + bytearray(self.payload.encode("UTF-8"))

            # elif external:
            #     self.setTNF(4)
            #     header = ''.join(str(value) for key,value in self.header.items())
            #     self.ndef_payload = bytearray(self.bitstring_to_bytes(header)) + external + bytearray(self.payload.encode("UTF-8"))
            #
            # elif unchanged :
            #     self.setTNF(6)
            #     header = ''.join(str(value) for key,value in self.header.items())
            #     self.ndef_payload = bytearray(self.bitstring_to_bytes(header)) + unchanged + bytearray(self.payload.encode("UTF-8"))
            # print(self.ndef_payload)
            return self.ndef_payload
        return None

# NdefGeneation().getNdef_payload("http://www.google.com")
