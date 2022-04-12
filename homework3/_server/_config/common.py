import os

ip_address = '127.0.0.1'
port = 7177
base_dir = os.path.dirname(os.path.abspath(__file__))

DB_FILE_PATH = os.path.join(os.path.dirname(base_dir), 'db', 'users.xlsx')
USER_FOLDER_PATH = os.path.join(os.path.dirname((base_dir)), 'files')

'''
homework3/_server/_config
homework3/_server/db/users.xlsx
homework3/_server/files

'''
