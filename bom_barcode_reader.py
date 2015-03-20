#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import sqlite3 as lite

import httplib
import socket
import uuid

con = lite.connect('bom.db')

with con:
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS upc(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            `upc` TEXT,
            `location` TEXT,
            `uuid` TEXT,
            `timestamp` timestamp DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

con.commit()
con.close()

while True:
    barcode = raw_input("scann bar code: ")

    if barcode == '':
        continue

    print(datetime.now())
    print(barcode)

    con = lite.connect('bom.db')
    with con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO upc (upc, location, uuid) VALUES( ?, ?, ? )",
            ( barcode, socket.gethostname(), str(uuid.uuid4()) )
        )

    con.commit()
    con.close()

    # Small time out for repeated scans.
    try:
        conn = httplib.HTTPConnection("beverages.cw", timeout=1)
        conn.request("GET", "/ping/?upc={0}".format(barcode))
        response = conn.getresponse()
        conn.close()
        print("Ping status {0}".format(response.status))
    except (httplib.HTTPException, socket.error):
        print("Unable to ping, no big deal.")
