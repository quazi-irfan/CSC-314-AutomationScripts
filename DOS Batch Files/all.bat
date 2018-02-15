@echo off

REM Repeatedly calls "run.bat <source.asm>" to all *.asm files available in the directory

REM Since the user might copy/paste files in the folder, it made sense to rescan the folder.
REM Otherwise the newly added file would be ignore.

rescan > nul

FOR %%i IN (*.asm) DO (
	echo ---------------------- File Name: %i ------------------------------
	call run %i 
)