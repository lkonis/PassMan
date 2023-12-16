import os
from datetime import datetime
import pickle as pkl
import hashlib

from encrypt_binary import encrypt_file, decrypt_file

class Repeated:
    def __init__(self, user=None, password=None):
        item = {'time': datetime.now(), 'user': user, 'pass': password}
        self.item_list = []
        self.item_list.append(item)

    def add_item(self, user=None, password=None):
        item = {'user': user, 'pass': password, 'time': datetime.now()}
        self.item_list.append(item)
    def get_item(self,i):
        return self.item_list[i]


def createRecord():
    return {'Account': '', 'Nrec': 0, 'Records': Repeated(), 'Comment': ''}


class NewAccountManager:
    """
    Class NewAccountManager
    methods:
    * open_database_file
    * check_valid_db
    * save_dataBase
    * add_record
    * delete_record
    """

    def __init__(self):
        use_pass = False
        self.dbFile = "acc_psw.db"
        self.recDatabase = list()
        self.encrypted = False
        password = b'blabla'#get_random_bytes(32)
        self.password_in = hashlib.sha256(password).digest()[:16]
        self.password_out = hashlib.sha256(password).digest()[:16]

    def _findInDB(self, ac):
        for indx, item in enumerate(self.recDatabase):
            if item['Account'] == ac:
                return indx
        return -1

    def open_database_file(self, ask_pass=None, password=None):
        # first check if un-coded database file exists
        if os.path.isfile(self.dbFile):
            with open(self.dbFile, 'rb') as infile:
                self.recDatabase = pkl.load(infile)
                # check if valid
                if not self.check_valid_db():
                    return "Not valid"
                else:
                    return 'decrypted'
        elif os.path.isfile(self.dbFile+".coded"):
            #decrypt_file(self.dbFile+".coded", self.dbFile+".decoded", key=self.password)
            #self.recDatabase = pkl.load(open(self.dbFile+".decoded", "rb"))
            if ask_pass==None or ask_pass.lower()=='no':
                if not decrypt_file(self.dbFile +".coded", self.dbFile +".decoded", key=self.password_out):
                    return self.dbFile
                self.recDatabase = pkl.load(open(self.dbFile+".decoded", "rb"))
                # check if valid
                if not self.check_valid_db():
                    return "not valid"
            else:
                if password==None:
                    in_pass = input("Enter password: ")
                else:
                    in_pass = password
                self.password_out = hashlib.sha256(in_pass.encode('utf-8')).digest()[:16]

                if not decrypt_file(self.dbFile +".coded", self.dbFile +".decoded", key=self.password_out):
                    return "not valid"
                self.recDatabase = pkl.load(open(self.dbFile + ".decoded", "rb"))
        # no file found
        else:
            return "no file"
        # found and decrypted file successfully
        return "decrypted"
    def createNewFile(self):
        return self.dbFile
    def save_dataBase(self, password=None):
        # update password
        if not password==None:
            self.password_out = self.password_in = password
        # dump database into pickled file
        with open(self.dbFile, 'wb') as fi:
            pkl.dump(self.recDatabase, fi)
        # if there's a password, encrypted (and save) pickled file
        if not self.password_in == None:
            encrypt_file(self.dbFile, self.dbFile +".coded", key=self.password_in)
            decrypt_file(self.dbFile +".coded", self.dbFile +".decoded", key=self.password_out)
            unpickled = pkl.load(open(self.dbFile+".decoded", "rb"))
            return unpickled

    def add_record(self, ac=None, usr=None, psw=None, comment=None, force=None):
        """
        adding new record (or modifying existing record)\n
        ac: account name\n
        usr: user name\n
        psw: password\n
        force: if 'yes', override without waiting for confirmation\n
        """
        db = self.recDatabase
        # check if record exists already
        repeated = Repeated(user=usr, password=psw)
        found_indx = self._findInDB(ac)
        if found_indx == -1:
            rec = createRecord()
            rec['Account'] = ac
            rec['Nrec'] = 1
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
            if answer=="":
                answer="yes"
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
    if not ac1.open_database_file(ask_pass='yes'):
        # start new database
        pass
    if not ac1.delete_record(ac='ac8'):
        print('requested account ac8 not exit')
    ac1.add_record(ac='ac3', usr='oh_something', psw='notreal')
    ac1.add_record(ac='ac8', usr='nur', psw='1abcd', force='yes')
    ac1.add_record(ac='ac5', usr='nur', psw='1abcd', force='yes')
    unpickled=ac1.save_dataBase()
    print(unpickled)
