@echo off

REM Assignment 7 GCD : Compile and link two files
REM Usages: run7.bat IrfanA7.asm GCD.asm

REM Since files may have changed
rescan > nul

REM CHECK if we have two input files
SET /A numOfArg=0
for %%x in (%*) do (
	set /A numOfArg=%numOfArg+1
)
if %numOfArg != 2 (
	@echo.
	echo %=>%=>%=>%=>%=> Two asm files needed as argument: run7 main.asm gcd.asm %=<%=<%=<%=<%=<
	goto :exitScript
)

REM Check if both files exits.
if not exist %1 (	
	@echo.
	echo %=>%=>%=>%=>%=> '%1' file not found. %=<%=<%=<%=<%=<
	goto :exitScript
)
if not exist %2 (	
	@echo.
	echo %=>%=>%=>%=>%=> '%2' file not found. %=<%=<%=<%=<%=<
	goto :exitScript
)
REM Since we are using link source.obj,,,util; for everyfile we link, to avoid error, we check if we have the necessary files.
if not exist UTIL.LIB (	
	@echo.
	echo %=>%=>%=>%=>%=> UTIL.LIB not found. %=<%=<%=<%=<%=<
	goto :exitScript
)
if not exist PCMAC.INC (	
	@echo.
	echo %=>%=>%=>%=>%=> PCMAC.INC not found. %=<%=<%=<%=<%=<
	goto :exitScript
)


@echo.
echo %=>%=>%=>%=>%=> First 5 lines of source file: %1 %=<%=<%=<%=<%=<
SET /A lineNum=0
FOR %%d IN (@%1) DO (
 	set /A lineNum=%lineNum+1
 	echo %d
 	IF %lineNum EQ 4 goto :endofcmnt1
)
:endofcmnt1	
echo %=>%=>%=>%=>%=> First 5 lines of source file: %1 %=<%=<%=<%=<%=<

@echo.
echo %=>%=>%=>%=>%=> First 5 lines of source file: %2 %=<%=<%=<%=<%=<
SET /A lineNum=0
FOR %%d IN (@%2) DO (
	set /A lineNum=%lineNum+1
	echo %d
	IF %lineNum EQ 4 goto :endofcmnt2
)
:endofcmnt2
echo %=>%=>%=>%=>%=> First 5 lines of source file: %2 %=<%=<%=<%=<%=<
@echo.
pause

REM Save substring of the filename in variables
set first=%1
set /a lenfir=%@len[%first]
set tsrif=%@reverse[%first]
set subtsrif=%@substr[%tsrif, 4, %lenfir]
set subfirst=%@reverse[%subtsrif]

set sec=%2
set /a lensec=%@len[%sec]
set ces=%@reverse[%sec]
set subces=%@substr[%ces, 4, %lensec]
set subsec=%@reverse[%subces]

REM Compiling main.asm
echo %=>%=>%=>%=>%=> Compiling and linking: %subfirst.asm & %subfirst.asm %=<%=<%=<%=<%=<
masm %subfirst.asm
if not exist %subfirst.obj (
	@echo.
	echo %=>%=>%=>%=>%=> Compiling failed: %subfirst.asm %=<%=<%=<%=<%=<
	goto :cleanup
)
@echo.
echo %=>%=>%=>%=>%=> Compilation sucessful: %subfirst.asm %=<%=<%=<%=<%=<

REM Compiling gcd.asm
masm %subsec.asm
if not exist %subsec.obj (
	@echo.
	echo %=>%=>%=>%=>%=> Compiling failed: %subsec.asm %=<%=<%=<%=<%=<
	goto :cleanup
)
@echo.
echo %=>%=>%=>%=>%=> Compiling successful: %subsec.asm %=<%=<%=<%=<%=<

REM LINKING
link %subfirst.obj + %subsec.obj,,,util;
if not exist %subfirst.exe (
		@echo.
		echo %=>%=>%=>%=>%=> Linking failed: %subfirst.asm & %subsec.asm %=<%=<%=<%=<%=<
		goto :cleanup	
)
@echo.
echo %=>%=>%=>%=>%=> Linking successful: %subfirst.asm & %subsec.asm %=<%=<%=<%=<%=<

:runAgain
@echo.
@echo.
echo %=>%=>%=>%=>%=> Run: %subfirst.exe %=<%=<%=<%=<%=<
%subfirst.exe
@echo.
@echo.
input %=>%=>%=>%=>%=> Run again : %subfirst.exe y/n ? %%yn
if %yn eq y (
	goto :runAgain
) 
echo %=>%=>%=>%=>%=> End of Execution: %subfirst.exe %=<%=<%=<%=<%=<

:cleanup
REM Delete all intermediate files

if exist %subfirst.obj (
	DEL %subfirst.obj > nul
)
if exist %subsec.obj (
	DEL %subsec.obj > nul
)

if exist %subfirst.map (
	DEL %subfirst.map > nul
)
if exist %subsec.map (
	DEL %subsec.map > nul
)

@echo.
echo %=>%=>%=>%=>%=> Deleted all *.obj and *.map files. %=<%=<%=<%=<%=<

:exitScript