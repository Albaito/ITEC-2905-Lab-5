import sqlite3

con = sqlite3.connect('records_db.sqlite')
con.row_factory = sqlite3.Row
con.execute('create table if not exists records (name text, country text, catches integer, UNIQUE(name COLLATE NOCASE))')
con.commit()
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

# TODO create database table OR set up Peewee model to create table

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

    with sqlite3.connect('records_db.sqlite') as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        rows = cursor.execute(get_all_records_sql)

        

        records = []

        for i in rows:
            record = Record(i['name'], i['country'], i['catches'])
            new_id = cursor.lastrowid
            record.id = new_id
            records.append(record)
            

    con.close()

    for i in records:
        print(i.name, i.country, i.catches, i.id)


def search_by_name():
    name = str(input('Who\'s record do you wish to view: \n'))
    
    get_record_by_name_sql = 'select * from records where upper(name) = upper(?)'

    with sqlite3.connect('records_db.sqlite') as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        rows = cursor.execute(get_record_by_name_sql, (name, ))

        
        for i in rows:
            print(i['name'], i['country'], i['catches'])
        
        
    con.close()


def add_new_record(record):
    '''
    Adds record to database, raises error if record already exists
    '''

    insert_sql = 'insert into records (name, country, catches) values (?, ?, ?)'

    try:
        with sqlite3.connect('records_db.sqlite') as con:
            cursor = con.cursor()
            cursor.execute(insert_sql, (record.name, record.country, record.catches))
            new_id = cursor.lastrowid

            print('new id', new_id)
            record.id = new_id
    except sqlite3.IntegrityError:
        raise RecordError(f'Error - record for: {record.name} already exists')
    finally:
        con.close()


def edit_existing_record():
    chosen_id = input('Enter the id for the row you wish to modify: ')

    new_record = get_record_info()

    update_record_sql = 'update records set name = ?, country = ?, catches = ? where rowid = ?'

    with sqlite3.connect('records_db.sqlite') as con:
        updated = con.execute(update_record_sql, (new_record.name, new_record.country, new_record.catches , chosen_id))


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