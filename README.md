# OMRON SysmacStudio - SymbolParser
A tool to export published global variables from OMRON Sysmac Studio projects.

When using Sysmac Studio, you can export the published variables 
by using `Tools > Export Global Variables > CX-Designer ...` from the menu bar.

However, this built-in feature doesn't export the symbols of some types such as Enum;
as well as STRUCT type symbols whose members are of these types.\
The skipped symbols are listed in a message dialog: 
*The following variable will not be copied to CX-Designer*.

That tool is intended to overcome this behavior and thus to allow you to export 
all the global symbols whose *Network Publish* is set to *Publish Only*.

## Sysmac project directory
By default, the Sysmac project directory is located at `C:\Omron\Data\Solution`.

However, if you ticked "Manage in project file" at the home screen, each project are extracted 
to a temporary directory each time you open it.\
This directory is located at `C:\Omron\Data\ProjFileTmp`.
