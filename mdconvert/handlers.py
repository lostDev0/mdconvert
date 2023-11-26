from mdconvert.app import *
from mdconvert.decorators import *
from html.parser import HTMLParser
from mdconvert.block_types import block
import re
from collections.abc import Callable

g_hide_uri_scheme = False   # http://www.google.com becomes www.google.com
g_hide_section_numbers = False # 1.2 Section becomes Section

# (content: str, flags: {})
CallableType = Callable[[re.match], (str, {})]

class interface_reader:
    """
    Reads the given language data looking for the registered patterns. It invokes the callback when a pattern match occurs.
    """
    def __init__(self, writer):
        self._callbacks = {}
        self._writer = writer

    def register(self, pattern: str, callback: CallableType, btype: block) -> None:
        self._callbacks[re.compile(pattern)] = [callback, btype]

    def feed(self, data: str) -> str:
        iter = enumerate(str.splitlines())
        for idx, line in iter:
            for pattern, callable in self._callbacks:
                for match in re.finditer(pattern, line):
                    (content, flags) = callable[0](match, iter)
                    # line could now be many lines
                    match callable[1]:
                        case block.SECTION:
                            self._writer.section(content, flags)
                            

class interface_writer:
    def __init__(self):
        pass
        
    def bold(self, content: str, flags={}):
        pass

    def italic(self, content: str, flags={}):
        pass

    def monospace(self, content: str, flags={}):
        pass

    def superscript(self, content: str, flags={}):
        pass

    def subscript(self, content: str, flags={}):
        pass

    def underline(self, content: str, flags={}):
        pass

    def strike_through(self, content: str, flags={}):
        pass

    def small(self, content:str, flags={}):
        pass

    def overline(self, content: str, flags={}):
        pass

    def image(self, content: str, flags={}):
        pass

    def literal(self, content: str, flags={}):
        pass

    def literal_block(self, content: str, flags={}):
        pass

    def code_block(self, content: str, flags={}):
        pass

    def admonition(self, content: str, flags={}):
        pass

    def table(self, content: str, flags={}):
        pass

    def table_cell(self, content: str, flags={}):
        pass

    def include(self, content: str, flags={}):
        pass

    def listing(self, content: str, flags={}):
        pass

    def listing_block(self, content: str, flags={}):
        pass

    def callout(self, content: str, flags={}):
        pass

    def section(self, content: str, flags={}):
        pass

    def hide_uri_scheme(self, content: str, flags={}):
        g_hide_uri_scheme = True

    def hide_section_numbers(self, content: str, flags={}):
        g_hide_section_numbers = True

    def show_uri_scheme(self, content: str, flags={}):
        g_hide_uri_scheme = False

    def show_section_numbers(self, content: str, flags={}):
        g_hide_section_numbers = False

    def line_break(self, content: str, flags={}):
        pass


class asciidoc_reader(interface_reader):
    def __init__(self):
        interface_reader.__init__(self)
        self.register(r'^(?P<escape>\\)?=+ .+ *$', block.SECTION)

    # TODO - override feed()

