import sqlite3


class DBHelper:

    def __init__(self, dbname="cryptobase.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        tbl_items = "CREATE TABLE IF NOT EXISTS items (cryptocurrency text, owner text)"
        tbl_rates = "CREATE TABLE IF NOT EXISTS rates (cryptocurrency text, value text)"
        itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (cryptocurrency ASC)" 
        ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
        cryptocurrencyidx = "CREATE INDEX IF NOT EXISTS cryptocurrencyIndex ON rates (cryptocurrency ASC)"
        valueidx = "CREATE INDEX IF NOT EXISTS valueIndex ON rates (value ASC)" 
        self.conn.execute(tbl_items)
        self.conn.execute(tbl_rates)
        self.conn.execute(itemidx)
        self.conn.execute(ownidx)
        self.conn.execute(cryptocurrencyidx)
        self.conn.execute(valueidx)
        self.conn.commit()

    def add_item(self, item_text, owner):
        stmt = "INSERT INTO items (cryptocurrency, owner) VALUES (?, ?)"
        args = (item_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text, owner):
        stmt = "DELETE FROM items WHERE cryptocurrency = (?) AND owner = (?)"
        args = (item_text, owner )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self, owner):
        stmt = "SELECT cryptocurrency FROM items WHERE owner = (?)"
        args = (owner, )
        return [x[0] for x in self.conn.execute(stmt, args)]

    def add_rates(self, cryptocurrency, value):
        stmt = "INSERT INTO rates (cryptocurrency, value) VALUES (?, ?)"
        args = (cryptocurrency, value)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_rates(self):
        stmt = "DELETE FROM rates"
        self.conn.execute(stmt)
        self.conn.commit()

    # def get_rates(self):
    #     stmt = "SELECT * FROM rates"
    #     return self.conn.execute(stmt)