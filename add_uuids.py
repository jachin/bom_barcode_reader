#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import uuid

con = lite.connect('bom.db')
with con:
    cur = con.cursor()

    cur.execute( "SELECT id FROM upc WHERE uuid IS NULL")
    for row in cur.fetchall():
        id = row[0]

        cur.execute( "UPDATE upc SET uuid = ? WHERE id = ?", (str(uuid.uuid4()), id) )

        #con.commit()
        print(row)

con.close()
