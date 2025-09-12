@Echo Off

REM set http_proxy=he141117.emea1.cds.t-internal.com:8080/
REM set https_proxy=he141117.emea1.cds.t-internal.com:8080/
REM set HTTP_PROXY=he141117.emea1.cds.t-internal.com:8080/
REM set HTTPS_PROXY=he141117.emea1.cds.t-internal.com:8080/

Set "VIRTUAL_ENV=venv_fast_prototyping_genai_with_streamlit"
Set "REQUIREMENTS_TXT=requirements.txt"

Set "PYTHON_EXE_PATH=C:\Users\A3370680\AppData\Local\Programs\Python\Python313\python.exe"
REM Set "PYTHON_EXE_PATH=C:\Program Files\WPy64-31230\python-3.12.3.amd64\python.exe"
REM Set "PYTHON_EXE_PATH=C:\Users\A3370680\AppData\Local\Programs\Python\Python311\python.exe"


echo Using Python Version:
"%PYTHON_EXE_PATH%" --version

If Not Exist "%VIRTUAL_ENV%\Scripts\activate.bat" (
    echo Creating a new virtual environment in "%VIRTUAL_ENV%"...
    "%PYTHON_EXE_PATH%" -m venv --clear "%VIRTUAL_ENV%"
    If ErrorLevel 1 (
        echo Failed to create virtual environment.
        Exit /B 1
    )
) else (
    echo Using existing virtual environment in "%VIRTUAL_ENV%"...
)

Call "%VIRTUAL_ENV%\Scripts\activate.bat"
If ErrorLevel 1 (
    echo Failed to activate virtual environment.
    Exit /B 1
)

python -m pip install --upgrade pip
echo Checking pip version:
pip --version

pip install -r %REQUIREMENTS_TXT%
If ErrorLevel 1 (
    echo Failed to install requirements.
    Exit /B 1
)

echo ****************************************
echo Virtual environment is now ready to use.
python --version
pip --version
echo Path to your virtual environment: %VIRTUAL_ENV%
pause
