import sqlite3

DATABASE_NAME = 'desks_database.db'


class Handler:
    def __init__(self):
        db = DATABASE_NAME
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

    def return_desk_names(self):
        desks = self.cur.execute(f'''SELECT title FROM desks''').fetchall()
        return list(map(lambda x: ''.join(x), desks))

    def return_desk_id(self, desk_name):
        desk_id = self.cur.execute(f'''SELECT id from desks WHERE title='{desk_name}' ''').fetchall()
        return desk_id[0][0]

    def return_card_id(self, card_name):
        card_id = self.cur.execute(f'''SELECT id from cards WHERE title='{card_name}' ''').fetchall()
        return card_id

    def return_note_id(self, note_content):
        note_id = self.cur.execute(
            f'''SELECT id from notes WHERE content='{note_content}' ''').fetchall()
        return note_id[-1][0]

    def create_desk(self, desk_name):
        self.cur.execute(f'''INSERT INTO desks(title) VALUES('{desk_name}')''')
        self.con.commit()

    def create_card(self, card_name, desk_id):
        self.cur.execute(f'''INSERT INTO cards(title, deskid) VALUES('{card_name}', '{desk_id}') ''')
        self.con.commit()

    def create_note(self, note_content, card_id):
        self.cur.execute(
            f'''INSERT INTO notes(content, cardid) VALUES('{note_content}', '{card_id}') ''')
        self.con.commit()

    def update_desk(self, desk_id, new_desk_name):
        self.cur.execute(f'''UPDATE desks SET title='{new_desk_name}' WHERE id={desk_id} ''')
        self.con.commit()

    def update_card(self, card_id, new_card_name):
        self.cur.execute(f'''UPDATE cards SET title='{new_card_name}' WHERE id={card_id} ''')
        self.con.commit()

    def update_note(self, new_note_content, content_id):
        self.cur.execute(f'''UPDATE notes SET content='{new_note_content}' WHERE id={content_id} ''')
        self.con.commit()

    def delete_desk(self, desk_id):
        cards = self.cur.execute(f'''SELECT id FROM cards WHERE deskid={desk_id}''').fetchall()
        for i in cards:
            self.delete_card(i[0])
        self.cur.execute(f'''DELETE FROM desks WHERE id={desk_id}''')
        self.con.commit()

    def delete_card(self, card_id):
        self.cur.execute(f'''DELETE FROM notes WHERE cardid={card_id}''')
        self.con.commit()
        self.cur.execute(f'''DELETE FROM cards WHERE id={card_id}''')
        self.con.commit()

    def delete_note(self, note_id):
        self.cur.execute(f'''DELETE FROM notes WHERE id={note_id} ''')
        self.con.commit()

    def load_desks(self):
        desks = self.cur.execute(f'''SELECT id, title FROM desks''').fetchall()
        return desks

    def load_cards(self, desk_id):
        cards = self.cur.execute(
            f'''SELECT id, title FROM cards WHERE deskid={desk_id}''').fetchall()
        return cards

    def load_notes(self, card_id):
        notes = self.cur.execute(
            f'''SELECT id, content FROM notes WHERE cardid={card_id}''').fetchall()
        return notes
# TODO: Добавить в таблицу столбец с позицией виджета в списке