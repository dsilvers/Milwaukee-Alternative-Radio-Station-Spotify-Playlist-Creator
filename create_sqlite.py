import sqlite3

# because using the same thing for the name for the file, table, and column is cool
con = sqlite3.connect("tracks.db")
con.execute("create table tracks (id integer primary key, tracks varchar unique)")
