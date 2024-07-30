from ansible.parsing.vault import VaultLib, VaultSecret
from ansible.constants import DEFAULT_VAULT_ID_MATCH

import yaml
import base64 

class VaultHelper(object): 
    """
        VaultHelper

        This is a helper utility for parsing encrypted ansible vault files
    """
    def __init__(self) -> None:
        return

    def parse(vault_file, vault_password):
        vault_secret = VaultSecret(base64.b64encode(vault_password.encode('utf-8')))
        vault = VaultLib([(DEFAULT_VAULT_ID_MATCH, vault_secret)])

        # Read the vault file content
        with open(vault_file, 'rb') as f:
            vault_content = f.read()

        # Decrypt the vault content
        decrypted_content = vault.decrypt(vault_content).decode('utf-8')

        return decrypted_content