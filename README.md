# IR_CTF_Tools
Parsing artifacts in IR CTF

<br>

### Purpose
    - 침해사고 대응 대회에서 부팅 가능한 시스템 이미지가 주어질 경우 필요한 타겟 정보를 빠르게 수집하기 위함

<br>

### Target artifacts
    1. registry
    2. prefetch
    3. web history (IE, Chrome, Firefox)
    4. recent
    5. services
    6. $mft
    7. shimcache
    8. $Recycle.Bin
    9. lnk (appdata/local, roaming, download, desktop)
    10. jumplist
    11. eventlog
    12. autoruns
    13. processlist
    14. netstat
    
<br>
    
### Used tools
    1. MFTEcmd.exe
    2. forecopy
    3. AppCompatCacheParser.exe
    4. RBCmd.exe
    5. LECmd.exe
    6. JLECmd.exe
    7. autorunsc.exe
