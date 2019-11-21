import random
import re


class Header():

    def __init__(self):
        pass

    # TODO: Finir la génération du header


    def TNF(self, data,fuzz=None): # RECORD TYPE
        # TODO prendre en compte le type 02 et
        tnf_list = bytes([0x00,0x01,0x02,0x03,0x04,0x05,0x06])
        rand = random.randint(0, len(tnf_list)-1)
        if fuzz == None:
            uri = self.URI_Identifier(data)
            smartp = self.SmartPoster(data)
            if uri :
                return uri
            elif smartp :
                 return smartp
            else :
                return self.text(data)
        else :
            rand = random.randint(0, 128)
            return bytes([rand])

    def payload_length(self, data, fuzz=None):
        if fuzz == None:
            return len(data)
        else:
            rand = random.randint(0, 128)
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
        for key, value in URI_Identifier_Code.items():
            if key in data:
                return bytes([value])
        return None

    def SmartPoster(self, data):
        pass

    def text(self, data):
        pass

print(Header().TNF("http://google.com"))
