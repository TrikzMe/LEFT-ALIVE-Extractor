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

import glob

files = glob.glob('D:\\TrikzMe\\Desktop\\test\\*')
for f in files:
    os.remove(f)
    
    
DARFile     = ("C:\\LEFT ALIVE\\game\\resource\\masterWin64\\GxArchivedFile000.dat")
DARFilename = os.path.splitext(os.path.basename(DARFile))[0]
DARFilePath = os.path.dirname(os.path.abspath(DARFile))
f           = open(DARFile, 'rb')

'''
    magic: 4 bytes
    NB files: 4 bytes
    each file in table lenght = 90B8/73C = 14 bytes long
    table size = 14 x 73C = 90B0
    null: 1CF0 = 73C/4 = 4null bytes for each files

'''

offset      = 0

magic = f.read(4)
NBFiles = struct.unpack("<I", f.read(4))[0]

curr_pos = 8 # Position in file
curr_count = 1 # Current file number

# Create an emtpy dictionary
FilesDict = dict()

# Files table
while (curr_count <= NBFiles):
    # Create an empty list
    FileIDList = list()

    # print(str(curr_count)+'/'+str(NBFiles))
    # strcurr_pos = f.tell()
    # if curr_count == 273:
    # if curr_count in [38,39,40,42,43,44]:
        # print('strcurr_pos: '+str(curr_count)+' - '+str(hex(strcurr_pos)))

    hash = struct.unpack("<I", f.read(4))[0] & 0xffffff
    hash = str(hex(hash)[2:].zfill(6))

    # Add DARFilesData to that list
    FileIDList += [str(curr_count)]
    # Assign that list in the dictionary
    FilesDict[hash] = FileIDList

    f.read(0x10) #14 table line + 4 nulls
    curr_count = curr_count + 1  

#null bytes
curr_count = 1 # Current file number
while (curr_count <= NBFiles):
    f.read(4)
    curr_count = curr_count + 1  

