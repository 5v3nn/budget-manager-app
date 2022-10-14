import sqlite3
import loghandler


class DataManagement:

    # db variables
    path_db = "./assets/data.db"
    category_table_name = "category"
    entry_table_name = "entry"

    PATH_LOGFILE = "./logs/data_management.log"

    def __init__(self):
        # create table
        con, cur = self.start_connection()
        try:
            self.create_table(cur)
        except Exception as sql_create_err:
            loghandler.write_log(
                self.PATH_LOGFILE,
                "SQL CREATE TABLE ERROR: " + str(sql_create_err),
                print_log=True,
            )
        self.end_connection(con)

        # add default categories
        self.add_category("General")

    def start_connection(self):
        con = sqlite3.connect(self.path_db)
        cur = con.cursor()
        return con, cur

    @staticmethod
    def end_connection(con):
        con.commit()
        con.close()

    def create_table(self, cur):
        cur.execute(
            "CREATE TABLE IF NOT EXISTS "
            + self.category_table_name
            + " ("
            + "category TEXT UNIQUE"
            + ")"
        )
        cur.execute(
            "CREATE TABLE IF NOT EXISTS "
            + self.entry_table_name
            + " ("
            + "category_id TEXT, "
            + "name TEXT, "
            + "value TEXT, "
            + "date TEXT)"
        )

    def drop_table(self):
        con, cur = self.start_connection()
        cur.execute("DROP TABLE IF EXISTS " + self.category_table_name)
        cur.execute("DROP TABLE IF EXISTS " + self.entry_table_name)
        self.end_connection(con)

    def get_available_dates(self) -> list:
        """
        Returns a list of all the month dates in the database.

        :return: list e.g.: ['yyyy-mm', 'yyyy-mm']
        """

        con, cur = self.start_connection()

        try:
            cur.execute(
                "SELECT SUBSTR(date, 1, 7) as d "
                + "FROM " + self.entry_table_name
                + " GROUP BY d"
                + " ORDER BY d ASC"
            )
            # [['2022-01',], ['2022-02',]]
            dates = [d[0] for d in cur.fetchall()]

        except Exception as sql_get_dates_err:
            loghandler.write_log(self.PATH_LOGFILE, 'SQL GET DATES ERROR: ' + str(sql_get_dates_err), print_log=True)
            dates = []

        self.end_connection(con)

        return dates

    def add_element(self, category, name, value, date):

        # connect
        con, cur = self.start_connection()

        try:
            # check if category already exists
            cur.execute(
                "SELECT c.rowid "
                "FROM " + self.category_table_name + " AS c "
                + 'WHERE c.category="' + str(category) + '"'
            )
            category_id = cur.fetchall()[0][0]
            cur.execute(
                "INSERT INTO " + self.entry_table_name + " AS e "
                + "VALUES ("
                + '"' + str(category_id) + '",'
                + '"' + str(name) + '",'
                + '"' + str(value) + '",'
                + '"' + str(date) + '"'
                + ");"
            )
        except Exception as add_err:
            loghandler.write_log(self.PATH_LOGFILE, 'SQL ADD ENTRY ERROR: ' + str(add_err), print_log=True)

        # commit
        self.end_connection(con)

    def get_entries_by_date(self, date_yyyymm):
        """
        Get entries by date

        :param date_yyyymm: date with format YYYY-MM
        :return: list with entries, [] on error
        """

        # calculate start year/month and end year/month
        try:
            start_y, start_m = [int(d) for d in date_yyyymm.split('-')]
            end_m = (start_m + 1) % 12
            end_y = start_y if start_m < end_m else (start_y + 1)

        except Exception as date_err:
            err_msg = f"GET ENTRY BY DATE FORMAT ERROR: {str(date_err)}"
            loghandler.write_log(self.PATH_LOGFILE, err_msg)
            print(err_msg)
            return []

        con, cur = self.start_connection()

        # "SELECT substr(e.date, 9), e.name, c.category, e.value, substr(e.ROWID, 0) "  # todo add the rowid for deletion process
        sql_statement = "SELECT substr(e.date, 9), e.name, c.category, e.value, e.ROWID " + "FROM category as c " + \
                        "JOIN entry as e " + \
                        "ON e.category_id = c.ROWID " + \
                        "WHERE julianday('" + str(start_y).zfill(4) + "-" + str(start_m).zfill(2) + "-01') " + \
                        "<= julianday(e.date) " + \
                        "AND julianday(e.date) < julianday('" + str(end_y).zfill(4) + "-" + str(end_m).zfill(2) + "-01') " + \
                        "ORDER BY e.date ASC"
        print(sql_statement)

        try:
            cur.execute(sql_statement)
            # [['category', 'item', '-100.00', '2022-01-01', 0], [...]]
            entries = cur.fetchall()

        except Exception as get_entry_by_date_err:
            loghandler.write_log(self.PATH_LOGFILE, 'SQL GET ENTRY BY DATE ERROR: ' + str(get_entry_by_date_err), print_log=True)
            entries = []

        self.end_connection(con)

        return entries

    def get_entries_by_category(self, category: str) -> list:

        con, cur = self.start_connection()

        sql_statement = f"SELECT substr(e.date, 9), e.name, c.category, e.value, e.ROWID " + "FROM category as c " + \
                        f"JOIN entry as e " + \
                        f"ON e.category_id = c.ROWID " + \
                        f"WHERE c.category = '{category}' " + \
                        f"ORDER BY e.date ASC"
        print(sql_statement)
        try:
            cur.execute(sql_statement)
            # [['category', 'item', '-100.00', '2022-01-01', 0], [...]]
            entries = cur.fetchall()

        except Exception as get_entry_by_cat_err:
            loghandler.write_log(self.PATH_LOGFILE, 'SQL GET ENTRY BY CATEGORY ERROR: ' + str(get_entry_by_cat_err), print_log=True)
            entries = []

        self.end_connection(con)

        return entries

    def delete_entry(self, entry_id: int):
        print('del at ', entry_id)

        con, cur = self.start_connection()

        try:
            cur.execute(
                "DELETE FROM " + self.entry_table_name
                + " WHERE rowid=" + str(entry_id)
            )

        except Exception as del_entry_err:
            loghandler.write_log(self.PATH_LOGFILE, 'SQL DELETE ENTRY ERROR: ' + str(del_entry_err),
                                 print_log=True)

        self.end_connection(con)

    def add_category(self, category):

        # do nothing if category is empty
        if not category:
            return

        # connect
        con, cur = self.start_connection()

        try:
            cur.execute(
                "INSERT OR IGNORE INTO " + self.category_table_name + " "
                + 'VALUES ("' + str(category) + '")'
            )
        except Exception as add_err:
            loghandler.write_log(self.PATH_LOGFILE, 'SQL CATEGORY ADD ERROR: %s' % str(add_err))

        # commit
        self.end_connection(con)

    def get_categories(self):
        con, cur = self.start_connection()

        try:
            cur.execute(
                "SELECT category "
                + "FROM " + self.category_table_name
                # + " GROUP BY category"
                # + " ORDER BY category ASC"
            )
            # [['cat',], ['cat2',]]
            categories = [c[0] for c in cur.fetchall()]

        except Exception as get_cat_err:
            loghandler.write_log(self.PATH_LOGFILE, 'SQL GET CATEGORY ERROR: ' + str(get_cat_err),
                                 print_log=True)
            categories = []

        self.end_connection(con)

        return categories

    def del_category(self, category: str):

        # do nothing if category is empty
        if not category:
            return

        # get entries by category
        entries_with_category = self.get_entries_by_category(category)

        # connect
        con, cur = self.start_connection()

        try:

            # overwrite existing entries with category to delete with new category_id -1
            for e in entries_with_category:
                e_id = e[-1]

                # cur.execute(f"UPDATE {self.entry_table_name} SET category_id = -1 WHERE ROWID = {e_id}")
                cur.execute(f"DELETE FROM {self.entry_table_name} WHERE ROWID = {e_id}")

            # delete category
            cur.execute(f"DELETE FROM {self.category_table_name} WHERE category = '{category}'")

        except Exception as del_err:
            loghandler.write_log(self.PATH_LOGFILE, 'SQL CATEGORY DELETE ERROR: %s' % str(del_err))

        # commit
        self.end_connection(con)
