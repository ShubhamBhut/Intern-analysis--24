import streamlit as st
import sqlite3


def update_visitor_count(conn):
    c = conn.cursor()
    c.execute("UPDATE visitor_count SET count = count + 1")
    conn.commit()


def get_visitor_count(conn):
    c = conn.cursor()
    c.execute("SELECT count FROM visitor_count")
    return c.fetchone()[0]


def main():
    conn = sqlite3.connect("visitor_count.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS visitor_count (count INTEGER)")
    c.execute("INSERT OR IGNORE INTO visitor_count (count) VALUES (0)")
    conn.commit()
    update_visitor_count(conn)
    count = get_visitor_count(conn)
    st.write("Number of visitors: ", count)


if __name__ == "__main__":
    main()
