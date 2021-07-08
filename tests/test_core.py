from cryptography.fernet import Fernet

from mask_in_situ.core import encrypt_string, decrypt_string

key = Fernet.generate_key()


def test_encryption_changes():
    original = "THIS IS A %MASK{TEST} SECRET"
    assert (encrypt_string(original, key) != original)


def test_different_plaintext_encrypts_differently():
    raw1 = "THIS IS A %MASK{SECRET}."
    raw2 = "THIS IS A %MASK{DIFFERENT secret SECRET}."

    assert (encrypt_string(raw1, key) != encrypt_string(raw2, key))


def test_encryption_reversible():
    raw = "THIS IS A TEST SECRET"
    original = "THIS IS A %MASK{TEST} SECRET"

    masked = encrypt_string(original, key)
    assert (masked != raw)
    assert (masked != original)

    unmasked = decrypt_string(masked, key)
    assert (raw == unmasked)