#files datas
curr_count = 1 # Current file number
while (curr_count <= NBFiles):
# for curr_count in range(35,46):
    if DARFilename == "GxArchivedFile000":
        print(str(hex(f.tell())))
        if str(hex(f.tell())) == "0x11e8de":
            f.seek(0x2C36CD6,0)
        if str(hex(f.tell())) == "0x7ec0d8f":
            f.seek(0x83798F5,0)
        if str(hex(f.tell())) == "0x868cea8":
            f.seek(0x86eab0d,0)
        if str(hex(f.tell())) == "0xfe1c6188":
            f.seek(0xFE4345E6,0)
        if str(hex(f.tell())) == "0xfe4ea576":
            f.seek(0xFE4DA64F,0)
    if DARFilename == "GxArchivedFile004":
        print(str(hex(f.tell())))
        if str(hex(f.tell())) == "0x45238":
            f.seek(0x2B4048,0)
        if str(hex(f.tell())) == "0x423092":
            f.seek(0x4323C6,0)

    extension = f.read(3).decode("utf-8")
    # print('"'+extension+'" - '+str(curr_count)+'/'+str(NBFiles)+' -> Curr_pos = '+str(hex(f.tell())))
    # while extension not in ['dt2','dtex','tex','csh', 'csdt', 'cms','hlk', 'mdl']:
        # byte = f.read(3)
    # byte = f.read(3)
    
    # f.seek(0x7D,1)
    f.seek(0x25,1)
    mipmaps = hex(struct.unpack(">b", f.read(1))[0])
    print("mipmaps: ",mipmaps)
    f.seek(0x57,1)
    ZLIB = f.read(4).decode("utf-8") # 0x42494C5A
    FileSize = struct.unpack(">L", f.read(4))[0]
    FileSizeCompressed = struct.unpack(">L", f.read(4))[0]
    print("FileSizeCompressed: ", hex(FileSizeCompressed))
    Unknown = f.read(4)

    # if FileSizeCompressed == FileSize:
        # f.read(FileSizeCompressed)
    # print(hex(FileSize), hex(FileSizeCompressed))

    # f.read(FileSizeCompressed)

    if extension == "tex":
        # save = open("D:\\TrikzMe\\Desktop\\test\\"+str(curr_count)+"."+str(extension),"wb")
        # save.write(zlib.decompress(f.read(FileSizeCompressed)))
        # save.close
    
        data = zlib.decompress(f.read(FileSizeCompressed))
        
        savefile = open("D:\\TrikzMe\\Desktop\\test\\_"+ str(curr_count) +"."+str(extension),"wb")
        savefile.write(data)
        savefile.close
        
        
    # if extension == "mdl":
        # save = open("D:\\TrikzMe\\Desktop\\test\\"+get_random_string(8)+"."+str(extension),"wb")
        # save.write(zlib.decompress(f.read(FileSizeCompressed)))
        # save.close
    # else:
        # f.read(FileSizeCompressed)
    # if extension == "tex":
        print('"'+extension+'" - '+str(curr_count)+'/'+str(NBFiles)+' -> Curr_pos = '+str(hex(f.tell())))
        for FileHash,ID in FilesDict.items():
            if str(ID[0]) == str(curr_count):

                with io.BytesIO(data) as ZlibDecompressed: # instead of writing contents to a file, it's written to a memory buffer.(a chunk of ram)
                    # height = str(ZlibDecompressed.read(2)).split('\\x')
                    # height = ''.join(height[1:]).replace("'","")
                    # width = str(ZlibDecompressed.read(2)).split('\\x')
                    # width = ''.join(width[1:]).replace("'","")
                    width = hex(struct.unpack(">H", ZlibDecompressed.read(2))[0])
                    height = hex(struct.unpack(">H", ZlibDecompressed.read(2))[0])
                    
                    print("width: ",width, " - height: ", height)
                    #DXT1='444453207C00000007100000'+height+'0000'+width+'0000000020000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000040000004458543100000000000000000000000000000000000000000000000000000000000000000000000000000000'


                    DXT1='444453207C00000007100000'+str(width).replace("0x","")+'0000'+str(height).replace("0x","")+'00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200000004100000000000000200000000000FF0000FF0000FF000000000000FF0810400000000000000000000000000000000000'
                    DXT1 = DXT1.encode()    # convert to bytes
                    
                    DX10='444453207C00000007100000'+str(width).replace("0x","")+'0000'+str(height).replace("0x","")+'00000000'+str(mipmaps).replace("0x","")+'0000000000'+str(mipmaps).replace("0x","")+'0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200000000400000044583130000000000000000000000000000000000000000000000000000000000000000000000000000000001B00000003000000000000000100000000000000'
                    DX10 = DX10.encode()    # convert to bytes
                    
                    ZlibData=(ZlibDecompressed.read())[0x0:] # Shift 4 bytes
                    # Write TEX
                    # ZlibDataTex=(ZlibDecompressed.read())[0x0:] # Shift 4 bytes
                    savefile = open("D:\\TrikzMe\\Desktop\\test\\"+ str(FileHash)+"_"+ str(curr_count) +"."+str(extension),"wb")
                    savefile.write(ZlibData)
                    savefile.close

                    # Write DDS
                    # ZlibData=(ZlibDecompressed.read())[0x0:][8:] # Shift 4 bytes
                    # print("FileHash: ",FileHash)
                    save = open("D:\\TrikzMe\\Desktop\\test\\"+str(FileHash)+"_"+ str(curr_count) +".dds","wb")
                    save.write(binascii.unhexlify(DXT1)+ZlibData)
                    # save.write(binascii.unhexlify(DX10)+ZlibData)
                    save.close
    else:
        f.read(FileSizeCompressed)
    curr_count = curr_count + 1   

'''
00 00 00 00 19 01 00 00 32 16 22 8C 11 DA E4 62 08 C2 05 00

26EE0F (script lenght) 2B4047-45238 (between two ZLIBs)

'''

f.close()
