REM Set env vars on windows from K=V definition file
REM >./env.bat <path_to_env_var_definition_file>

@echo off
python _env.py %1 > temp.cmd
IF ERRORLEVEL 1 (
    @echo on
    echo Error setting environmental variables
) ELSE (
    call temp.cmd
    @echo on
    echo Environmental variables set
)
@echo off
del temp.cmd