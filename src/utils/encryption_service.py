import base64
import hashlib
from cryptography.fernet import Fernet

class EncryptionService:
    _fernet_instances: dict[str, Fernet] = {}

    @staticmethod
    def get_key(password: str):
        hash_key = hashlib.blake2b(password.encode(), digest_size=16).hexdigest()
        encoded = base64.urlsafe_b64encode(hash_key.encode())
        return encoded
        

    @classmethod
    def get_fernet(cls, password: str):
        # if already exists, return existing fernet instance
        if password in cls._fernet_instances:
            return cls._fernet_instances[password]
        
        # otherwise generate one
        fernet = Fernet(key=cls.get_key(password))
        cls._fernet_instances[password] = fernet
        return fernet
    
    @classmethod
    def encrypt_file(cls, file_path: str, password: str):
        # read plain data
        with open(file_path, 'rb') as file:
            binary_data = file.read()

        # encyrpt data
        fernet = cls.get_fernet(password)
        encrypted_data = fernet.encrypt(binary_data)

        # store encrypted
        with open(file_path, 'wb') as file:
            file.write(encrypted_data)

    @classmethod
    def decrypt_file(cls, file_path: str, password: str):
        # read encrypted data
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()

        # encyrpt data
        fernet = cls.get_fernet(password)
        decrypted_data = fernet.decrypt(encrypted_data)

        # store decrypted
        with open(file_path, 'wb') as file:
            file.write(decrypted_data)