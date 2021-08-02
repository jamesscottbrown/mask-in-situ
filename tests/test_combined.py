import os

from cryptography.fernet import Fernet
from click.testing import CliRunner

from mask_in_situ.cli import encrypt, decrypt, encrypt_dir, decrypt_dir

key = Fernet.generate_key()
os.makedirs("test_output", exist_ok=True)


def test_single_file_roundtrip():
    """
    This testa an encryption-decryption round-trip of a single file
    """
    runner = CliRunner()

    original = "THIS IS A TEST SECRET"
    to_mask = "THIS IS A %MASK{TEST} SECRET"

    file_to_mask = os.path.join('test_output', 'to_mask.txt')
    with open(file_to_mask, 'w') as fp:
        fp.write(to_mask)

    os.environ['TEST_KEY'] = key.decode()

    file_masked = os.path.join('test_output', 'masked.txt')
    result_1 = runner.invoke(encrypt, ['-e', 'TEST_KEY', file_to_mask, file_masked])
    assert result_1.exit_code == 0

    file_unmasked = os.path.join('test_output', 'unmasked.txt')
    result_2 = runner.invoke(decrypt, ['-e', 'TEST_KEY', file_masked, file_unmasked])
    assert result_2.exit_code == 0

    with open(file_masked, 'r') as fp:
        masked = fp.read()
        assert masked != original

    with open(file_unmasked, 'r') as fp:
        unmasked = fp.read()
        assert unmasked == original


def test_directory_roundtrip():
    """
    This tests an encryption-decryption round-trip of a directory
    """
    runner = CliRunner()

    original = "THIS IS A TEST SECRET"
    to_mask = "THIS IS A %MASK{TEST} SECRET"

    test_dir = 'test_output/directory'
    dir_to_mask = os.path.join(test_dir, 'to_mask')

    os.makedirs(os.path.join(dir_to_mask, 'foo'), exist_ok=True)
    os.makedirs(os.path.join(dir_to_mask, 'foo', 'bar'), exist_ok=True)

    files = [
        os.path.join('foo', '1.txt'),
        os.path.join('foo', '2.txt'),
        os.path.join('foo', 'bar', '3.txt'),
        os.path.join('foo', 'bar', '4.txt'),
    ]

    files_to_exclude = [
        os.path.join('foo', '.DS_Store')
    ]

    for file in files:
        file_to_mask = os.path.join(dir_to_mask, file)
        with open(file_to_mask, 'w') as fp:
            fp.write(to_mask)

    for file in files_to_exclude:
        file_to_mask = os.path.join(dir_to_mask, file)
        with open(file_to_mask, 'w') as fp:
            fp.write(" ")

    os.environ['TEST_KEY'] = key.decode()

    dir_masked = os.path.join(test_dir, 'masked')
    result_1 = runner.invoke(encrypt_dir, ['-e', 'TEST_KEY', dir_to_mask, dir_masked])
    assert result_1.exit_code == 0

    dir_unmasked = os.path.join(test_dir, 'unmasked')
    result_2 = runner.invoke(decrypt_dir, ['-e', 'TEST_KEY', dir_masked, dir_unmasked])
    assert result_2.exit_code == 0

    # Assert initial files unchanged
    for file in files:
        file_to_mask = os.path.join(dir_to_mask, file)
        with open(file_to_mask, 'r') as fp:
            assert fp.read() == to_mask

    # Assert masked files are different from original or to_mask files
    for file in files:
        file_masked = os.path.join(dir_masked, file)
        with open(file_masked, 'r') as fp:
            assert fp.read() != to_mask
            assert fp.read() != original

    # Assert excluded files are not masked
    for file in files_to_exclude:
        file_masked = os.path.join(dir_masked, file)
        assert not os.path.exists(file_masked)

    # Assert unmasked files are correct
    for file in files:
        file_unmasked = os.path.join(dir_unmasked, file)
        with open(file_unmasked, 'r') as fp:
            assert fp.read() == original
