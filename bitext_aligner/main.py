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

import click

from bitext_aligner.aligner import align


log = logging.getLogger(__name__)


@click.option('-sl', '--src-lang')
@click.option('-tl', '--tar-lang')
@click.option('-sf', '--src-file', type=click.Path(exists=True,
                                                   dir_okay=False,
                                                   resolve_path=True,
                                                   readable=True))
@click.option('-tf', '--tar-file', type=click.Path(exists=True,
                                                   dir_okay=False,
                                                   resolve_path=True,
                                                   readable=True))
@click.argument('dest', type=click.Path(dir_okay=False,
                                        resolve_path=True,
                                        writable=True,
                                        path_type=Path))
@click.command()
def cli(src_lang, tar_lang, src_file, tar_file, dest):
    """Align bitext files
    The files must have the same number of lines, where every pair of lines will
    be aligned in the memory.
    All options are required.
    """
    try:
        tmx = align(src_lang, tar_lang, src_file, tar_file)
        tmx.save(path=dest)
        log.info(f'TMX saved to {dest}')
    except Exception as E:
        log.error(E)


if __name__ == '__main__':
    cli()
