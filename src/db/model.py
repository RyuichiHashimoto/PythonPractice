from peewee import MySQLDatabase, Model, IntegerField, PrimaryKeyField, TextField, DateTimeField, SqliteDatabase
from playhouse.shortcuts import model_to_dict
from datetime import datetime

DB = MySQLDatabase(
    database = 'sample-db', user = 'hashimoto', password = 'hashimoto', host = 'mysql', port =3306
)
pragmas = {'journal_mode': 'wal','cache_size': -1024 * 64}

class Posts(Model):
    id = PrimaryKeyField()
    user_id = IntegerField()
    title = TextField()
    body = TextField()
    created_at = DateTimeField()

    
    @classmethod
    def set_database(cls, db):
        cls._meta.database = db

# サンプルデータを生成してSQLiteファイルに書き込む関数
def write_sample_data_to_sqlite(db_file):
    # データベースの接続
    db = SqliteDatabase(db_file)
    Posts.set_database(db)

    # テーブルの作成
    db.create_tables([Posts])

    # サンプルデータの生成
    sample_data = [
        {'user_id': 1, 'title': 'First Post', 'body': 'This is the first post.', 'created_at': datetime(2023, 1, 1, 10, 0, 0)},
        {'user_id': 2, 'title': 'Second Post', 'body': 'This is the second post.', 'created_at': datetime(2023, 1, 2, 11, 0, 0)},
        {'user_id': 1, 'title': 'Third Post', 'body': 'This is the third post.', 'created_at': datetime(2023, 1, 3, 12, 0, 0)},
        {'user_id': 3, 'title': 'Fourth Post', 'body': 'This is the fourth post.', 'created_at': datetime(2023, 1, 4, 13, 0, 0)},
        {'user_id': 2, 'title': 'Fifth Post', 'body': 'This is the fifth post.', 'created_at': datetime(2023, 1, 5, 14, 0, 0)},
    ]

    # サンプルデータをデータベースに書き込む
    with db.atomic():
        for data in sample_data:
            Posts.create(**data)

    print("Sample data has been written to the SQLite file.")


if __name__ == "__main__":
    
    # date = [model_to_dict(query) for query in posts.select()]
    
    # sqlite_db = SqliteDatabase('./sample.sqlie3', pragmas=pragmas)

    write_sample_data_to_sqlite("./sample1.sqlite3")
    write_sample_data_to_sqlite("./sample2.sqlite3")

    



    # portst