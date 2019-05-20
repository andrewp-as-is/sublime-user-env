#!/usr/bin/env python
import os
import sublime

"""
~/.config/sublime-text-3/User/.env                                  Linux
~/Library/Application Support/Sublime Text 3/Packages/User/.env     macOS
%APPDATA%\\Sublime Text 3\\User\\.env                               Windows
"""

SETTINGS = sublime.packages_path()
path = os.path.join(sublime.packages_path(),"User",".env")

def parse(line):
    """parse line and return a dictionary with variable value"""
    if line.lstrip().startswith('#'):
        return {}
    if not line.lstrip():
        return {}
    """find the second occurence of a quote mark:"""
    if line.find("export=") == 0:
        line = line.replace("export=", "")
    quote_delimit = max(line.find('\'', line.find('\'') + 1),
                        line.find('"', line.rfind('"')) + 1)
    """find first comment mark after second quote mark"""
    if '#' in line:
        line = line[:line.find('#', quote_delimit)]
    key, value = map(lambda x: x.strip().strip('\'').strip('"'),
                     line.split('=', 1))
    return {key: value}

try:
    if os.path.exists(path):
        for l in open(path).read().splitlines():
            data = parse(l)
            os.environ.update(data)
except Exception as e:
    sublime.error_message(str(e))
