@echo off
rem PoolWind install script for Windows.
rem
rem Runs PoolWind on a PC as a demo: a recorded swim and a simulated jet.
rem A PC can't control a pool (that needs the Raspberry Pi build). See
rem docs/SETUP_GUIDE.md. Download this file and double-click it: it
rem installs PoolWind, opens the demo tour in the browser and starts the
rem demo. When it finishes it deletes itself, so Downloads doesn't fill
rem with copies; to watch the demo again, download it again: Python and
rem the libraries are already there, so it gets PoolWind and the sample
rem video again. The video is hidden, and when PoolWind closes the whole
rem PoolWind folder is deleted (Bill, 2026-10-23: "I can lower the number
rem of PC's that have it"; 2026-10-24: "Can the entire Poolwind folder be
rem deleted on demo program exit"). Until then, everything it does is
rem written to %USERPROFILE%\PoolWind\install.log.
rem
rem With poolwind.py in the same folder as this script, it installs the
rem files from that folder (poolwind.py, and poolwind_defaults.txt,
rem poolwind_calibration.txt and PoolWind_demo.mp4 if they are there)
rem instead of downloading them.
rem
rem License: see LICENSE.md.

setlocal
set "PW_DIR=%USERPROFILE%\PoolWind"
set "LOG=%PW_DIR%\install.log"
set "REPO=https://github.com/WillyAG/PoolWind"
set "ZIP=%TEMP%\PoolWind-download.zip"
set "SRC=%TEMP%\PoolWind-download"
set "TOUR=%REPO%/blob/main/docs/USER_MANUAL.md#9-the-demo-tour"

rem Python packages, at the versions PoolWind was tested with (the Pi's).
set "PIP_PACKAGES=opencv-python==4.13.0.92 scipy==1.17.1 numpy~=2.2.0 matplotlib~=3.10.0 PySide6~=6.8.0"

if not exist "%PW_DIR%" mkdir "%PW_DIR%"
echo ===== PoolWind install %DATE% %TIME% ===== >> "%LOG%"
echo.
echo PoolWind install for Windows (demo)
echo Everything is written to %LOG%
echo.

rem --------------------------------------------------------------------
echo 1/5  Python
rem --------------------------------------------------------------------
set "PY="
py -3.13 --version >nul 2>&1 && set "PY=py -3.13"
if not defined PY py -3.12 --version >nul 2>&1 && set "PY=py -3.12"
if defined PY goto have_python
where winget >nul 2>&1
if errorlevel 1 goto no_winget
echo      installing Python 3.13 (a few minutes)...
winget install -e --id Python.Python.3.13 --scope user --accept-package-agreements --accept-source-agreements >> "%LOG%" 2>&1
set "PY=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
if not exist "%PY%" goto fail
set "PY="%PY%""
:have_python
%PY% --version >> "%LOG%" 2>&1 || goto fail
%PY% --version

rem --------------------------------------------------------------------
echo 2/5  Python packages (a few minutes the first time)
rem --------------------------------------------------------------------
%PY% -c "import cv2, PySide6, scipy, numpy, matplotlib" >nul 2>&1
if not errorlevel 1 (
    echo      already installed
    goto have_packages
)
%PY% -m pip install --upgrade pip >> "%LOG%" 2>&1
%PY% -m pip install %PIP_PACKAGES% >> "%LOG%" 2>&1 || goto fail
echo      installed
:have_packages

rem --------------------------------------------------------------------
echo 3/5  Getting PoolWind
rem --------------------------------------------------------------------
if exist "%~dp0poolwind.py" (
    set "SOFTWARE=%~dp0."
    echo      using the files in %~dp0
    goto have_files
)
curl.exe -L -f -o "%ZIP%" "%REPO%/archive/refs/heads/main.zip" >> "%LOG%" 2>&1 || goto fail
if exist "%SRC%" rmdir /s /q "%SRC%"
mkdir "%SRC%"
tar -xf "%ZIP%" -C "%SRC%" >> "%LOG%" 2>&1 || goto fail
set "SOFTWARE=%SRC%\PoolWind-main\software"
if not exist "%SOFTWARE%\poolwind.py" goto fail
echo      downloaded
:have_files

rem --------------------------------------------------------------------
echo 4/5  Copying PoolWind to %PW_DIR%
rem --------------------------------------------------------------------
if exist "%PW_DIR%\poolwind.py" (
    copy /y "%PW_DIR%\poolwind.py" "%PW_DIR%\poolwind.py.previous" >> "%LOG%" 2>&1
    echo      the previous program is kept as poolwind.py.previous
)
copy /y "%SOFTWARE%\poolwind.py" "%PW_DIR%\poolwind.py" >> "%LOG%" 2>&1 || goto fail
echo      installed poolwind.py
for %%f in (poolwind_defaults.txt poolwind_calibration.txt) do (
    if exist "%PW_DIR%\%%f" (
        echo      kept your %%f
    ) else if exist "%SOFTWARE%\%%f" (
        copy "%SOFTWARE%\%%f" "%PW_DIR%\%%f" >> "%LOG%" 2>&1
        echo      installed %%f
    ) else (
        echo      %%f is missing: put it next to this script and run it again
    )
)
rem A fresh copy each time: a hidden file can't be overwritten, and an
rem older copy may be an older video.
if exist "%PW_DIR%\PoolWind_demo.mp4" del /f /a "%PW_DIR%\PoolWind_demo.mp4" >> "%LOG%" 2>&1
if exist "%SOFTWARE%\PoolWind_demo.mp4" (
    copy "%SOFTWARE%\PoolWind_demo.mp4" "%PW_DIR%\PoolWind_demo.mp4" >> "%LOG%" 2>&1
    echo      installed PoolWind_demo.mp4
) else (
    echo      downloading the sample video...
    curl.exe -L -f -o "%PW_DIR%\PoolWind_demo.mp4" "%REPO%/releases/latest/download/PoolWind_demo.mp4" >> "%LOG%" 2>&1
    if errorlevel 1 (
        del "%PW_DIR%\PoolWind_demo.mp4" >nul 2>&1
        echo      the sample video couldn't be downloaded: PoolWind will say so
    ) else (
        echo      installed PoolWind_demo.mp4
    )
)
if exist "%PW_DIR%\PoolWind_demo.mp4" attrib +h "%PW_DIR%\PoolWind_demo.mp4"
rmdir /s /q "%SRC%" >nul 2>&1
del "%ZIP%" >nul 2>&1

rem --------------------------------------------------------------------
echo 5/5  Starting the demo
rem --------------------------------------------------------------------
rem No desktop icon (Bill, 2026-10-23): the demo starts from here, next to
rem the demo tour in the browser, every time the script is run.
rem PoolWind.bat is in %TEMP%, not in the PoolWind folder, so that it can
rem delete the whole folder when PoolWind closes. It runs under cmd /c, so
rem its window closes too (Bill, 2026-10-24: "opens up a blank titled
rem Poolwind and leaves it there").
set "BAT=%TEMP%\PoolWind.bat"
del "%PW_DIR%\PoolWind.bat" >nul 2>&1
> "%BAT%" (
    echo @echo off
    echo cd /d "%PW_DIR%"
    echo %PY% -X utf8 poolwind.py
    echo if errorlevel 1 pause
    echo cd /d "%TEMP%"
    echo if exist "%PW_DIR%\poolwind.py" rmdir /s /q "%PW_DIR%"
)
echo      opening the demo tour in your browser
start "" "%TOUR%"
echo      starting PoolWind
start "PoolWind" /min cmd /c "%BAT%"

echo.
echo Done. The demo is running: follow the demo tour in your browser.
echo To watch the demo again, download it again from PoolWind's GitHub page.
echo ===== done ===== >> "%LOG%"
timeout /t 15
rem A downloaded copy deletes itself, so Downloads doesn't fill with
rem install_windows (1).bat, (2) ... (Bill, 2026-10-24). A copy next to
rem poolwind.py, for testing, is kept.
if exist "%~dp0poolwind.py" exit /b 0
(goto) 2>nul & del "%~f0"

:no_winget
echo.
echo Python isn't installed, and this PC can't install it by itself.
echo Install Python 3.13 from python.org (tick "Add python.exe to PATH"),
echo then run this script again.
pause
exit /b 1

:fail
echo.
echo Something went wrong. The details are in:
echo    %LOG%
echo ===== failed ===== >> "%LOG%"
pause
exit /b 1
