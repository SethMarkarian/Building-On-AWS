# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except
# in compliance with the License. A copy of the License is located at
#
# https://aws.amazon.com/apache-2-0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
""" Script to create DDL"""
import mysql.connector

def populate():
    """ create DDL for tables and users """
    print("This script will drop and recreate the photo table, and the web_user user.")
    print("")

    photo_sql_1 = "DROP TABLE IF EXISTS photo;"
    photo_sql_2 = """
    create table photo (
    object_key nvarchar(80) not null primary key,
    labels nvarchar(200),
    description nvarchar(200),
    cognito_username nvarchar(150),
    created_datetime DATETIME DEFAULT now()
    );
    """

    user_sql_1 = "DROP USER 'web_user';"
    user_sql_2 = "CREATE USER 'web_user' IDENTIFIED BY %s;"
    user_sql_3 = "GRANT SELECT, INSERT, UPDATE, DELETE on photo to 'web_user';"

    #rds settings
    rds_host = input("Database host> ")
    db_user = input("Database user> ")
    password = input("Database password> ")
    db_name = input("Database name> ")
    app_password = input("web_user password> ")

    conn = mysql.connector.connect(user=db_user, password=password,
                                   host=rds_host,
                                   database=db_name)
    cursor = conn.cursor()
    print("Dropping / creating photo table")
    cursor.execute(photo_sql_1)
    conn.commit()
    cursor.execute(photo_sql_2)
    conn.commit()

    # this would be nicer in mysql 5.7, i.e "IF EXISTS"
    # https://dev.mysql.com/doc/refman/5.7/en/drop-user.html
    cursor.execute("SELECT 1 FROM mysql.user WHERE user = 'web_user'")
    result = cursor.fetchone()
    if result:
        print("Dropping web_user")
        cursor.execute(user_sql_1)
        conn.commit()

    print("Creating the web_user")
    cursor.execute(user_sql_2, (app_password,))
    conn.commit()
    print("Granting access to web_user")
    cursor.execute(user_sql_3)
    conn.commit()

    conn.close()


populate()
