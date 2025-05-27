from PyInstaller.utils.hooks import collect_all

# Collect all files from the backend package
datas, binaries, hiddenimports = collect_all('backend')