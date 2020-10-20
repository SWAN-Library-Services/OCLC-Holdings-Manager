import sqlite3

class OhmDatabase:

    def __init__(self, database_file):
        self.conn = sqlite3.connect(database_file)
        self.c = self.conn.cursor()

    def list_tables(self):
        self.c.execute('SELECT name FROM sqlite_master WHERE type="table";')
        tables = [table_name[0] for table_name in self.c.fetchall()]
        tables.sort(reverse = True)
        return tables

    def compare_tables(self, left_table, right_table):
        # shows data that exists in left_table, but does not exist in right
        self.c.execute(f"select oclcNum,library from '{left_table}' EXCEPT SELECT oclcNum,library from '{right_table}';")
        return self.c.fetchall()

    def commit_changes(self):
        self.conn.commit()
        return

    def close(self):
        self.conn.close()
        return

    def commit_and_close(self):
        self.commit_changes()
        self.close()
        return

    # create table if it doesn't exist
    def create_table(self, table_name):
        if table_name not in self.list_tables():
            self.c.execute(f'CREATE TABLE "{table_name}" ("catKey" TEXT, "oclcNum" TEXT, "library" TEXT)')
        return

    def insert_record(self, table_name, ils_catalog_key, oclc_number, oclc_symbol):
        self.c.execute(f'INSERT INTO "{table_name}" VALUES ("{ils_catalog_key}", "{oclc_number}", "{oclc_symbol}")')
        return