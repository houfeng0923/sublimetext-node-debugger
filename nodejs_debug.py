from subprocess import Popen
import re
import sublime, sublime_plugin
import webbrowser
import os
import sys


SETTINGS_FILE = "nodejs_debug.sublime-settings"

if sys.version_info >= (3,):
    installed_dir, _ = __name__.split('.')
else:
    installed_dir = os.path.basename(os.getcwd())


def _get_startupinfo():

    PLATFORM_IS_WINDOWS = (sublime.platform() == 'windows')
    if PLATFORM_IS_WINDOWS:
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = subprocess.SW_HIDE
        return info
    return None


class NodejsDebugCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    sublime.set_timeout(self.launch, 100)

  def launch(self):

    window = sublime.active_window()
    window.run_command('save')

    regx = re.compile(" ")
    cmd = "node-debug";
    if sublime.platform() == "windows":
        cmd += ".cmd";

    subprocess.Popen([cmd,'--web-port=9901',regx.sub("\ ",self.view.file_name())],
            startupinfo=_get_startupinfo())
