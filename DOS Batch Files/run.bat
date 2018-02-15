@echo off

REM Automation script to compile and link submissino from Assignment 2,3,4,6 and 8

REM Since files may have changed
rescan > nul

REM Check if script has one source.asm file as argument
SET /A numOfArg=0
for %%x in (%*) do (
	set /A numOfArg=%numOfArg+1
)
if %numOfArg != 1 (
	@echo.
	echo %=>%=>%=>%=>%=> Souce asm files needed as argument. %=<%=<%=<%=<%=<
	goto :exitScript
)

REM Check if the source file, util.lib and pcmac.inc exists
if not exist %1 (	
	@echo.
	echo %=>%=>%=>%=>%=> File not found '%1' %=<%=<%=<%=<%=<
	goto :exitScript
)
REM Since we are using link source.obj,,,util; for everyfile we link, to avoid error, we check if we have the necessary files.
if not exist UTIL.LIB (	
	@echo.
	echo %=>%=>%=>%=>%=> UTIL.LIB not found %=<%=<%=<%=<%=<
	goto :exitScript
)
if not exist PCMAC.INC (	
	@echo.
	echo %=>%=>%=>%=>%=> PCMAC.INC not found %=<%=<%=<%=<%=<
	goto :exitScript
)

REM PRINT FIRST FIVE LINE OF COMMENTS
REM %= is an escape character
echo %=>%=>%=>%=>%=> First 5 lines of source file: %1 %=<%=<%=<%=<%=<
SET /A lineNum=0
FOR %%d IN (@%1) DO (
	set /A lineNum=%lineNum+1
	echo %d
	IF %lineNum EQ 4 goto :endofcmnt
)
:endofcmnt	
echo %=>%=>%=>%=>%=> First 5 lines of source file: %1 %=<%=<%=<%=<%=<
@echo.
pause

REM Save 'soure' substring from source.asm to variable dd
REM aa = 'source.asm' and dd = 'source'
set aa=%1
set /a length=%@len[%aa]
set bb=%@reverse[%aa]
set cc=%@substr[%bb, 4, %length]
set dd=%@reverse[%cc]

REM COMPILING
echo %=>%=>%=>%=>%=> Compiling and linking: %dd.asm %=<%=<%=<%=<%=<
masm %dd.asm
if not exist %dd.obj (
	echo %=>%=>%=>%=>%=> Compilation failed: %dd.asm %=<%=<%=<%=<%=<
	goto :cleanup
)
echo %=>%=>%=>%=>%=> Compilation successful: %dd.asm %=<%=<%=<%=<%=<

REM LINKING
link %dd.obj,,,util;
if not exist %dd.exe (
		echo %=>%=>%=>%=>%=> Linking failed: %dd.asm %=<%=<%=<%=<%=<
		goto :cleanup	
)
echo %=>%=>%=>%=>%=> Linking sucessful: %dd.asm %=<%=<%=<%=<%=<

REM EXECUTION
:runAgain
@echo.
@echo.
echo %=>%=>%=>%=>%=> Run: %dd.exe %=<%=<%=<%=<%=<
%dd.exe
@echo.
@echo.
REM Anything but 'y' is a interprated as 'n'
REM For example, pressing Enter will be interprated as 'n'
input %=>%=>%=>%=>%=> Run again : %dd.exe y/n ? %%yn
if %yn eq y (
	goto :runAgain
) 
echo %=>%=>%=>%=>%=> End of Execution: %dd.exe %=<%=<%=<%=<%=<

REM Copy asm to an extentionless file
type %1 > %dd
DEL %dd.asm > nul
@echo.
echo %=>%=>%=>%=>%=> Renaming: %dd.asm to %dd %=<%=<%=<%=<%=<

REM CLEANUP
:cleanup
REM If program jumps to cleaup, it means something didn't go well, and the script will delete the intermediate file it has created
if exist %dd.obj (
	DEL %dd.obj > nul
)

if exist %dd.map (
	DEL %dd.map > nul
)
echo %=>%=>%=>%=>%=> Deleted files: %dd.obj & %dd.map %=<%=<%=<%=<%=<
@echo.
@echo.

:exitScript