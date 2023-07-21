HYPERLINK = ('button', 'nav', 'optgroup', 'option', 'select')
ADDRESS = ('address', '')
INDIRECT_INFORMATION = ('article', 'aside')
SOURCE = ('cite', 'source')
FOOTER = ('footer', 'tfoot')
HEADING = ('head', 'header', 'meta', 'title')
ANNOTATION = ('ruby', 'rb', 'rt', 'rtc', 'rp')
IGNORED = ('area', 'audio', 'base', 'br', 'canvas', 'datalist', 'dialog', 'embed', 'figcaption', 'figure', 'form',
           '!DOCTYPE', 'hr', 'iframe', 'img', 'input', 'kbd', 'label', 'legend', 'link', 'map', 'meter', 'noscript',
           'object', 'output', 'param', 'picture', 'progress', 'samp', 'script', 'style', 'track', 'video', 'wbr')
ALL_TAGS = ('button', 'nav', 'optgroup', 'option', 'select', 'address', 'article', 'cite', 'source', 'footer', 'tfoot',
            'head', 'header', 'meta', 'title', 'ruby', 'rb', 'rt', 'rtc', 'rp', 'area', 'audio', 'base', 'br', 'canvas',
            'datalist', 'dialog', 'embed', 'figcaption', 'figure', 'form', '!DOCTYPE', 'hr', 'iframe', 'img', 'input',
            'kbd', 'label', 'legend', 'link', 'map', 'meter', 'noscript', 'object', 'output', 'param', 'picture',
            'progress', 'samp', 'script', 'style', 'track', 'video', 'wbr', 'a', 'abbr', 'article', 'b', 'bdi', 'bdo',
            'blockquote', 'body', 'caption', 'code', 'col', 'colgroup', 'data', 'dd', 'del', 'details', 'dfn', 'div',
            'dl', 'dt', 'em', 'fieldset', 'h1-h6', 'html', 'i', 'ins', 'li', 'main', 'mark', 'ol', 'p', 'pre', 'q', 's',
            'section', 'small', 'span', 'strong', 'sub', 'summary', 'sup', 'table', 'tbody', 'td', 'template',
            'textarea', 'th', 'thead', 'time', 'tr', 'u', 'ul', 'var')
PUNCTUATION_MARKS_END = ['!', '?', '.']
PUNCTUATION_MARKS = [',', '"', '"', ':', ';', '(', ')', '-', '«', '»', '—']  # В современном русском
# языке 10 знаков препинания: точка, вопросительный знак, восклицательный знак, многоточие, двоеточие, точка с
# запятой, запятая, тире, двойное тире, скобки.
OTHER_SIGNS = ['#', '№', '$', '%', '^', '&', '*', '=', '+', '/', '{', '}', '[', ']', "'", '>', '<', '\\', '|', '`', '~']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
