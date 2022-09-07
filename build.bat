set root=C:\Users\%USERNAME%\anaconda3
call %root%\Scripts\activate.bat %root%

taskkill /f /im Git-Popup-Closer.exe

call conda activate git-popup-closer
call pyinstaller -n "Git-Popup-Closer" --onefile --noconsole --version-file file_version_info.txt main.py
call move "dist\Git-Popup-Closer.exe"

start "" "Git-Popup-Closer.exe"