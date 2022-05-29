# This file is part of Plain Aligner
#
# Plain Aigner is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# Plain Aligner is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Plain Aligner.
# If not, see <https://www.gnu.org/licenses/>.
import logging
from pathlib import Path
from datetime import datetime
import xml.dom
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
    def __init__(self, src_lang, tar_lang, bitext_lines):
        """source and target lang should be ISO codes e.g. es-ES
        bitext_lines must be an interable with pairs of (source, target) strings
        """
        dtd = self.mk_doctype()
        self.doc = self.dom.createDocument(None, 'tmx', dtd)
        self.doc.encoding = 'UTF-8'
        self.root = self.doc.documentElement
        self.root.setAttribute('version', config.TMX_VERSION)
        header = self.doc.createElement('header')
        header = self.root.appendChild(header)
        self.set_attrs(header, config.HEADER_ATTRS)
        header.setAttribute('srclang', src_lang)
        self.body = self.doc.createElement('body')
        self.root.appendChild(self.body)

        self.creationdate = datetime.today().strftime(config.ISO_8601_FMT)
        self.src_lang = src_lang
        self.tar_lang = tar_lang
        self.append_tus(bitext_lines)

    def set_attrs(self, elem, attrs):
        for k, v in attrs.items():
            elem.setAttribute(k, v)

    def append_tuv(self, tu, text, lang):
        attrib = {'xml:lang': lang,
                  'creationdate': self.creationdate,
                  'creationtool': 'plain_aligner'}
        tuv = self.doc.createElement('tuv')
        self.set_attrs(tuv, attrib)
        seg = self.doc.createElement('seg')
        tnode = self.doc.createTextNode(escape(text))
        seg.appendChild(tnode)
        tuv.appendChild(seg)
        tu.appendChild(tuv)

    def append_tus(self, bitext_lines):
        for s, t in bitext_lines:
            tu = self.doc.createElement('tu')
            tu.setAttribute('srclang', self.src_lang)
            self.body.appendChild(tu)
            self.append_tuv(tu, s, self.src_lang)
            self.append_tuv(tu, t, self.tar_lang)

    def mk_doctype(self):
        self.dom = xml.dom.getDOMImplementation()
        tmxdoctype = self.dom.createDocumentType("tmx",
                                                 None,
                                                 config.TMX_DTD_NAME)
        return tmxdoctype

    def save(self, path=None):
        if not isinstance(path, Path):
            path = Path(path)
        if not path.suffix == '.tmx':
            path = path.with_suffix('.tmx')
        try:
            with path.open('w') as fd:
                self.doc.writexml(fd, addindent='  ', encoding='utf-8')
        except Exception as E:
            log.error(E)


def align(src_lang, tar_lang, src_file, tar_file):
    return TmxFactory(src_lang, tar_lang,
                      bitext_lines(src_file, tar_file))
