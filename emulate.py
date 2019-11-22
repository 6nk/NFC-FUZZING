import struct
import nfc
import logging
import ndef
import logging
import subprocess
from header import Header

log = logging.getLogger('main')

class Emulate():
    def __init__(self, usb):
        self.data = ''
        print(self.data)

        self.usb = usb

    def on_startup(self, target):
        print("1")
        target = self.prepare_tag(target)
        print("** waiting for a reader **")
        return target

    def prepare_tag(self, target):
        print("2")
        return self.prepare_tag(target)

    def on_connect(self, tag):
        print("4")
        log.info("tag activated")
        return self.emulate_on_start(tag)

    def emulate_on_start(self, tag):
        print("5")
        return self.emulate_tag(tag)

    def prepare_tag(self, target):
        print("3")
        # if self.data:
        #     # TODO: GENERER LES PREMIERS BYTES AU LIEU DE LES ECRIRE EN DUR DANS LE FICHIER
        #     ndef_data_size = len(self.data)
        #     print("OPTION.DATA prepared ", self.data)
        #     ndef_area_size = ((ndef_data_size + 15) // 16) * 16
        #     ndef_area_size = max(ndef_area_size, 1024)
        #     ndef_data_area = (self.data) \
        #         + bytearray(ndef_area_size - ndef_data_size)
        # else:
        #     ndef_data_area = bytearray(1024)

        if self.data:
            # TODO: GENERER LES PREMIERS BYTES AU LIEU DE LES ECRIRE EN DUR DANS LE FICHIER
            header = Header().getNdef_data(self.data)
            ndef_data_size = len(header)
            print("OPTION.DATA prepared ", self.data)
            ndef_area_size = ((ndef_data_size + 15) // 16) * 16
            ndef_area_size = max(ndef_area_size, 1024)
            ndef_data_area = header \
                + bytearray(ndef_area_size - ndef_data_size)
        else:
            ndef_data_area = bytearray(1024)

        # create attribute data

        attribute_data = bytearray(16)
        attribute_data[0] = 16
        attribute_data[1] = 1
        attribute_data[2] = 1
        nmaxb = len(ndef_data_area) // 16
        attribute_data[3:5] = struct.pack(">H", nmaxb)
        print("nmaxb", nmaxb)
        attribute_data[5:9] = 4 * [0]
        attribute_data[9] = 0
        print("self.options.data", self.data)
        attribute_data[10:14] = struct.pack(">I", len(self.data))

        attribute_data[10] = 1
        print(attribute_data[15])
        attribute_data[14:16] = struct.pack(">H", sum(attribute_data[:14]))
        self.data = attribute_data + ndef_data_area
        print("ndef_data_area", ndef_data_area)
        print("ndef_data_area len",len(ndef_data_area))
        print(self.data)
        target.brty =  "212F"
        idm, pmm, _sys = '03FEFFE011223344', '01E0000000FFFF00', '12FC'
        target.sensf_res = bytearray.fromhex('01' + idm + pmm + _sys)

        return target

    def emulate_tag(self, tag):
        print("6")
        def ndef_read(block_number, rb, re):
            print("7")
            log.debug("tt3 read block #{0}".format(block_number))
            if block_number < len(self.data) / 16:
                first, last = block_number * 16, (block_number + 1) * 16
                block_data = self.data[first:last]
                return block_data

        def ndef_write(block_number, block_data, wb, we=1):
            print("8")
            log.debug("tt3 write block #{0}".format(block_number))
            if block_number < len(self.data) / 16:
                first, last = block_number * 16, (block_number + 1) * 16
                self.data[first:last] = block_data
                print("block_data", block_data)
                return True

        tag.add_service(0x0009, ndef_read, ndef_write)
        tag.add_service(0x000B, ndef_read, lambda: False)
        return True

    def on_release(self, tag):
        print("tag released")
        time.sleep(5)
        return True

    def emulate(self, data):
        self.data = data
        clf = nfc.ContactlessFrontend(self.usb)
        clf.connect(card={'on-startup': self.on_startup, 'on-connect': self.on_connect, 'on-released': self.on_release})
        clf.close()
