import streamlit as st
import sqlite3
import datetime
import requests

st.set_page_config(
    page_title="NITKKR'24 Intern analysis",
    page_icon="👋",
)

st.markdown("# Welcome")
st.markdown(
    "* #### If you just want to read conclusions, go to end of the files. Analytics are a bit detailed, but I bet they are interesting."
)


st.markdown(
    "###### For any quaries or contributions, feel free to contact me anytime through anonymous message on my [Portfolio](portfolio-shubhampatel.vercel.app/) or [Linkedin](https://www.linkedin.com/in/shubham-patel01/)"
)


def update_visitor_count(conn, ip_address):
    c = conn.cursor()
    c.execute(
        "INSERT INTO visitors (timestamp, ip_address, is_unique) VALUES (?, ?, 1)",
        (datetime.datetime.now(), ip_address),
    )
    c.execute("UPDATE visitor_count SET count = count + 1")
    conn.commit()


def get_visitor_count(conn):
    c = conn.cursor()
    c.execute("SELECT count FROM visitor_count")
    return c.fetchone()[0]


def main():
    # Get visitor IP address
    visitor_ip = requests.get("https://api.ipify.org?format=json").json()["ip"]

    # Connect to SQLite database and create tables if they don't exist
    conn = sqlite3.connect("visitor_count.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS visitor_count (count INTEGER)")
    c.execute(
        """CREATE TABLE IF NOT EXISTS visitors (timestamp TEXT, ip_address TEXT, is_unique INTEGER);"""
    )

    c.execute("INSERT OR IGNORE INTO visitor_count (count) VALUES (0)")
    conn.commit()

    # Update visitor count and add visitor data
    update_visitor_count(conn, visitor_ip)
    count = get_visitor_count(conn)

    # Write visitor count to the Streamlit app
    st.write("Number of visitors: ", count)


if __name__ == "__main__":
    main()
