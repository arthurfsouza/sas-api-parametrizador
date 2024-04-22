@if "%DEBUG%" == "" @echo off
@rem ##########################################################################
@rem
@rem  mkt-agent-upgrade startup script for Windows
@rem
@rem ##########################################################################

@rem Set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" setlocal

set DIRNAME=%~dp0
if "%DIRNAME%" == "" set DIRNAME=.
set APP_BASE_NAME=%~n0

@rem Find java.exe
if defined JAVA_HOME goto findJavaFromJavaHome

set JAVA_EXE=java.exe
%JAVA_EXE% -version >NUL 2>&1
if "%ERRORLEVEL%" == "0" goto init

echo.
echo ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail


:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE=%JAVA_HOME%/bin/java.exe

if exist "%JAVA_EXE%" goto init

echo.
echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME%
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:init
@rem set MKT_AGENT_UPGRADE_OPTS=-agentlib:jdwp=transport=dt_socket,address=8003,server=y,suspend=n
if "%1."=="copyfiles." goto copyfiles
if "%1."=="copyfilesonly." goto copyfiles
if "%1."=="cleanup." goto cleanup

:download
set APP_HOME=%DIRNAME%..
set CLASSPATH=%APP_HOME%\config;%APP_HOME%\lib\*
set DEFAULT_JVM_OPTS="-Dlogback.configurationFile=%APP_HOME%\config\logback-upgrade.xml"
cd %APP_HOME%
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %MKT_AGENT_UPGRADE_OPTS%  -classpath "%CLASSPATH%" com.sas.mkt.apigw.sdk.streaming.agent.UpgradeAgent download
if "%ERRORLEVEL%" NEQ "0"  goto fail
if "%1."=="downloadonly." goto mainEnd
for /f %%i in ('dir /b new') do set MKT=%%i
%APP_HOME%\new\%MKT%\bin\mkt-agent-upgrade.bat copyfiles
@rem should not get to this line after calling another bat file without the "call " prefix
goto fail


:copyfiles
set APP_HOME=%DIRNAME%..\..\..
set CLASSPATH=%DIRNAME%..\config;%DIRNAME%..\lib\*
set DEFAULT_JVM_OPTS="-Dlogback.configurationFile=%DIRNAME%..\config\logback-upgrade.xml"
cd %APP_HOME%
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %MKT_AGENT_UPGRADE_OPTS%  -classpath "%CLASSPATH%" com.sas.mkt.apigw.sdk.streaming.agent.UpgradeAgent copyfiles
if "%ERRORLEVEL%" NEQ "0"  goto fail
if "%1."=="copyfilesonly." goto mainEnd
%APP_HOME%\bin\mkt-agent-upgrade.bat cleanup
@rem should not get to this line after calling another bat file without the "call " prefix
goto fail

:cleanup
set APP_HOME=%DIRNAME%..
set CLASSPATH=%APP_HOME%\config;%APP_HOME%\lib\*
set DEFAULT_JVM_OPTS="-Dlogback.configurationFile=%APP_HOME%\config\logback-upgrade.xml"
cd %APP_HOME%
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %MKT_AGENT_UPGRADE_OPTS%  -classpath "%CLASSPATH%" com.sas.mkt.apigw.sdk.streaming.agent.UpgradeAgent cleanup
if "%ERRORLEVEL%" NEQ "0"  goto fail
goto finish


:fail
rem Set variable APPLICATION_START_DIR if you need the _script_ return code instead of
rem the _cmd.exe /c_ return code!
@echo Upgrade failed.   Check logs.
if  not "" == "%APPLICATION_START_DIR%" exit 1
exit /b 1

:finish
echo "Upgrade complete."

:mainEnd
if "%OS%"=="Windows_NT" endlocal

:omega
