cp ./dist_linux_binary/main build_appimage/MyApp.AppDir/usr/bin/main

chmod a+x ./build_appimage/MyApp.AppDir/usr/bin/main
chmod a+x ./build_appimage/MyApp.AppDir/MyApp.desktop
chmod a+x ./build_appimage/MyApp.AppDir/AppRun

# appimagetool [OPTION?] SOURCE [DESTINATION] 
./build_appimage/appimagetool-x86_64.AppImage ./build_appimage/MyApp.AppDir/ ./dist_linux_appimage/MyApp.AppImage