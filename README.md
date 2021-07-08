# Mask in situ

Mask in situ (`maskis`) makes it easy to encrypt only specific sections of files (for example, secrets such as password in configuration files).

The intended use is to allow config files to be shared in a partially-encrypted form, so that secrets are protected but the overall structure of the file, and the value of non-sensitive options are visible.

## Usage

If you have a config file that contains secrets, indicate the values to be encrypted by enclosing them in `%MASK{..}`, then run the `encrypt1` command:

You cna generate a key using the `generate-key` subcommand.

...

You can provide the name of an environment variable containing the key as an option; if you do not, you will be prompted for a he key interactively.


## Alternatives

Listing an alternative tool below is not an endorsement: it means I am aware that the tool exists, not that I have evaluated it.

### Encrypt part of config file

By default, [SOPS](https://github.com/mozilla/sops) encrypts every value (but not hhe keys) in a YAML/JSON file, but it can [optionally encrypt only specific values](https://github.com/mozilla/sops#encrypting-only-parts-of-a-file).

However, it works only for YAMl/JSON files (not arbitrary text files).

### Encrypt the whole file

A significant number of tools have bene developed to handle the encryption of single files; many of these support integration with Git.

* [age](https://github.com/FiloSottile/age)
* [tomb](https://www.dyne.org/software/tomb/) (GNU/linux only)

* [git-crypt](https://github.com/AGWA/git-crypt)
* [git-encrypt](https://github.com/shadowhand/git-encrypt) - deprecated
* [git-remote-crypt](https://github.com/spwhitton/git-remote-gcrypt)
* [git-secret](https://github.com/sobolevn/git-secret)
  

([git-nerps](https://github.com/mk-fg/git-nerps), [git-blur](https://github.com/acasajus/git-blur), [git-easy-crypt](https://github.com/taojy123/git-easy-crypt))
  
* [BlackBox](https://github.com/StackExchange/blackbox) - specifically intended for secrets

* [pass](https://www.passwordstore.org/)
* [transcrypt](https://github.com/elasticdog/transcrypt)
* [keyringer](https://keyringer.pw/)

As the whole file is encrypted, checking or editing a non-sensitive part of the file requires decrypting it.


### Manually remove the secrets

The original file could be edited to manually replace the secrets with placeholders, and the secrets could be stored separately in a passwword manager or encrypted file.

When a file containing plaintext secrets is required, they can be manually retrieved and re-added.

However, this requires manual effort.
In particular, whenever any change is made, it must be manually made to both the file containing the placeholders, and any versions containing plaintext secrets.


### Automatically fetch secrets from a vault

An alternative is not store secrets in any config files, and instead load them from a centralised store provided by a system like:

* [HashiCorp Vault](https://www.vaultproject.io/)
* [Akeyless Vault](https://www.akeyless.io/)
* [Thycotic Secret Server](https://thycotic.com/products/secret-server/)
* [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)

This provides advantages like auditing and the ability to more easily rotate credentials, but requires additional infrastructure.


### Tool-specific approaches

These typically involving extracting secrets from a config to a separate encrypted file that is then imported.

* [Ansible vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html)
* [Docker-compose secrets](https://docs.docker.com/compose/compose-file/compose-file-v3/#secrets)/[Docker swarm secrets](https://docs.docker.com/engine/swarm/secrets/)
* [Kubernetes secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
...
