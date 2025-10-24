# -----------------------------------------------------------------------------
# File: saving.py
# ACS School Project - Simple Maze Example
# Organization: THUAS (The Hague University of Applied Sciences)
# Location: Delft
# Date: July 2025
# -----------------------------------------------------------------------------
import sys
import pathlib
from pathlib import Path
import ast
import sqlite3

conn = sqlite3.Connection('SavesDB.db')
cursor = conn.cursor()
cursor.execute('''Create table if not exists "Rooms" (
	"Id"	INTEGER,
	"classroom2015"	INTEGER NOT NULL DEFAULT 0,
	"teachersroom1"	INTEGER NOT NULL DEFAULT 0,
	"lab2001"	INTEGER NOT NULL DEFAULT 0,
	"projectroom1"	INTEGER NOT NULL DEFAULT 0,
	"projectroom3"	INTEGER NOT NULL DEFAULT 0,
	"frontdesk"	INTEGER NOT NULL DEFAULT 0,
	"equinox"	INTEGER NOT NULL DEFAULT 0,
	"correctionroom" INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("Id" AUTOINCREMENT)
)
                    ''')
cursor.execute('''create table if not exists "Items" (
	"ID"	INTEGER,
	"Name"	TEXT,
	PRIMARY KEY("ID")
)''')

cursor.execute('''create table if not exists "State" (
	"Id"	INTEGER,
	"SaveName"	TEXT NOT NULL UNIQUE,
	"Current"	TEXT NOT NULL,
	"Previos"	TEXT,
	"VisitedId"	INTEGER NOT NULL,
	"Coins"	INTEGER,
	"FrontdeskFailures"	INTEGER,
	"Time" real,
	PRIMARY KEY("Id" AUTOINCREMENT),
	FOREIGN KEY("VisitedId") REFERENCES "Rooms"("Id")
)''')

cursor.execute('''create table if not exists "Inventory" (
	"StateID"	INTEGER NOT NULL,
	"ItemID"	INTEGER NOT NULL,
	FOREIGN KEY("ItemID") REFERENCES "Items"("ID"),
	FOREIGN KEY("StateID") REFERENCES "State"("Id")
)''')

#existing items to be added into the items table
cursor.execute("INSERT OR IGNORE INTO Items (ID, Name) VALUES (?, ?)", (1, 'Access Pass'))
cursor.execute("INSERT OR IGNORE INTO Items (ID, Name) VALUES (?, ?)", (2, 'key'))
cursor.execute("INSERT OR IGNORE INTO Items (ID, Name) VALUES (?, ?)", (3, 'calculator'))
cursor.execute("INSERT OR IGNORE INTO Items (ID, Name) VALUES (?, ?)", (4, 'Good Classmate Badge'))


conn.commit()
conn.close()

def save(state,name):
    conn = sqlite3.Connection('SavesDB.db')
    cursor = conn.cursor()
    # cursor.execute('''Insert into Items
    #                     values(1,'Access Pass'),
    #                             (2,'key')''')
    rooms = state["visited"]
    for room in rooms:
        if(rooms[room]): rooms[room] = 1
        else: rooms[room] = 0
    cursor.execute('''
        INSERT INTO Rooms (
            classroom2015,
            teachersroom1,
            lab2001,
            projectroom1,
            projectroom3,
            frontdesk,
            equinox,
            correctionroom
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        rooms["classroom2015"],
        rooms["teachersroom1"],
        rooms["lab2001"],
        rooms["projectroom1"],
        rooms["projectroom3"],
        rooms["frontdesk"],
        rooms["equinox"],
        rooms["correctionroom"]
    ))
    RoomsID = cursor.lastrowid
    cursor.execute('''
        INSERT INTO State (
            SaveName,
            Current,
            Previos,
            VisitedId,
            Coins,
            FrontdeskFailures,
            Time
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        name,
        state["current_room"],
        state["previous_room"],
        RoomsID,
        state["coins"],
        state["frontdesk_failures"],
        state["start_time"]
    ))

    StateID = cursor.lastrowid
    inve = state["inventory"]

    cursor.execute("SELECT ID, Name FROM Items")
    rows = cursor.fetchall()

    for item in inve:
            # Get item_id

            cursor.execute("SELECT ID FROM Items WHERE Name = ?", (f"{item}",))
            item_row = cursor.fetchone()

            if item_row:
                item_id = item_row[0]
                # Insert relationship into inventory table
                cursor.execute("""
                    INSERT OR IGNORE INTO Inventory (StateID, ItemId)
                    VALUES (?, ?)
                """, (StateID,item_id))
            else:
                print(f"⚠️ Item '{item}' not found in item table")

    print(f"State has been saved as {name} ")

    conn.commit()
    conn.close()

# def save(state):
#     p = Path(r"saves.txt")
#     with p.open("w") as file:
#         file.write(f"{state}")
#     print("Saved")

# def load(state):
#     p = Path(r"saves.txt")
#     pro = {}
#     with p.open("r") as file:
#         for item in file:
#             pro = ast.literal_eval(item)
#         print("Loading...")
#         return pro

def load(state,save_name):

    print(f"Loading {save_name}...")
    conn = sqlite3.Connection('SavesDB.db')
    cursor = conn.cursor()

    cursor.execute("""
           SELECT Id, Current, Previos, Coins, FrontdeskFailures, Time
           FROM State
           WHERE SaveName = ?
       """, (save_name,))
    state_row = cursor.fetchone()

    if not state_row:
        raise ValueError(f"No state found with SaveName='{save_name}'")

    state_id, current_room, previous_room, coins, frontdesk_failures, start_time = state_row


    cursor.execute("SELECT * FROM Rooms WHERE Id = ?", (state_id,))
    rooms_row = cursor.fetchone()
    if rooms_row:
        room_columns = [col[0] for col in cursor.description][1:]  # skip 'Id'
        room_values = rooms_row[1:]
        visited = {room: bool(value) for room, value in zip(room_columns, room_values)}
    else:
        visited = {}


    cursor.execute("""
           SELECT i.Name
           FROM Inventory inv
           JOIN Items i ON inv.ItemID = i.ID
           WHERE inv.StateID = ?
       """, (state_id,))
    inventory_items = [row[0] for row in cursor.fetchall()]


    game_state = {
        "current_room": current_room,
        "previous_room": previous_room,
        "visited": visited,
        "inventory": inventory_items,
        "coins": coins,
        "frontdesk_failures": frontdesk_failures,
        "start_time":start_time
    }


    conn.close()
    return game_state






