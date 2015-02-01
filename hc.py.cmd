@setlocal enableextensions & python -x %~f0 %* & goto :EOF

from app import *

app.run()
