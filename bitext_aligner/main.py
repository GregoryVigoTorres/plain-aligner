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
