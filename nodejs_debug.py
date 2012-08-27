from subprocess import Popen
import re
import sublime, sublime_plugin
import webbrowser

p = 0
p2 = 0
 
SETTINGS_FILE = "nodejs_debug.sublime-settings"

class NodejsDebugCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    sublime.set_timeout(self.launch, 100)
 
  def launch(self):

    window = sublime.active_window()
    window.run_command('save')

    regx = re.compile(" ")
    cmd = "cmd.exe /K node --debug-brk " + regx.sub("\ ", self.view.file_name());
    p = Popen(cmd) 
     
    p2 = Popen("node-inspector.cmd")

    sublime.set_timeout(self.openChrome,300)
  

  def openChrome(self):
   		
    url = "localhost:8080/debug?port=5858"

    config = sublime.load_settings(SETTINGS_FILE)
    chrome_path = config.get('chrome_path',"") 
    Popen(chrome_path+" "+url) 
 
    # webbrowser.open_new(url)   
    # self.view.run_command("open_browser")
 
