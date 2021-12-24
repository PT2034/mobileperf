#adb start-server

# 覆盖安装：
#adb install -r xxx.apk

#查看手机端安装的所有app包名：
#adb shell pm list packages

#打开 mtklog 界面
#adb shell am start -n com.mediatek.mtklogger/com.mediatek.mtklogger.MainActivity“

#打开手机设置页面
adb shell am start com.android.settings/com.android.settings.Settings
#adb shell am start com.android.settings.DevelopmentSettings

#返回主页面 3 --> "KEYCODE_HOME"
adb shell input keyevent 3

#返回 4 --> "KEYCODE_BACK"
# adb shell input keyevent 4