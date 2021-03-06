import concurrent, csv, json, os, re, sys, concurrent.futures, subprocess, time
__version__ = 1.0

def ScanPC(PCID):
    plugins = []
    FNULL = open(os.devnull, 'w')
    response = subprocess.call("ping -n 1 " + PCID, stdout=FNULL)

    # and then check the response...
    if response == 0:

        global verbose
        connected = False

        try:
            os.chdir(r'\\' + f'{PCID}' + r'\\C$\\users\\')
            dir = r'\\' + f'{PCID}' + r'\\C$\\users\\'
            connected = True
        except:
            try:
                os.chdir(r'\\' + f'{PCID}' + r'\\C$\\Documents and Settings\\')
                dir = r'\\' + f'{PCID}' + r'\\C$\\Documents and Settings\\'
                connected = True
            except:
                if verbose:
                    print(f"Can't connect to {PCID}")

        if connected:
            try:
                for user in os.listdir(os.getcwd()):

                    try:
                        chromeDir = dir + user + r'\\AppData\\Local\\Google\\Chrome\\User Data\\'
                        os.chdir(chromeDir)
                        for chromeProfile in os.listdir(chromeDir):
                            if "Default" in chromeProfile or "Profile" in chromeProfile:
                                try:
                                    ExtDir = chromeDir + chromeProfile + r'\\Extensions\\'
                                    os.chdir(ExtDir)
                                    for extensionHash in os.listdir():
                                        ExtHashDir = ExtDir + extensionHash + r'\\'
                                        for extensionVer in os.listdir(ExtHashDir):
                                            try:
                                                extensionFolderVer = ExtHashDir + extensionVer + r'\\'
                                                os.chdir(extensionFolderVer)
                                                try:
                                                   with open('manifest.json') as json_file:
                                                        data = json.load(json_file)
                                                        if '__MSG' in data['name']:
                                                            hasLocalisation = re.search(r'__MSG_([a-z0-9_-]+)__', data['name'], re.M | re.I)
                                                            if hasLocalisation:
                                                                try:
                                                                    localisationFolder = extensionFolderVer + r'_locales\en_US\\'
                                                                    os.chdir(localisationFolder)
                                                                    for localisation in os.listdir(localisationFolder):
                                                                        if "messages.json" in localisation:
                                                                            with open(localisationFolder + localisation) as json_file2:
                                                                                data2 = json.load(json_file2)
                                                                                try:
                                                                                    if data2[hasLocalisation.group(1)]['message']:
                                                                                        name = data2[hasLocalisation.group(1)]['message']
                                                                                except:
                                                                                    if data2[hasLocalisation.group(1).lower()]['message']:
                                                                                        name = data2[hasLocalisation.group(1).lower()]['message']

                                                                                plugins.append([name, PCID, user, ExtHashDir])
                                                                except:
                                                                    try:
                                                                        localisationFolder = extensionFolderVer + \
                                                                                             r'_locales\en\\'
                                                                        os.chdir(localisationFolder)
                                                                        for localisation in os.listdir(localisationFolder):
                                                                            if "messages.json" in localisation:
                                                                                with open(localisationFolder + localisation) as json_file2:
                                                                                    data2 = json.load(json_file2)
                                                                                    try:
                                                                                        if data2[hasLocalisation.group(1)]['message']:
                                                                                            name = data2[hasLocalisation.group(1)]['message']
                                                                                    except:
                                                                                        if data2[hasLocalisation.group(1).lower()]['message']:
                                                                                            name = data2[hasLocalisation.group(1).lower()]['message']

                                                                                    plugins.append(
                                                                                        [name, PCID, user, ExtHashDir])
                                                                    except:
                                                                        if verbose:
                                                                            print(f'english localisation not found for {extensionHash}' + f' {chromeProfile}' + f' {user}' + f' {PCID}')
                                                        else:
                                                            if verbose:
                                                                print('\t\t\t\t' + data['name'])
                                                            plugins.append([data['name'], PCID, user, ExtHashDir])
                                                except:
                                                    if verbose:
                                                        print('manifest.json not found for {extensionHash}' + f' {chromeProfile}' + f' {user}' + f' {PCID}')
                                            except:
                                                if verbose:
                                                    print(f'No version found for extensions {extensionHash}' + f' {chromeProfile}' + f' {user}' + f' {PCID}')
                                except:
                                    if verbose:
                                        print('No Chrome extensions found for' + f' {chromeProfile}' + f' {user}' + f' {PCID}')
                    except:
                        if verbose:
                            print('Chrome directory not found for' + f' {user}' + f' {PCID}')
            except:
                if verbose:
                    print('Error: ' + f' {PCID}')
    return plugins


