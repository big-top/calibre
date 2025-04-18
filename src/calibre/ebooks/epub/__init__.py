__license__   = 'GPL v3'
__copyright__ = '2008, Kovid Goyal kovid@kovidgoyal.net'
__docformat__ = 'restructuredtext en'

'''
Conversion to EPUB.
'''
from calibre.utils.zipfile import ZIP_STORED, ZipFile


def rules(stylesheets):
    for s in stylesheets:
        if hasattr(s, 'cssText'):
            for r in s:
                if r.type == r.STYLE_RULE:
                    yield r


def simple_container_xml(opf_path, extra_entries=''):
    return f'''\
<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
   <rootfiles>
      <rootfile full-path="{opf_path}" media-type="application/oebps-package+xml"/>
      {extra_entries}
   </rootfiles>
</container>
    '''


def initialize_container(path_to_container, opf_name='metadata.opf',
        extra_entries=[]):
    '''
    Create an empty EPUB document, with a default skeleton.
    '''
    rootfiles = ''
    for path, mimetype, _ in extra_entries:
        rootfiles += f'<rootfile full-path="{path}" media-type="{mimetype}"/>'
    CONTAINER = simple_container_xml(opf_name, rootfiles).encode('utf-8')
    zf = ZipFile(path_to_container, 'w')
    zf.writestr('mimetype', b'application/epub+zip', compression=ZIP_STORED)
    zf.writestr('META-INF/', b'', 0o755)
    zf.writestr('META-INF/container.xml', CONTAINER)
    for path, _, data in extra_entries:
        zf.writestr(path, data)
    return zf
