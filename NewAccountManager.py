import os
from datetime import datetime
import pickle as pkl
import hashlib

from encrypt_binary import encrypt_file, decrypt_file

class Repeated:
    def __init__(self, user=None, password=None):
        item = {'time': datetime.now(), 'user': user, 'pass': password}
        self.list = []
        self.list.append(item)

    def add_item(self, user=None, password=None):
        item = {'user': user, 'pass': password, 'time': datetime.now()}
        self.list.append(item)


def createRecord():
    return {'Account': '', 'Nrec': 0, 'Records': Repeated(), 'Comment': ''}


class NewAccountManager:

    def __init__(self):
        use_pass = False
        self.dbFile = "acc_psw.db"
        self.recDatabase = list()
        self.encrypted = False
        password = b'blabla'#get_random_bytes(32)
        self.password = hashlib.sha256(password).digest()[:16]
    def _findInDB(self, ac):
        for indx, item in enumerate(self.recDatabase):
            if item['Account'] == ac:
                return indx
        return -1

    def open_database_file(self):
        # check if un coded database file exists
        if os.path.isfile(self.dbFile):
            with open(self.dbFile, 'rb') as infile:
                self.recDatabase = pkl.load(infile)
                # check if valid
                if not self.check_valid_db():
                    return False
        elif os.path.isfile(self.dbFile+".coded"):
            #decrypt_file(self.dbFile+".coded", self.dbFile+".decoded", key=self.password)
            #self.recDatabase = pkl.load(open(self.dbFile+".decoded", "rb"))
            decrypt_file(self.dbFile+".coded", self.dbFile+".decoded", key=self.password)
            self.recDatabase = pkl.load(open(self.dbFile+".decoded", "rb"))

        # no file found
        return True
    def save_dataBase(self):
        # dump database into pickled file
        with open(self.dbFile, 'wb') as fi:
            pkl.dump(self.recDatabase, fi)
        # if there's a password, encrypted (and save) pickled file
        if not self.password==None:
            encrypt_file(self.dbFile, self.dbFile+".coded", key=self.password)
            decrypt_file(self.dbFile+".coded", self.dbFile+".decoded", key=self.password)
            unpickled = pkl.load(open(self.dbFile+".decoded", "rb"))
            return unpickled

    def add_record(self, ac=None, usr=None, psw=None, comment=None, force=None):
        db = self.recDatabase
        # check if record exists already
        repeated = Repeated(user=usr, password=psw)
        found_indx = self._findInDB(ac)
        if found_indx == -1:
            rec = createRecord()
            rec['Account'] = ac
            rec['Nrec'] = 0
            rec['Records'] = repeated
            if comment is None:
                rec['Comment'] = ''
            else:
                rec['Comment'] = comment
            db.append(rec)
            self.recDatabase = db
        else:
            if force is None:
                answer = input(f'Record {ac} exist, update? [Yes]')
            else:
                answer = 'yes'

            if not answer.lower() == 'yes':
                return
            else:
                db_upd = db[found_indx]
                historyRec = db_upd['Records']
                db_upd['Account'] = ac
                db_upd['Nrec'] += 1
                historyRec.add_item(user=usr, password=psw)
                if comment is None:
                    db_upd['Comment'] = ''
                else:
                    db_upd['Comment'] = comment
                self.recDatabase = db

    def is_encrypted(self):
        return self.encrypted
    def check_valid_db(self):
        if self.recDatabase == []:
            return False
        if not isinstance(self.recDatabase, list):
            return False
        first = self.recDatabase[0]
        if not isinstance(first,dict):
            return False
        if not 'Account' in first.keys():
            self.encrypted=True
            return False
        return True

    def delete_record(self, ac):
        found_indx = self._findInDB(ac)
        if found_indx > -1:
            db = self.recDatabase
            del db[found_indx]
            return True
        else:
            return False

if __name__ == '__main__':
    ac1 = NewAccountManager()
    if not ac1.open_database_file():
        exit()
    if not ac1.delete_record(ac='ac3'):
        print('requested account ac2 not exit')
    ac1.add_record(ac='ac3', usr='oh_something', psw='notreal')
    ac1.add_record(ac='ac8', usr='nur', psw='1abcd', force='yes')
    ac1.add_record(ac='ac5', usr='nur', psw='1abcd', force='yes')
    unpickled=ac1.save_dataBase()
    print(unpickled)
