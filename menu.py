import sqlite3
import os

con = sqlite3.connect('records_db.sqlite')
con.row_factory = sqlite3.Row

con.execute('create table if not exists records (name text, country text, catches integer, UNIQUE(name COLLATE NOCASE))')

con.commit()

for row in con.execute('select * from records'):
    print(row['name'])

con.close()

with sqlite3.connect('records_db.sqlite') as con:
    con.execute('delete from records')
    con.execute('insert into records (name, country, catches) values ("Jim Jam", "United States", 89)')
con.close()

class Record:
    def __init__(self, name, country, catches, id=None):
        self.name = name
        self.country = country
        self.catches = catches
        self.id = id


class RecordError(Exception):
    ''' For Record Errors'''
    pass


"""
A menu - you need to add the database and fill in the functions. 
"""


def main():
    menu_text = """
    1. Display all records
    2. Search by name
    3. Add new record
    4. Edit existing record
    5. Delete record 
    6. Quit
    """

    while True:
        try:
            print(menu_text)
            choice = input('Enter your choice: ')
            if choice == '1':
                display_all_records()
            elif choice == '2':
                search_by_name()
            elif choice == '3':
                record = get_record_info()
                add_new_record(record)
            elif choice == '4':
                edit_existing_record()
            elif choice == '5':
                delete_record()
            elif choice == '6':
                break
            else:
                print('Not a valid selection, please try again')
        except Exception as err:
            print(err)


def display_all_records():
    get_all_records_sql = 'select * from records'

    con = sqlite3.connect('records_db.sqlite')
    con.row_factory = sqlite3.Row
    rows = con.execute(get_all_records_sql)

    records = []

    for i in rows:
        record = Record(i['name'], i['country'], i['catches'])
        records.append(record)
        print(record.id)

    con.close()

    for i in records:
        print(i.name, i.country, i.catches, i.id)


def search_by_name():
    print('todo ask user for a name, and print the matching record if found. What should the program do if the name is not found?')


def add_new_record(record):
    '''
    Adds record to database, raises error if record already exists
    '''

    insert_sql = 'insert into records (name, country, catches) values (?, ?, ?)'

    try:
        with sqlite3.connect('records_db.sqlite') as con:
            res = con.execute(insert_sql, (record.name, record.country, record.catches))  
            new_id = res.lastrowid
            record.id = new_id
    except sqlite3.IntegrityError:
        raise RecordError(f'Error - record for: {record.name} already exists')
    finally:
        con.close()


def edit_existing_record():
    name = input('Who\'s record do you wish to change: ')

    update_record_sql = 'update records set name = ?, country = ?, catches = ? where rowid = ?'

    with sqlite3.connect('records_db.sqlite') as con:
        updated = con.execute(update_record_sql, ())


def delete_record(record):
    

    if not record.id:
        raise RecordError('Record does not have ID') 
    
    delete_sql = 'delete from records where rowid = ?'

    with sqlite3.connect('records_db.sqlite') as con:
        deleted = con.execute(delete_sql, (record.id))
        deleted_count = deleted.rowcount
    con.close()

    if deleted_count == 0:
        raise RecordError(f'Record with id {id} not found')


def get_record_info():
    name = input('What is the name of the record holder: ')
    country = input('What country are they from: ')
    catches = input('How many catches has this person done: ')
    return Record(name, country, catches)


if __name__ == '__main__':
    main()