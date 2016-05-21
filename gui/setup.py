
from cx_Freeze import *

# http://msdn.microsoft.com/en-us/library/windows/desktop/aa371847(v=vs.85).aspx
shortcut_table = [
	("DesktopShortcut",       # Shortcut
	"DesktopFolder",          # Directory_
	"GiveMeFive",                 # Name
	"TARGETDIR",              # Component_
	"[TARGETDIR]main.exe", # Target
	None,                     # Arguments
	None,                     # Description
	None,                     # Hotkey
	None,                     # Icon
	None,                     # IconIndex
	None,                     # ShowCmd
	'TARGETDIR'               # WkDir
	)
	]

# Now create the table dictionary
msi_data = {"Shortcut": shortcut_table}

# Change some default MSI options and specify the use of the above defined tables
bdist_msi_options = {'data': msi_data}

base = None
if sys.platform == "win32":
	base = "Win32GUI"

build_exe_options = {"packages": ["os", "pyautogui"], "excludes": ["tkinter"], 'includes': ['atexit', 'mainwindow', 'ui_mainwindow'], 'path': sys.path + ['gmouseui', 'gmouseui/uimodules', 'daemon']}

setup(name = "GiveMeFive",
		version = "0.3",
		description = "Cliente",
		options = {"bdist_msi": bdist_msi_options, "build_exe": build_exe_options},
		executables = [Executable("main.py", base=base)]
		)