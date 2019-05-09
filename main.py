# -*- coding: utf-8 -*-
import sys, os, psutil, socket
from sys import platform
from winreg import *
import subprocess
import codecs
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM

'''
[*] Target artifacts
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

[*] Tool Set Available
    1. https://ericzimmerman.github.io/#!index.md
    2. https://code.google.com/archive/p/proneer/downloads
'''


AD = "-"
AF_INET6 = getattr(socket, 'AF_INET6', object())
proto_map = {
    (AF_INET, SOCK_STREAM): 'tcp',
    (AF_INET6, SOCK_STREAM): 'tcp6',
    (AF_INET, SOCK_DGRAM): 'udp',
    (AF_INET6, SOCK_DGRAM): 'udp6',
}


def check_os():
    try:
        if platform == 'linux' or platform =='linux2':
            print ('OS System : linux')
        elif platform == 'win32':
            print ('OS System : Windows')
        elif platform == 'darwin':
            print ('OS System : macOS')
        else:
            return 0
    
        return platform
    
    except Exception as e:
        print (e)


def parsing_registry():
    try:
        sys.stdout = open('./output/registry_list.txt','w')
        print ('[+] registry list')
        dic ={0:["HKEY_LOCAL_MACHINE","SOFTWARE\Microsoft\Windows\CurrentVersion","Run"],
            1:["HKEY_CURRENT_USER", "Software\Microsoft\Windows NT\CurrentVersion","Winlogon"],
            2:["HKEY_CURRENT_USER", "Software\Microsoft\Windows NT\CurrentVersion", "Windows"],
            }

        for a in range(len(dic)):
            root_hive = dic[a][0]

            #hive = "HKEY_LOCAL_MACHINE"
            #varSubkey = "SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"
            varSubkey = dic[a][1]#"SOFTWARE\Microsoft\Windows\CurrentVersion"
            if dic[a][0] == "HKEY_LOCAL_MACHINE":
                varReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE) 
                varKey = OpenKey(varReg, varSubkey) 

            if dic[a][0] == "HKEY_CURRENT_USER":
                print (dic[a])
                varReg = ConnectRegistry(None, HKEY_CURRENT_USER) 
                varKey = OpenKey(varReg, varSubkey) 

            for i in range(1024):
                try:
                    keyname = EnumKey(varKey, i)
                    varSubkey2 = "%s\\%s" % (varSubkey, keyname)
                    if keyname == dic[a][2]:
                        print (root_hive + '\\' + varSubkey2)

                        varKey2 = OpenKey(varReg, varSubkey2)
                        try:
                            for j in range(1024):
                                n, v, t = EnumValue(varKey2, j)
                                print (n + '-------' + v)

                        except:
                            errorMsg = "Exception Inner:", sys.exc_info()[0]
                        print ()

                except:
                    errorMsg = "Exception Outter:", sys.exc_info()[0]
                    break

            CloseKey(varKey)
            CloseKey(varReg)
    
    except Exception as e:
        print (e)


def getProcessesList():
    try:
        print ('\n'*2)
        sys.stdout = open('./output/processlist.txt','w')
        print ('[+] process list')
        data = subprocess.check_output(["tasklist"],universal_newlines=True)
        print (data)

    
    except Exception as e:
        print (e)


def recent_list():
    try:
        sys.stdout = open('./output/recent_list.txt','w')
        user_name = (os.environ.get('USERNAME'))
        path = 'C:/Users/'+user_name+'/AppData/Roaming/Microsoft/Windows/Recent'
        for (path, dir, files) in os.walk(path):
            print (path)
            for filename in files:
                print("%s/%s" % (path, filename))
    
    except Exception as e:
        print (e)



