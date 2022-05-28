import logging
from pathlib import Path
from datetime import datetime
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape


from bitext_aligner import config


log = logging.getLogger(__name__)


class AlignerError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'<AlignerError {repr(self.value)}>'


def file_lines(path):
    if not isinstance(path, Path):
        path = Path(path)
    with path.open() as fd:
        return [i.strip() for i in fd]


def bitext_lines(src_file, tar_file):
    s = file_lines(src_file)
    t = file_lines(tar_file)
    try:
        # when Python 3.10 becomes the default use the strict=True keyword
        assert len(list(s)) == len(list(t))
        yield from zip(s, t)
    except AssertionError:
        raise AlignerError('The source and target files are not the same length')


class TmxFactory():
    def __init__(self, src_lang, tar_lang, bitext_lines, src_path, tar_path):
        self.root = ET.Element('tmx', attrib={'version': config.TMX_VERSION})
        self.header = ET.SubElement(self.root, 'header', attrib=config.HEADER_ATTRS)
        self.header.set('srclang', src_lang)
        self.body = ET.SubElement(self.root, 'body')
        self.creationdate = datetime.today().strftime(config.ISO_8601_FMT)

        self.src_path = Path(src_path).name
        self.tar_path = Path(tar_path).name

        self.src_lang = src_lang
        self.tar_lang = tar_lang
        self.bitext_lines = bitext_lines
        self.append_tus()
        self.tree = ET.ElementTree(self.root)

    def append_tuv(self, tu, text, lang, path):
        tuv = ET.SubElement(tu, 'tuv',
                            attrib={'xml:lang': lang,
                                    'creationdate': self.creationdate,
                                    'creationtool': 'plain_aligner'})
        note = ET.SubElement(tuv, 'note')
        note.text = f'segmentsource:"{path}"'
        seg = ET.SubElement(tuv, 'seg')
        seg.text = escape(text)

    def append_tus(self):
        for s, t in self.bitext_lines:
            tu = ET.SubElement(self.body, 'tu',
                               attrib={'srclang': self.src_lang})
            self.append_tuv(tu, s, self.src_lang, self.src_path)
            self.append_tuv(tu, t, self.tar_lang, self.tar_path)

    def save(self, path=None):
        if not isinstance(path, Path):
            path = Path(path)
        if not path.suffix == '.tmx':
            path = path.with_suffix('.tmx')
        with path.open('wb') as fd:
            self.tree.write(fd, encoding='utf-8',
                            xml_declaration=True,
                            short_empty_elements=False)


def align(src_lang, tar_lang, src_file, tar_file):
    """This is done like this to make testing easier"""
    return TmxFactory(src_lang, tar_lang,
                      bitext_lines(src_file, tar_file),
                      src_file, tar_file)
