from peewee import SqliteDatabase
from model import Posts
from playhouse.shortcuts import model_to_dict


def is_same_sqlite_file(db1_path, db2_path, model, ignore_columns: list[str]=[]) -> bool:
    """2つのSQLiteファイルの特定のテーブルの内容が同じかどうかを確認する。

    Args:
        db1_path: 比較対象の1つ目のSQLiteファイルのパス。
        db2_path: 比較対象の2つ目のSQLiteファイルのパス。
        model: 比較対象のテーブルに対応するPeeweeのモデルクラス。
        ignore_columns: 比較時に無視するカラム名のリスト。デフォルトは空のリスト。

    Returns:
        bool: 2つのSQLiteファイルの特定のテーブルの内容が同じ場合はTrue、そうでない場合はFalse。
    """
    
    db1 = SqliteDatabase(db1_path)
    db2 = SqliteDatabase(db2_path)

    
    # モデルのメタデータを更新
    model._meta.database = db1
    column_set = set(model._meta.sorted_field_names)    
    for column in ignore_columns:
        column_set.remove(column)
        
        
    model._meta.database = db1
    dat1 = [model_to_dict(a) for a in model.select().order_by(model._meta.primary_key)]
    
    model._meta.database = db2
    dat2 = [model_to_dict(a) for a in model.select().order_by(model._meta.primary_key)]
    
    if len(dat1) !=  len(dat2):
        return False
    
    for d1, d2 in zip(dat1, dat2):
        for column in column_set:
            if d1[column] != d2[column]:
                return False
    return True




if __name__ == "__main__":
    print(is_same_sqlite_file("./sample1.sqlite3", "./sample2.sqlite3", Posts, []))
