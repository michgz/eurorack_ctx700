
import struct
import subprocess
import sys
import os


U1_TONE = (81, 2)   # Saw lead 2   (CT-X3000 number: 378)
U2_TONE = (81, 2)   # Saw lead 2   (CT-X3000 number: 378)
L_TONE  = (33, 6)   # Fingered bass 1  (CT-X3000 number: 173)


def MakeProgramChange(prgm, bankMSB, bankLSB=0, channel=0):
    return struct.pack("<BBBBBBBB", 0xB0+channel, 0x00, bankMSB, 0xB0+channel, 0x20, bankLSB, 0xC0+channel, prgm)

def MakeSysEx(parameter, data, category=3, memory=3, parameter_set=0, block0=0):
    return bytes.fromhex("F0 44 19 01 7F 01") + struct.pack("<BBHHHHHHHH", category, memory, parameter_set, 0, 0, 0, block0, parameter, 0, 0) + data + bytes.fromhex("F7")

def TwoBytes(X):
    # Expect X to be between 0 and 32267
    return struct.pack("<BB", X%128, X//128)

A = []
# Deal with each sysex.
def DoCmd(X):
    #print(X.hex(" ").upper())
    A.append(X)


# U1 Monophonic
DoCmd(MakeSysEx(114, b'\x01', parameter_set=0))

# U2 Monophonic
DoCmd(MakeSysEx(114, b'\x01', parameter_set=1))

# U2 raise pitch by +1 (1/8 semitone)
U2_PITCH_OFFSET = 2
DoCmd(MakeSysEx(6, TwoBytes(128+U2_PITCH_OFFSET), parameter_set=1, block0=0))
DoCmd(MakeSysEx(6, TwoBytes(128+U2_PITCH_OFFSET), parameter_set=1, block0=1))
DoCmd(MakeSysEx(6, TwoBytes(128+U2_PITCH_OFFSET), parameter_set=1, block0=2))

# U1 no DSP. We need to bypass each effect individually, the overall enable bit doesn't seem
# to have an effect in this case.
DoCmd(MakeSysEx(44, b'\x00', parameter_set=0))
DoCmd(MakeSysEx(86, b'\x01', parameter_set=0, block0=0))
DoCmd(MakeSysEx(86, b'\x01', parameter_set=0, block0=1))
DoCmd(MakeSysEx(86, b'\x01', parameter_set=0, block0=2))
DoCmd(MakeSysEx(86, b'\x01', parameter_set=0, block0=3))

# U2 no DSP. We need to bypass each effect individually, the overall enable bit doesn't seem
# to have an effect in this case.
DoCmd(MakeSysEx(44, b'\x00', parameter_set=1))
DoCmd(MakeSysEx(86, b'\x01', parameter_set=1, block0=0))
DoCmd(MakeSysEx(86, b'\x01', parameter_set=1, block0=1))
DoCmd(MakeSysEx(86, b'\x01', parameter_set=1, block0=2))
DoCmd(MakeSysEx(86, b'\x01', parameter_set=1, block0=3))

# U1 infinite release time
DoCmd(MakeSysEx(20, TwoBytes(0), parameter_set=1, block0=5))

# U2 infinite release time
DoCmd(MakeSysEx(20, TwoBytes(0), parameter_set=1, block0=5))



# Now do what we want with each sysex
if sys.platform.startswith('linux'):
    for AA in A:
        #subprocess.run(['amidi', '-p', 'hw:2,0,0', '--send-hex="{0}"'.format(AA.hex(" ").upper())])
        os.system('amidi -p hw:2,0,0 --send-hex="{0}"'.format(AA.hex(" ").upper()))
for AA in A:
    print(AA.hex(" ").upper())







