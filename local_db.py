import sqlite3
from collections import Iterable
from uuid import UUID
from enum import Enum

import constants


class Locale(Enum):
    English = "EN"
    Russian = "RU"
    Spanish = "ES"


locale = Locale.Russian


class ObjectType(Enum):
    Operator = 0
    Domain = 1
    OrganizationUnit = 2
    Person = 3
    Territory = 4
    Component = 5
    Part = 6


class __Base:

    def __init__(self, database_path: str):
        self.path = database_path
        self.connection = sqlite3.connect(database_path, detect_types=sqlite3.PARSE_DECLTYPES)
        sqlite3.register_adapter(UUID, lambda x: x.bytes_le)
        sqlite3.register_converter('uniqueidentifier', lambda x: UUID(bytes_le=x))

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def close(self):
        self.connection.close()

    def execute_scalar(self, sql: str, parameters: Iterable = None):
        cursor = self.connection.cursor()
        if parameters:
            cursor.execute(sql, parameters)
        else:
            cursor.execute(sql)

        return cursor.fetchone()[0]


class Dictionary(__Base):
    FILE_NAME = "parsec3.dictionary.dat"

    HIERARCHY_META = [
        "t_id",
        "action",
        "parent_id",
        "obj_id",
        "is_deleted",
        "obj_type",
        "type_guid"
    ]

    def __init__(self):
        super().__init__(constants.parsec_directory + Dictionary.FILE_NAME)

    def get_object_name(self, id: UUID) -> str:
        sql = """
            SELECT
                [VAL]
            FROM [DICTIONARY]
            WHERE
                [OBJ_ID] = ?
        """

        return self.execute_scalar(sql, [id])

    def get_event_name(self, code: int) -> str:
        sql = """
            SELECT
                [TRANTYPE_DESC]
            FROM [TRANTYPES_DESC]
            WHERE
                [TRANTYPE_ID] = ?
                AND [LOCALE] = ?
        """

        return self.execute_scalar(sql, [code, locale.value])

    def get_parents(self, id: UUID) -> list:
        sql = """
            WITH RECURSIVE [with_parents]( objectID ) 
            AS 
            (
               VALUES( ? ) 
               UNION    
               SELECT 
                   [parent_id]
               FROM [HIERARCHY], [with_parents] 
               WHERE   
                   [HIERARCHY].[obj_id] = [with_parents].[objectID]
            )
            SELECT 
               [HIERARCHY].* 
            FROM [HIERARCHY] 
               INNER JOIN [with_parents] ON
            [with_parents].[objectID] = [HIERARCHY].[obj_id] 
            WHERE
                 [IS_DELETED] = 0
        """

        result = []
        for row in self.connection.execute(sql, [id]):
            result.append(dict((key, value) for key, value in zip(Dictionary.HIERARCHY_META, row)))

        return result

    def get_parsec_root_id(self, type: ObjectType):
        sql = """
            SELECT
                [OBJ_ID]
            FROM [HIERARCHY]
            WHERE
                [OBJ_TYPE] = {0}
            LIMIT 1                
        """.format(type.value)

        random_object_id = self.execute_scalar(sql)
        result = next((x for x in self.get_parents(random_object_id) if x["obj_id"] == x["parent_id"]), None)

        return result["obj_id"] if result else None

    def get_type_root_ids(self, type: ObjectType):
        sql = """
            SELECT
                [OBJ_ID]
            FROM [HIERARCHY]
            WHERE                
                [PARENT_ID] = ?
                AND [OBJ_ID] <> [PARENT_ID]
        """

        return list(map(lambda x: x[0], self.connection.execute(sql, [self.get_parsec_root_id(type)])))

    def get_root_territory_ids(self):
        return self.get_type_root_ids(ObjectType.Territory)

    def get_root_domain_ids(self):
        return self.get_type_root_ids(ObjectType.Domain)

    def get_root_organization_unit_ids(self):
        return self.get_type_root_ids(ObjectType.OrganizationUnit)

    def get_root_ids(self):
        return self.get_root_territory_ids() + self.get_root_domain_ids() + self.get_root_organization_unit_ids()
