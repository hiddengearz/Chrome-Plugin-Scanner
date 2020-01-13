# Chrome Plugin canner
This script will scan the provided windows PC's with the current users credentials for chrome plugins. A CSV is then generated listing each plugin, the user who installed it and it's location.


# Requirments

Python 3.5+

# Useage

```
-t #, -threads # total ammount of threads to use
-c #, -chunksize # total ammount of PC\'s each thread should scan
-T #, -timeout # how long to spend on scanning each pc before ending the scan
-f [file], -file [file] the location of the file containing all of the systems
-o [file], -output [file] file location/name, defaults is results.csv
```

# Example

`python3 newmain.py -t 50 -c 5 -f systems.txt -o chromeplugins.csv`
