from kivy import Config
Config.set('graphics', 'orientation', 'portrait')
Config.set('graphics', 'resizable', False)
Config.set('kivy', 'keyboard_mode', 'system')

import os
import sys
import traceback

def is_android():
    return 'ANDROID_ARGUMENT' in os.environ or 'ANDROID_ROOT' in os.environ

def log_error(msg):
    try:
        log_path = '/sdcard/gala_error.log'
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(msg + '\n')
        print(msg)
    except:
        print(msg)

if hasattr(sys, '_MEIPASS'):
    resource_path = os.path.join(sys._MEIPASS, 'data')
    if os.path.exists(resource_path):
        os.environ['KIVY_NO_ARGS'] = '1'

error_msg = None

try:
    from mobile_main import MobileApp
except Exception as e:
    error_msg = f"导入错误: {e}\n{traceback.format_exc()}"
    log_error(error_msg)

if __name__ == '__main__':
    if error_msg:
        from kivy.app import App
        from kivy.uix.label import Label
        class ErrorApp(App):
            def build(self):
                return Label(text=error_msg[:500], font_size='14sp')
        ErrorApp().run()
    else:
        try:
            app = MobileApp()
            app.run()
        except Exception as e:
            error_msg = f"运行错误: {e}\n{traceback.format_exc()}"
            log_error(error_msg)
            from kivy.app import App
            from kivy.uix.label import Label
            class ErrorApp(App):
                def build(self):
                    return Label(text=error_msg[:500], font_size='14sp')
            ErrorApp().run()
