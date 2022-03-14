import hashlib
from importlib.metadata import files
import json
import os

blockchain_dir = os.curdir + '/flask/app/blockchain/'

def get_files():
    files = os.listdir(blockchain_dir)
    return sorted([int(i) for i in files])


def get_hash(filename):
    file = open(blockchain_dir + filename, 'rb').read()
    return hashlib.md5(file).hexdigest()

def check_integrity():
    files = get_files()
    results = []
    for file in files[1:]:
        hh = json.load(open(blockchain_dir + str(file)))['hash']
        prev_file = str(file - 1)
        actual_hash = get_hash(prev_file)

        if hh == actual_hash:
            result = 'Ok'
        else:
            result = 'Corrupted'

        results.append({'block': prev_file, 'result': result})
        # print('block{} id : {}'.format(prev_file, result))        
    return results

def write_block(name, amount, to_whom, prev_hash=''):

    files = get_files()
    prev_file = files[-1]
    filename = str(prev_file + 1)
    prev_hash = get_hash(str(prev_file))

    data = {'name': name,
        'amount': amount,
        'to_whom':to_whom,
        'hash': prev_hash}

    with open(blockchain_dir + filename, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
   # write_block(name='oleg', amount='5', to_whom='Ksu')
   print(check_integrity()) 

if __name__ == '__main__': 
    main()