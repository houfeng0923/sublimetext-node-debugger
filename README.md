a  simple plugin for sublime text2 to debug node file  in  WebKit based browser

## Getting Started


### Requirements

* [nodeJS](http://github.com/ry/node)
  - versions: 0.6.0 or later
* [npm](http://github.com/isaacs/npm)
* [node-inspector]
* A WebKit based browser: Chrome, Safari, etc.

### Install

* With [npm](http://github.com/isaacs/npm)
        $ npm install -g node-inspector
ps: node-inspector 
http://stackoverflow.com/questions/11695739/installing-node-inspector-on-windows
### Debugging

1. start the inspector. I usually put it in the background

		$ node-inspector &

2. open http://127.0.0.1:8080/debug?port=5858 in your favorite WebKit based browser

3. you should now see the javascript source from node. If you don't, click the scripts tab.

4. select a script and set some breakpoints (far left line numbers)

5. then watch the [screencasts](http://www.youtube.com/view_play_list?p=A5216AC29A41EFA8)

For more information on getting started see the [wiki](http://github.com/dannycoates/node-inspector/wiki/Getting-Started---from-scratch)

node-inspector works almost exactly like the web inspector in Safari and
Chrome. Here's a good [overview](http://code.google.com/chrome/devtools/docs/scripts.html) of the UI
  