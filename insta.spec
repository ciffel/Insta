# -*- mode: python -*-
a = Analysis(['insta.py'],
             pathex=['C:\\Users\\shuming\\Desktop\\Insta'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
datas = [
	('icon.png', './icon.png', 'DATA')
]
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas + datas,
          name='Insta.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='icon.ico')
