from subprocess import Popen
import re
import sublime, sublime_plugin
import webbrowser
import os
import sys

p = 0
p2 = 0

SETTINGS_FILE = "nodejs_debug.sublime-settings"

if sys.version_info >= (3,):
    installed_dir, _ = __name__.split('.')
else:
    installed_dir = os.path.basename(os.getcwd())

class NodejsDebugCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    sublime.set_timeout(self.launch, 100)

  def launch(self):

    window = sublime.active_window()
    window.run_command('save')

    regx = re.compile(" ")

    if sublime.platform() == "windows":
        cmd = "cmd /K node --debug-brk " + regx.sub("\ ", self.view.file_name());
        # p = Popen(cmd)
        # p2 = Popen("node-inspector.cmd --web-port=9901")
        startupinfo1 = subprocess.STARTUPINFO()
        startupinfo1.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.Popen(cmd, startupinfo=startupinfo1)

        startupinfo2 = subprocess.STARTUPINFO()
        # startupinfo2.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.Popen("node-inspector.cmd --web-port=9901", startupinfo=startupinfo2)
        
    if sublime.platform() == "linux":
        terminal = TerminalSelector.get()
        cmd = terminal + " -e 'node --debug-brk " + regx.sub("\ ", self.view.file_name()+ "'");
        p = os.popen(cmd)
        p2 = os.popen(terminal + " -e 'node-inspector --web-port=9901'")

    sublime.set_timeout(self.openChrome,300)

  def openChrome(self):

    url = "http://localhost:9901/debug?port=5858"

    config = sublime.load_settings(SETTINGS_FILE)
    chrome_path = config.get('chrome_path',"")
    chrome = webbrowser.BackgroundBrowser(chrome_path)
    webbrowser.register('chrome', None, chrome)
    webbrowser.get('chrome').open_new_tab(url)

    # webbrowser.open_new(url)
    # self.view.run_command("open_browser")

# get command terminal for Linux
class TerminalSelector():
    default = None

    @staticmethod
    def get():
        settings = sublime.load_settings(SETTINGS_FILE)
        package_dir = os.path.join(sublime.packages_path(), installed_dir)

        terminal = settings.get('terminal')
        if terminal:
            dir, executable = os.path.split(terminal)
            if not dir:
                joined_terminal = os.path.join(package_dir, executable)
                if os.path.exists(joined_terminal):
                    terminal = joined_terminal
                    if not os.access(terminal, os.X_OK):
                        os.chmod(terminal, 0o755)
            return terminal

        if TerminalSelector.default:
            return TerminalSelector.default

        default = None

        if os.name == 'nt':
            if os.path.exists(os.environ['SYSTEMROOT'] +
                    '\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'):
                # This mimics the default powershell colors since calling
                # subprocess.POpen() ends up acting like launching powershell
                # from cmd.exe. Normally the size and color are inherited
                # from cmd.exe, but this creates a custom mapping, and then
                # the LaunchPowerShell.bat file adjusts some other settings.
                key_string = 'Console\\%SystemRoot%_system32_' + \
                    'WindowsPowerShell_v1.0_powershell.exe'
                try:
                    sublime.message_dialog(key_string)
                    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
                        key_string)
                except (WindowsError):
                    key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,
                        key_string)
                    _winreg.SetValueEx(key, 'ColorTable05', 0,
                        _winreg.REG_DWORD, 5645313)
                    _winreg.SetValueEx(key, 'ColorTable06', 0,
                        _winreg.REG_DWORD, 15789550)
                default = os.path.join(package_dir, 'PS.bat')
                sublime_terminal_path = os.path.join(sublime.packages_path(), installed_dir)
                # This should turn the path into an 8.3-style path, getting around unicode
                # issues and spaces
                buf = create_unicode_buffer(512)
                if windll.kernel32.GetShortPathNameW(sublime_terminal_path, buf, len(buf)):
                    sublime_terminal_path = buf.value
                os.putenv('sublime_terminal_path', sublime_terminal_path.replace(' ', '` '))
            else :
                default = os.environ['SYSTEMROOT'] + '\\System32\\cmd.exe'
        elif sys.platform == 'darwin':
            default = os.path.join(package_dir, 'Terminal.sh')
            if not os.access(default, os.X_OK):
                os.chmod(default, 0o755)

        else:
            ps = 'ps -eo comm | grep -E "gnome-session|ksmserver|' + \
                'xfce4-session" | grep -v grep'
            wm = [x.replace("\n", '') for x in os.popen(ps)]
            if wm:
                if wm[0] == 'gnome-session':
                    default = 'gnome-terminal'
                elif wm[0] == 'xfce4-session':
                    default = 'terminal'
                elif wm[0] == 'ksmserver':
                    default = 'konsole'
            if not default:
                default = 'xterm'

        TerminalSelector.default = default
        return default

