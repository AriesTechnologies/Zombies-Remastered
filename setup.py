from cx_Freeze import setup, Executable
target = Executable(
    script="main.py",
    targetName = "Zombies.exe",
    base="Win32GUI")
setup(
    name = "Zombies.exe",
    executables= [target]
    )
