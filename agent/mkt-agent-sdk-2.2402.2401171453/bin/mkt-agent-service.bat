@echo off 
setlocal 

@rem Find java.exe
if defined JAVA_HOME goto findJavaFromJavaHome

echo.
echo ERROR: JAVA_HOME is not set.
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.
goto end

:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE=%JAVA_HOME%/bin/java.exe

if exist "%JAVA_EXE%" goto checkPrinstall

echo.
echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME%
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.
goto end


:checkPrinstall
if defined PR_INSTALL goto checkPrunsrv

echo.
echo ERROR: PR_INSTALL is not set.
echo.
echo Please set the PR_INSTALL variable in your environment to contain the 
echo full path to the appropriate prunsrv.exe.
goto end

:checkPrunsrv
if exist "%PR_INSTALL%" goto init

echo.
echo ERROR: PR_INSTALL setting is invalid: %PR_INSTALL%
echo.
echo Please set the PR_INSTALL variable in your environment to contain the 
echo full path to the appropriate prunsrv.exe.
goto end

:init
set DIRNAME=%~dp0
if "%DIRNAME%" == "" set DIRNAME=.
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%..

set SERVICE_NAME=CustomerIntelligence360Agent


REM start - This takes the input from installService and places it between x's 
REM       - if there are none then you get xx as a null check 
if "x%1x" == "xx" goto displayUsage 
set SERVICE_CMD=%1 
REM shift moves to next field 
shift 
if "x%1x" == "xx" goto checkServiceCmd 
:checkServiceCmd 
if /i %SERVICE_CMD% == install goto doInstall 
if /i %SERVICE_CMD% == remove goto doRemove 
if /i %SERVICE_CMD% == uninstall goto doRemove 
echo Unknown parameter "%SERVICE_CMD%" 

:displayUsage 
echo. 
echo Usage: mkt-agent-service.bat install/remove 
goto end 

:doRemove 
echo Removing the service '%PR_INSTALL%' '%SERVICE_NAME%' ... 
"%PR_INSTALL%" //DS//%SERVICE_NAME% ^
       --LogPath=%APP_HOME%\logs ^
       --LogPrefix=CustomerIntelligence360AgentService ^
       --LogLevel=Debug ^
       --StdOutput=auto ^
       --StdError=auto

if not errorlevel 1 goto removed 
echo Failed removing '%SERVICE_NAME%' service 
goto end 

:removed 
echo The service '%SERVICE_NAME%' has been removed 
goto end 

:doInstall 
echo Installing the service '%PR_INSTALL%' '%SERVICE_NAME%' ... 
"%PR_INSTALL%" //IS//%SERVICE_NAME% ^
       --Description="Customer Intelligence 360 Agent Service" ^
       --LogPath="%APP_HOME%\logs" ^
       --LogPrefix=CustomerIntelligence360AgentService ^
       --LogLevel=Debug ^
       --StdOutput=auto ^
       --StdError=auto ^
       --JvmOptions="-Dlogging.config=%APP_HOME%\config\logback-spring.xml" ^
       ++JvmOptions="-DAPP_HOME=%APP_HOME%" ^
       ++JvmOptions="-Dagent.shell.enable=false" ^
       --Startup=auto ^
       --StartMode=jvm  ^
       --StartClass=com.sas.mkt.apigw.sdk.streaming.agent.Application ^
       --StartMethod=main ^
       --StopMode=jvm  ^
       --StopClass=com.sas.mkt.apigw.sdk.streaming.agent.Application ^
       --StopMethod=stopAgentService ^
       --StopTimeout=120 ^
       --Classpath="%APP_HOME%\config;%APP_HOME%\lib\*;%APP_HOME%\libThirdParty\*" ^
       --Jvm="%JAVA_HOME%\jre\bin\server\jvm.dll" ^
       --JavaHome="%JAVA_HOME%"
       
if not errorlevel 1 goto installed 
echo Failed installing '%SERVICE_NAME%' service 
goto end 

:installed 
echo The service '%SERVICE_NAME%' has been installed 
       

:end 
echo Exiting mkt-agent-service.bat ...