class asciidoc_writer(interface_writer):
    _typer = typer.Typer()

    def __init__(self):
        interface_writer.__init__(self)

    @staticmethod
    @_typer.command()
    def bold(content: str, flags={}):
        """
        Make content bold
        """
        return f'*{content}*'

    @staticmethod
    @_typer.command()
    def italic(content: str, flags={}):
        """
        Make content italic
        """
        return f'_{content}_'

    @staticmethod
    @_typer.command()
    def monospace(content: str, flags={}):
        """
        Make content monospace
        """
        return f'`{content}`'

    @staticmethod
    @_typer.command()
    def superscript(content: str, flags={}):
        """
        Make content superscript
        """
        return f'^{content}^'

    @staticmethod
    @_typer.command()
    def subscript(content: str, flags={}):
        """
        Make content subscript
        """
        return f'~{content}~'

    @staticmethod
    @_typer.command()
    def underline(content: str, flags={}):
        """
        Make content underlined
        """
        return f'[.underline]#{content}#'

    @staticmethod
    @_typer.command()
    def strike_through(content: str, flags={}):
        """
        Make content strike-through the middle
        """
        return f'[.line-through]#{content}#'

    @staticmethod
    @_typer.command()    
    def overline(content: str, flags={}):
        """
        Make content overlined
        """
        return f'[.overline]#{content}#'

    @staticmethod
    @_typer.command()
    def image(content: str, flags={}):
        """
        Make content an image
        """
        # Alt, width, height, options
        options = f"\"{flags['alt']}\"" if 'alt' in flags else u''
        start = u',' if len(options) > 0 else u''
        options = f'{start}{flags["width"]},{flags["height"]}' if 'width' in flags and 'height' in flags else u''

        for k,v in flags.items():
            if k != 'alt' and k != 'width' and k != 'height':
                options += f'{k}="{v}"'

        return f'image::{content}[{options}]'
    
    @staticmethod
    @_typer.command()
    def literal(content: str, flags={}):
        """
        Make content a literal with no substitutions
        """
        return f'[literal]\n{content}'

    @staticmethod
    @_typer.command()
    def literal_block(content: str, flags={}):
        """
        Make content into a literal block
        """
        tag = u'....'
        return f'{tag}\n{content}\n{tag}'

    @staticmethod
    @_typer.command()
    def code_block(content: str, flags={}):
        """
        Make content into a code block
        """
        tag = u'----'
        lang = f"\"{flags['lang']}\"" if 'lang' in flags else u''
        return f'[source,{lang}]{tag}\n{content}\n{tag}'

    @staticmethod
    @_typer.command()
    def admonition(content: str, flags={}):
        """
        Make content into an admonition block
        """
        pass

    @staticmethod
    @_typer.command()
    def table(content: str, flags={}):
        """
        Make content into a table
        """
        tag = u'!====' if 'sub-table' in flags else u'|===='
        return f'{tag}\n{content}\n{tag}' 

    @staticmethod
    @_typer.command()
    def table_cell(content: str, flags={}):
        """
        Make content into a table cell
        """
        pass

    @staticmethod
    @_typer.command()
    def include(content: str, flags={}):
        """
        Include content from a file
        """
        options = u''
        return f'include::{content}[{options}]'

    @staticmethod
    @_typer.command()
    def listing(content: str, flags={}):
        return f'[listing]\n{content}'
    
    @staticmethod
    @_typer.command()
    def listing_block(content: str, flags={}):
        tag = u'----'
        return f'{tag}\n{content}\n{tag}'
    
    @staticmethod
    @_typer.command()
    def callout(content: str, flags={}):
        pass

    @staticmethod
    @_typer.command()
    def section(content: str, flags={}):
        level = u'='*int(flags['level']) if 'level' in flags else u''
        return f'{level} {content}'
    
    @staticmethod
    @_typer.command()
    def hide_uri_scheme(content: str, flags={}):
        g_hide_uri_scheme = True
        return f':hide-uri-scheme:'

    @staticmethod
    @_typer.command()
    def hide_section_numbers(content: str, flags={}):
        g_hide_section_numbers = True
        return f':!numbered:'

    @staticmethod
    @_typer.command()
    def show_uri_scheme(content: str, flags={}):
        g_hide_uri_scheme = False
        return f':!hide-uri-scheme:'

    @staticmethod
    @_typer.command()
    def show_section_numbers(content: str, flags={}):
        g_hide_section_numbers = False
        return f':numbered:'

class html_resolver():
    def __init__(self, output_handler):
        self._handler = output_handler
        self._html_parser = html_resolver._html_parser()
    
    def feed(self, data: str) -> str:
        self._html_parser.feed(data)
        return self._html_parser.output()
    
    class _html_parser(HTMLParser, object):
        def __init__(self):
            super(html_reader._html_reader, self).__init__()
            self._handler = interface_writer()
            self._current_tag = []
            self._flags = {}
            self._output = ''
        
        def output(self):
            return self._output

        def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
            self._current_tag.append(tag)
            #match self._current_tag:
            #    case 'br':
            #        self._handler.line_break('', self._flags)
            return super().handle_starttag(tag)
        
        def handle_endtag(self, tag: str) -> None:
            super().handle_endtag(tag)
            self._current_tag.pop()
            return None
        
        def handle_data(self, data: str) -> None:
            if self._handler == None:
                return super().handle_data(data)
            
            content = u''
        
            match self._current_tag:
                case 'br':
                    content = self._handler.line_break(data, self._flags)
                case 'strong':
                    content = self._handler.bold(data, self._flags)
                case 'b':
                    content = self._handler.bold(data, self._flags)
                case 'em':
                    content = self._handler.italic(data, self._flags)
                case 'i':
                    content = self._handler.italic(data, self._flags)
                case 'strike':
                    content = self._handler.strike_through(data, self._flags)
                case 'small':
                    content = self._handler.small(data, self._flags)
                case _:
                    pass
                
            if content == u'':  # did nothing with the data
                self._output += data
            else:
                self._output += content

class html_reader(interface_reader):
    def __init__(self):
        interface_reader.__init__(self)

    # nothing to do as the default behavior for feed is to pass the content
            
class html_writer(interface_writer):
    _typer = typer.Typer()

    def __init__(self):
        interface_writer.__init__(self)

    @staticmethod
    @_typer.command()
    def bold(content: str, flags={}):
        """
        Make content bold
        """
        return f'<b>{content}</b>'