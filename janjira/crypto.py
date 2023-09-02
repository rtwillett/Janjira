class KeyringInterface:
    
    def __init__(self, key_type = 'local', salt_path = None):
        import os
    
        
        if salt_path is None: 
            self.salt_path = os.path.expanduser('~') + '/salts'
        else:         
            self.salt_path = salt_path
    
        if key_type == 'local':
            self.keyring_path = os.path.expanduser('~') + '/keyring'
        elif key_type == 'shared':
            # Insert code to implement a shared keyring
            raise Exception("Shared keyring is not currently implemented")
        else:
            raise Exception("Invalid key type") 
            
        
        self.read_keyring('.key')
            
    def read_keyring(self, file_extension:str) -> None: 
        from glob import glob

        self.keys = glob(ki.keyring_path + f'/*{file_extension}')
        
    def load_key(self, key_name:str, key_extension:str) -> str:
        with open(f'{self.keyring_path}/{key_name}{key_extension}', 'rb') as f: 
            self.key = f.read()
        
    def load_salt(self, salt_name:str) -> str:
        
        with open(f'{self.salt_path}/{salt_name}.txt', 'rb') as f: 
            self.salt = f.read()


class CreateSymmetricKey:
    '''Docstring'''
    
    def __init__(self, key_interface):
        import os
        
        self.key_extensions = r'.key'
        
        self.keyring_path = key_interface.keyring_path
        self.salt_path = key_interface.salt_path
            
        self.check_local_keyring()

    def check_local_keyring(self, keyring_path = None):

        import os

        if not os.path.exists(self.keyring_path):
            try:
                os.mkdir(self.keyring_path)
#             print("Doesn't exist")
            except: 
                raise Exception(f"Could not create the keyring directory at {self.keyring_path}")
        else: 
            print("Keyring directory exists")   
            
    def create_symmetric_key(self, key_name):
        from cryptography.fernet import Fernet
        key = Fernet.generate_key()

        print(key)
        file = open(f"{self.keyring_path}/{key_name}{self.key_extensions}", 'wb')
        file.write(key)
        file.close()

    def create_symmetric_key_return(self):
        from cryptography.fernet import Fernet
        return Fernet.generate_key()

class CryptoFernet():
    '''
    Docstring
    '''
    
    def __init__(self, keyname, key_interface):
        import os
        
        self.keyname = keyname
        self.key = key_interface.key
        self.salt = key_interface.salt
        
    def encrypt_string(self, plaintext):
        from cryptography.fernet import Fernet
        
        fn = Fernet(self.key)
        ciphertext = fn.encrypt(plaintext.encode())
        return ciphertext
    
    def decrypt_string(self, ciphertext):
        from cryptography.fernet import Fernet
        
        fn = Fernet(self.key)
        plaintext = fn.decrypt(ciphertext)
        return plaintext.decode()
    
    def encrypt_file(self, filepath, savepath, delete_original = False):
        from cryptography.fernet import Fernet
        
        with open(filepath, 'rb') as f: 
            plaintext = f.read()
        
        fn = Fernet(self.key)
        ciphertext = fn.encrypt(plaintext)
        
        with open(savepath, 'wb') as f: 
            f.write(ciphertext)
        
        if delete_original:
            print("Your file has been encrypted and deleted")
            # Insert code that would delete the original file. We have no use for this at present but
            # might want to build this out in the future.
        else: 
            print("A copy of your file has been encrypted. The original remains where it is.")
    
    def decrypt_file(self, filepath, savepath):
        from cryptography.fernet import Fernet
        
        with open(filepath, 'rb') as f: 
            ciphertext = f.read()
            
        fn = Fernet(self.key)
        plaintext = fn.decrypt(ciphertext)

        with open(savepath, 'wb') as f: 
            f.write(plaintext)

def create_alphanumeric_token(n: int) -> str:
    '''
    Takes an integer and returns and alphanumeric string with length of that integer.
    '''

    import numpy as np
    import string

    big_rand_string = string.ascii_letters + string.digits
    big_rand = [n for n in big_rand_string]
    return ''.join(np.random.choice(big_rand, size = n))