verbose = False

def main():
    startTime = time.time()
    print("Chrome Plugin scanner script")

    global verbose
    extensions = []
    PCS = []
    origDir = os.getcwd()
    _threads = 0
    _timeout = 0
    _chunksize = 0
    _file = 'systems.txt'
    _continue = True;
    _destination = 'results.csv'
    _target = ""

    for i, arg in enumerate(sys.argv):
        if '-t' in arg or '-threads' in arg:
            _threads = int(sys.argv[i+1])
        elif '-c' in arg or '-chunksize' in arg:
            _chunksize = int(sys.argv[i+1])
        elif '-T' in arg or '-timeout' in arg:
            _timeout = int(sys.argv[i+1])
        elif '-sf' in arg or '-sourcefile' in arg:
            _file = str(sys.argv[i+1])
        elif '-s' in arg or '-Source' in arg:
            _target = str(sys.argv[i+1])
        elif '-o' in arg or '-output' in arg:
            _destination = str(sys.argv[i+1])
        elif '-v' in arg or '-verbose' in arg:
            verbose = True
        elif '-h' in arg or '-H' in arg or '-help' in arg:
            print('example: python pluginScanner.py -s SMHPC27429 -o SMHPC27429.csv')
            print('example: python pluginScanner.py -sf allsmhpcs.txt -o SMH.csv')
            print('-t #, -threads # total ammount of threads to use')
            print('-c #, -chunksize # total ammount of PC\'s each thread should scan')
            print('-T #, -timeout # how long to spend on scanning each pc before ending the scan')
            print('-o [file], -output [file] file location/name, defaults is results.csv')
            print('-v, will provide more information on the scan while it\'s running')
            print('-s [PC Name], -source [PC Name] the name of the PC')
            print('-sf [file], -sourcefile [file] the location of the file containing a list of the systems')
            _continue = False;

    if _continue:
        if _threads == 0:
            _threads = 50
        if _timeout == 0:
            _timeout = 3
        if _chunksize == 0:
            _chunksize = 50

        if _target == "":
            systems = os.getcwd() + f'\\{_file}'
            with open(systems) as f:
                content = f.readlines()
                for i, PC in enumerate(content):
                    PCS.append(PC.rstrip())

            with concurrent.futures.ProcessPoolExecutor(max_workers=_threads) as pool:
                for i, res in enumerate(pool.map(ScanPC, PCS, chunksize=_chunksize)):
                    try:
                        if verbose:
                            print(f"Finished scanning {PCS[i]} {i + 1}/{len(content)}")
                        extensions += res
                    except:
                        if verbose:
                            print(f"timeout, couldn't scan {PCS[i]}")

        else:
            PCS.append(_target.rstrip())
            extensions += ScanPC(_target)



        os.chdir(origDir)

        file_name = _destination
        if os.path.isfile(file_name):
            expand = 1
            while True:
                expand += 1
                new_file_name = file_name.split(".csv")[0] + str(expand) + ".csv"
                if os.path.isfile(new_file_name):
                    continue
                else:
                    file_name = new_file_name
                    with open(file_name, 'w') as myfile:
                        writer = csv.writer(myfile, lineterminator='\n')
                        writer.writerows(extensions)
                        print(file_name)
                    break
        else:
            with open(file_name, 'w') as myfile:
                writer = csv.writer(myfile, lineterminator='\n')
                writer.writerows(extensions)
                print('Results in ' + file_name)

        print('done')
        print('The script took {0} second!'.format(time.time() - startTime))


if __name__ == "__main__":
    sys.exit(main())
