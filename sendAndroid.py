import nfc
import nfc.snep
import threading
import ndef
import re

class SendToAndroid():

    def __init__(self, usb, data):
        self.data = data
        print("dataseted ", data)
        self.usb = usb
        
    def send_ndef_message(self,llc):
        if self.URLparser() :
            sp = ndef.UriRecord(self.data)
        else :
            sp = ndef.TextRecord(self.data)
        nfc.snep.SnepClient(llc).put_records( [sp] )

    def connected(self,llc):
        threading.Thread(target=self.send_ndef_message, args=(llc,)).start()
        return True

    def released(self, tag):
        time.sleep(1)

    def send(self):
        clf = nfc.ContactlessFrontend(self.usb)
        clf.connect(llcp={'on-connect': self.connected, 'on-released': self.released})
        clf.close()

    def URLparser(self):
        regex = re.compile('(http[s]?:\/\/)?[^\s(["<,>]*\.[^\s[",><]*', re.IGNORECASE)
        return re.match(regex, self.data) is not None
