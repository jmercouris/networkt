Build Instructions:
___________________

1. Go to the PyInstaller directory, and build the spec:
2. $ pyinstaller -y --clean --windowed *.spec

3. Run:

   A. $ pushd dist
   B. $ hdiutil create ./*.dmg -srcfolder *.app -ov
   C. $ popd

You will now have a *.dmg available in the dist directory.



