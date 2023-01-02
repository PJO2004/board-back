from sqlalchemy.orm import Session
from typing import Dict, Any


def conditioncreater(conditions: Dict[str, Any], table) -> list:
    condition_list: list = list()
    for key, value in conditions.items():
        key: list = key.split("__")
        col = getattr(table, key[0])
        if len(key) == 1:
            condition_list.append((col == value))
        elif len(key) == 2 and key[1] == "gt":
            condition_list.append((col > value))
        elif len(key) == 2 and key[1] == "gte":
            condition_list.append((col >= value))
        elif len(key) == 2 and key[1] == "lt":
            condition_list.append((col < value))
        elif len(key) == 2 and key[1] == "lte":
            condition_list.append((col <= value))
        elif len(key) == 2 and key[1] == "in":
            condition_list.append((col.in_(value)))
        elif len(key) == 2 and key[1] == "ne":
            condition_list.append((col != value))
        elif len(key) == 2 and key[1] == "like":
            condition_list.append((col.like(f"%{value}%")))

    return condition_list


def insert_db(insert_item, db: Session):
    db.add(insert_item)
    db.commit()
    db.refresh(insert_item)


def insert_db_many(insert_item: list, db: Session):
    db.add_all(insert_item)
    db.commit()


def get_only_value(list_tuple):
    if list_tuple:
        return map(lambda one: one[0], list_tuple)
    return None
