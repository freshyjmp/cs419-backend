from html.parser import HTMLParser

class WaltzHTMLParser(HTMLParser):
    def __init__(self):
        self.links = []
        super().__init__()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.links.append(str(attr[1]))

