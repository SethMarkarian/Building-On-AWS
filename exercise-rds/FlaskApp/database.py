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
"Database layer"
import mysql.connector
import config

def list_photos():
    "Select all the photos from the database"
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""SELECT object_key, labels, created_datetime FROM photo
                      WHERE cognito_username is null""")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def add_photo(object_key, labels):
    "Add a photo to the database"
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO photo (object_key, labels) VALUES (%s, %s);", (object_key, labels))
    conn.commit()
    cursor.close()
    conn.close()

def get_database_connection():
    "Build a database connection"
    conn = mysql.connector.connect(user=config.DATABASE_USER, password=config.DATABASE_PASSWORD,
                                   host=config.DATABASE_HOST,
                                   database=config.DATABASE_DB_NAME,
                                   use_pure=True) # see https://bugs.mysql.com/90585
    return conn
