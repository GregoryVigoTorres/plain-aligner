from pathlib import Path

from bitext_aligner import align, AlignerError


# This doesn't test whether the tmx is actually valid


def test_aligner_aligns(src_path, tar_path):
    try:
        tmx = align('en-US', 'en-GB', src_path, tar_path)
        tus = tmx.body.getElementsByTagName('tu')
        assert len(tus) > 0
    except Exception as E:
        raise E


def test_files_different_length(src_path, long_tar_path):
    try:
        align('en-US', 'en-GB', src_path, long_tar_path)
    except AlignerError:
        pass
    except Exception as E:
        raise E


def test_write_tmx(tmp_path, src_path, tar_path):
    path = Path(tmp_path).joinpath('test.tmx')
    try:
        tmx = align('en-US', 'en-GB', src_path, tar_path)
        tmx.save(path=path)
    except Exception as E:
        raise E
