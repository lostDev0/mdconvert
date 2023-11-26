import typer
import pickle
from mdconvert import handlers

g_cache = u'cache.pickle'

# create the application
g_app = typer.Typer()

# create readers and writers
g_reader = typer.Typer()
g_writer = typer.Typer()

# determine what language we're working with
g_asciidoc = typer.Typer()
g_html = typer.Typer()

def html_typer():
    g_html.add_typer(g_reader, name="read", help="Read html")
    g_html.add_typer(g_writer, name="write", help="Write html")

    doc = handlers.html_writer()
    g_html.add_typer(doc._typer, name="create", help="Create html output from stdin content")

def asciidoc_typer():
    # set the proper language typer
    # command example:
    #   asciidoc read file input.adoc
    #   asciidoc write file output.adoc
    g_asciidoc.add_typer(g_reader, name="read", help="Read asciidoc")
    g_asciidoc.add_typer(g_writer, name="write", help="Write asciidoc")

    doc = handlers.asciidoc_writer()
    g_asciidoc.add_typer(doc._typer, name="create", help="Create asciidoc output from stdin content")

    class reader:
        @g_reader.command()
        def file(file_path: str):
            """
            Read a file and place it in cache
            """
            typer.echo(f'reading "{file_path}" ...')

            content = []
            with open(file_path, 'r') as f:
                content = f.readlines()

            num_lines = len(content)
            content = '\n'.join(content)

            typer.echo(f'read {num_lines} line(s) from "{file_path}"')

            typer.echo(f'converting asciidoc to html ...')

            # source type
            src = handlers.asciidoc_reader()

            # destination type
            dst = handlers.html_writer()

            # do the conversion
            resolver = handlers.resolver(src, dst)

            typer.echo(f'writing html to debug file "cache.html"')
            with open('cache.html', 'w') as f:
                f.write(content)

            typer.echo(f'writing html to "{g_cache}" ...')

            with open(g_cache, 'wb') as f:
                pickle.dump(content, f)

        @g_reader.command()
        def string(content: str):
            """
            Read a file and place it in cache
            """
            typer.echo(f'reading stdin ...')

            with open(g_cache, 'w') as f:
                pickle.dump(f, content)

    class writer:
        @g_writer.command()
        def file(file_path: str):
            """
            Read a file and place it in cache
            """
            typer.echo(f'reading html from "{g_cache}" ...')

            content = ''
            with open(g_cache, 'rb') as f:
                content = pickle.load(f)

            typer.echo(f'converting html content to asciidoc')

            h = handlers.html_reader()
            a = handlers.asciidoc_writer()
            content = h.feed(a, content)
            
            typer.echo(f'writing asciidoc to "{file_path}"')
            
            with open(file_path, 'w') as f:
                f.writelines(content)

        @g_writer.command()
        def string(content: str):
            """
            Read a file and place it in cache
            """
            typer.echo(f'{content}')

asciidoc_typer()
html_typer()

g_app.add_typer(g_asciidoc, name="asciidoc", help="Working with the asciidoc language")
