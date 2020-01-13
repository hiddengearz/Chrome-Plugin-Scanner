# Chrome Plugin Scanner
The Chrome Plugin Scanner is a multi-threaded python script that will connect to any computer provided (assuming the account executing the script has permissions) and will find all installed chrome plugins and save them in a CSV containing the plugin name, who installed it and it's location.

* Tested with windows 2003 and newer
* The script assumes the users folder is in the C drive


# Requirments

* Python 3.5+
* Run the script with an account that has read permissions to all user folders on the desired systems

# Useage

```
-t #, -threads # total ammount of threads to use
-c #, -chunksize # total ammount of PC\'s each thread should scan
-T #, -timeout # how long to spend on scanning each pc before ending the scan
-f [file], -file [file] the location of the file containing all of the systems
-o [file], -output [file] file location/name, defaults is results.csv
-v, will provide more information on the scan while it\'s running
-h, -help will provide help information
```

# Example

`python3 newmain.py -t 50 -c 5 -f systems.txt -o chromeplugins.csv`

Systems.txt:
```
PC1.domain
PC2.domain
192.168.0.1
```

chromeplugins.csv

| Extension  |Computer   |Location|
|-------------|---|---|
|Google Slides|PC|\\PC\\C$\\users\\user\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions\\aapocclcgogkmnckokdopfmhonfmgoek\\|
|Google Docs|PC|\\PC\\C$\\users\\user2\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions\\aohghmighlieiainnegkcijnfilokake\\|
|Google Drive|PC|\\PC\\C$\\users\\user3\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions\\apdfllckaahabafndbhieahigkjlhalf\\|
