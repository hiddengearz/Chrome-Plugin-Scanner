#!C:\Users\smithmic\PycharmProjects\UHTChromePlugins\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'CProfileV==1.0.7','console_scripts','cprofilev'
__requires__ = 'CProfileV==1.0.7'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('CProfileV==1.0.7', 'console_scripts', 'cprofilev')()
    )
