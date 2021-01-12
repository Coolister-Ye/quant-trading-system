import pymysql.cursors
from utils.FileUtils import FileUtils


class DbUtils(FileUtils):

    def __init__(self):
        super().__init__()
        self.db_config = self.load_yaml('db_config.yaml')
        self.db_conn = pymysql.connect(**self.db_config['mysql'], cursorclass=pymysql.cursors.DictCursor)

    @staticmethod
    def joinValues(inList):
        re = list()
        for i in inList:
            if type(i) == str:
                re.append("'{}'".format(i))
            else:
                re.append(str(i))
        return ",".join(re)

    def push(self, tableName, colNames, values, update_date):
        try:
            with self.db_conn.cursor() as cursor:
                for v in values:
                    colNamesSql = ",".join(["`{}`".format(c) for c in colNames])
                    valuesSql = DbUtils.joinValues(v)
                    if update_date != "":
                        colNamesSql += ",`{}`".format('update_date')
                        valuesSql += ",'{}'".format(update_date)
                    sql = self.db_config['sql']['insert_template'].format(tableName, colNamesSql, valuesSql)
                    cursor.execute(sql)
            self.db_conn.commit()
        except:
            print("- Cannot load data to mysql: " + sql)

    def get(self, tableName, colNames="*", whereCondition="", limit=""):
        try:
            with self.db_conn.cursor() as cursor:
                colNamesSql = ",".join(["`{}`".format(c) for c in colNames]) if colNames != "*" else colNames
                sql = self.db_config['sql']['select_template'].format(colNamesSql, tableName)
                sql += " WHERE " + whereCondition
                sql += " LIMIT " + limit if limit != "" else limit
                cursor.execute(sql)
            data = cursor.fetchall()
            print("+ Load data from mysql: " + sql)
            return list(data)
        except:
            print("- Cannot get data from mysql: " + sql)


if __name__ == '__main__':
    dbu = DbUtils()
    dbu.push("users", ["email", "password"], ["text1", "text2"])
    print(dbu.get("users"))
