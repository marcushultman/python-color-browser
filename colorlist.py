import os.path
from html.parser import HTMLParser
import pickle

class ColorListParser(HTMLParser):
    def __init__(self, sourcecode=None):
        HTMLParser.__init__(self)
        self.data = dict()
        self._current = {'key':None, 'value':None}
        self._readcolor = False
        self._readname = False
        if sourcecode:
            self.feed(sourcecode)
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self._readcolor = True
            return
        if self._readcolor:
            attrs = dict(attrs)
            if tag == 'a' and 'title' in attrs:
                self._readname = True
            if tag == 'p' and 'title' in attrs:
                self._current['value'] = attrs['title'].split(' ')[-1]
    def handle_endtag(self, tag):
        if tag == 'div':
            self.data[self._current['key']] = self._current['value']
            self._readcolor = False
    def handle_data(self, data):
        if self._readcolor and self._readname:
            self._current['key'] = data
            self._readname = False

def load():
    if os.path.isfile('colordata.pkl'):
        input_file = open('colordata.pkl', 'rb')
        data = pickle.load(input_file)
        input_file.close()
        return data

    import urllib.request
    import json
    htmlsource = json.loads(urllib.request.urlopen('http://en.wikipedia.org/w/api.php?action=parse&format=json&prop=text&section=1&page=List_of_colors_(compact)&disabletoc').read().decode('utf-8'))['parse']['text']['*']
    
    current = {'key':None, 'value':None}
    parser = ColorListParser(htmlsource)
    data = parser.data
    
    output = open('colordata.pkl', 'wb')
    pickle.dump(data, output)
    output.close()
    parser.close()
    return data
