# -*- coding: utf-8 -*-
import binascii
import sys
import os
import struct
import zlib
import io 

import random
import string

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def writeHeader(TEXFile, header):
    # ft = open(TEXFile, "rb").read()

    h=(binascii.hexlify(ft))[0x0:][8:] # Shift 4 bytes

    file = open(TEXFile.split(".")[0]+".dds","wb")
    file.write(binascii.unhexlify(header+h))
    file.close

def convertTEXToDDS(TEXFile):
    # TEXFile='D:\\TrikzMe\\Desktop\\test\\abufvxwg.tex'
    tf = open(TEXFile, 'rb')
    height = str(tf.read(2)).split('\\x')
    height = ''.join(height[1:]).replace("'","")
    width = str(tf.read(2)).split('\\x')
    width = ''.join(width[1:]).replace("'","")

    DXT1='444453207C00000007100000'+height+'0000'+width+'0000000020000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000040000004458543100000000000000000000000000000000000000000000000000000000000000000000000000000000'
    DXT1 = DXT1.encode()    # convert to bytes
    # print(DXT1)
    writeHeader(TEXFile, DXT1)

'''convertTEXToDDS'''
# TEXFile='D:\\TrikzMe\\Desktop\\test\\abufvxwg.tex'
# convertTEXToDDS(TEXFile)


DARFile     = ("C:\\LEFT ALIVE\\game\\resource\\masterWin64\\GxArchivedFile002.dat")
DARFilePath = os.path.dirname(os.path.abspath(DARFile))
f           = open(DARFile, 'rb')
offset      = 0
# GxArchivedFile001
# f.seek(0x424E8,0)
# archivefileSize = 0x1981DAB76
# GxArchivedFile002
f.seek(0x20A38,0)
archivefileSize = 0x1160F938C
# GxArchivedFile004
# f.seek(0xADA8,0)
# archivefileSize = 0x55304E


# f.seek(0x158BB4616,0)
# print(hex(f.tell()))
# extension = f.read(3).decode("utf-8")
# print('"'+extension+'"')
# f.seek(0x7D,1)
# print(hex(f.tell()))
# ZLIB = f.read(4).decode("utf-8") # 0x42494C5A
# print(ZLIB)
# FileSize = struct.unpack(">L", f.read(4))[0]
# FileSizeCompressed = struct.unpack(">L", f.read(4))[0]
# Unknown = f.read(4)
# print(hex(FileSize), hex(FileSizeCompressed))

# save = open("D:\\TrikzMe\\Desktop\\test\\"+get_random_string(8)+"."+str(extension),"wb")
# save.write(zlib.decompress(f.read(FileSizeCompressed)))
# save.close

while offset != archivefileSize:

    print(hex(f.tell()))
    extension = f.read(3).decode("utf-8")
    print('"'+extension+'"')
    while extension not in ['','dt2','dtex','tex','csh', 'csdt', 'cms','hlk', 'mdl']:
        byte = f.read(3)

    f.seek(0x7D,1)
    # print(hex(f.tell()))
    ZLIB = f.read(4).decode("utf-8") # 0x42494C5A
    # print(ZLIB)
    FileSize = struct.unpack(">L", f.read(4))[0]
    FileSizeCompressed = struct.unpack(">L", f.read(4))[0]
    Unknown = f.read(4)
    if FileSizeCompressed == FileSize:
        f.read(FileSizeCompressed)
    # print(hex(FileSize), hex(FileSizeCompressed))

    # if extension == "tex":
        # data = zlib.decompress(f.read(FileSizeCompressed))

        # with io.BytesIO(data) as ZlibDecompressed: # instead of writing contents to a file, it's written to a memory buffer.(a chunk of ram)
            # height = str(ZlibDecompressed.read(2)).split('\\x')
            # height = ''.join(height[1:]).replace("'","")
            # width = str(ZlibDecompressed.read(2)).split('\\x')
            # width = ''.join(width[1:]).replace("'","")

            # DXT1='444453207C00000007100000'+height+'0000'+width+'0000000020000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000040000004458543100000000000000000000000000000000000000000000000000000000000000000000000000000000'
            # DXT1 = DXT1.encode()    # convert to bytes
            
            # ZlibData=(ZlibDecompressed.read())[0x0:][8:] # Shift 4 bytes

            # save = open("D:\\TrikzMe\\Desktop\\test\\"+get_random_string(8)+".dds","wb")
            # save.write(binascii.unhexlify(DXT1)+ZlibData)
            # save.close
    else:
        if extension == "mdl":
            print('"'+extension+'"')
            save = open("D:\\TrikzMe\\Desktop\\test\\"+get_random_string(8)+"."+str(extension),"wb")
            save.write(zlib.decompress(f.read(FileSizeCompressed)))
            save.close
        else:
            f.read(FileSizeCompressed)
        # if not extension == "tex":
            # print('"'+extension+'"')
            # save = open("D:\\TrikzMe\\Desktop\\test\\"+get_random_string(8)+"."+str(extension),"wb")
            # save.write(zlib.decompress(f.read(FileSizeCompressed)))
            # save.close
    print(hex(f.tell()))
    offset += FileSizeCompressed + 0x4

f.close()