def netstat():
    try:
        print ('\n'*2)
        sys.stdout = open('./output/net_stat.txt','w')
        print ('[+] netstat information')
        templ = "%-5s %-30s %-30s %-13s %-6s %s"
        print(templ % (
            "Proto", "Local address", "Remote address", "Status", "PID",
            "Program name"))
        proc_names = {}
        for p in psutil.process_iter(attrs=['pid', 'name']):
            proc_names[p.info['pid']] = p.info['name']
        for c in psutil.net_connections(kind='inet'):
            laddr = "%s:%s" % (c.laddr)
            raddr = ""
            if c.raddr:
                raddr = "%s:%s" % (c.raddr)
            print(templ % (
                proto_map[(c.family, c.type)],
                laddr,
                raddr or AD,
                c.status,
                c.pid or AD,
                proc_names.get(c.pid, '?')[:15],
            ))
    
    except Exception as e:
        print (e)
    

def services():
    try:
        sys.stdout = open('./output/services.txt','w')
        for service in psutil.win_service_iter():
            info = service.as_dict()
            print("%r (%r)" % (info['name'], info['display_name']))
            print("status: %s, start: %s, username: %s, pid: %s" % (
                info['status'], info['start_type'], info['username'], info['pid']))
            print("binpath: %s" % info['binpath'])
            print("")

    except Exception as e:
        print (e)

def mft_parsing():
    try:
        os.system(r"MFTECmd.exe -f C:\$MFT --csv ./output -csvf mft_parsing.csv")
        print ("MFT Paring complete")
    except Exception as e:
        print (e)

def forecopy():
    try:
        os.system(r"forecopy_handy.exe -gpgteixc ./output")
        print ("forecopy complete")
    except Exception as e:
        print (e)

def appcompat():
    #shimcache
    try:
        os.system(r"AppCompatCacheParser.exe --csv ./output -t --f ./output/registry/SYSTEM")
        print ("appcompat complete")
    except Exception as e:
        print (e)

def recyclebin():
    try:
        os.system(r"RBCmd.exe -d C:\$Recycle.Bin --csv ./output")
        print ("recyclebin complete")
    except Exception as e:
        print (e)

def lnkparsing_appdata():
    try:
        os.system(r"LECmd.exe -d %systemdrive%/Users/%username%/AppData/Roaming -all > ./output/appdata_Roaming_lnk.txt")
        print ("appdata/roaming lnkparsing complete")
    except Exception as e:
        print (e)

def lnkparsing_applocal():
    try:
        os.system(r"LECmd.exe -d %systemdrive%/Users/%username%/AppData/local -all > ./output/appdata_local_lnk.txt")
        print ("appdata/local lnkparsing complete")
    except Exception as e:
        print (e)

def lnkparsing_download():
    try:
        os.system(r"LECmd.exe -d %systemdrive%/Users/%username%/download -all > ./output/download_lnk.txt")
        print ("download lnkparsing complete")
    except Exception as e:
        print (e)

def lnkparsing_desktop():
    try:
        os.system(r"LECmd.exe -d %systemdrive%/users/%username%/Desktop > ./output/desktop_lnk.txt")
        print ("tesktop lnkparsing complete")
    except Exception as e:
        print (e)

def jmplist():
    try:
        os.system(r"JLECmd.exe -d C:\ --csv ./output -all")
        print ("download lnkparsing complete")    
    except Exception as e:
        print (e)

def autoruns():
    try:
        os.system(r"autorunsc.exe -c -o ./output/autoruns_list.csv")
        print ("autoruns complete")    
    except Exception as e:
        print (e)



if __name__ == '__main__':
    os_system = check_os()
    if os_system == 'win32':
        try:
            if not(os.path.isdir('./output')):
                os.makedirs(os.path.join('./output'))
        except OSError as e:
            print("Failed to create directory")

        try:
            recent_list()
            parsing_registry()
            getProcessesList()
            netstat()
            services()
            mft_parsing()
            forecopy()
            appcompat()
            recyclebin()
            lnkparsing_appdata()
            lnkparsing_applocal()
            lnkparsing_download()
            lnkparsing_desktop()
            jmplist()
            autoruns()
            sys.stdout.close()
        except Exception as e:
            print (e)
        
    elif os_system == '0':
        print('other operation system')
