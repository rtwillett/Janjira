class CreateSymmetricKey:
    '''Docstring'''
    
    def __init__(self, key_type = 'local', salt_path = None):
        import os
    
        
        if salt_path is None: 
            self.salt_path = os.path.expanduser('~') + '/salt.txt'
        else:         
            self.salt_path = salt_path
        
        self.key_extensions = r'.key'
    
        if key_type == 'local':
            self.keyring_path = os.path.expanduser('~') + '/keyring'
        elif key_type == 'shared':
            # Insert code to implement a shared keyring
            raise Exception("Shared keyring is not currently implemented")
        else:
            raise Exception("Invalid key type") 
            
        self.check_local_keyring()
        
#         with open(r'./salt.txt', 'rb') as f: 
#             self.salt = f.read()

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
