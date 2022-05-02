# Postgres SQL

import psycopg2

def create_tables():
    con=psycopg2.connect("dbname='database' user='postgres' password='pos' host='localhost' port='5432'")
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS store (item TEXT, quantity INTEGER, price REAL)")
    con.commit()
    con.close()
    
# Inserting Data to avoid SQL injection
def insert(item,quantity,price):
    con=psycopg2.connect("dbname='database' user='postgres' password='pos' host='localhost' port='5432'")
    cur=con.cursor()
    cur.execute("INSERT INTO store VALUES(%s,%s,%s)", (item,quantity,price))
    con.commit()
    con.close()
    
# Viewing all data
def view():
    con=psycopg2.connect("dbname='database' user='postgres' password='pos' host='localhost' port='5432'")
    cur=con.cursor()
    cur.execute("SELECT * FROM store")
    rows=cur.fetchall()
    con.close()
    return rows

# delete a rows
def delete(item):
    con=psycopg2.connect("dbname='database' user='postgres' password='pos' host='localhost' port='5432'")
    cur=con.cursor()
    cur.execute("DELETE FROM store WHERE item=%s",(item,))
    con.commit()
    con.close()
    
# Updating data
def update(quantity,price,item):
    con=psycopg2.connect("dbname='database' user='postgres' password='pos' host='localhost' port='5432'")
    cur=con.cursor()
    cur.execute("UPDATE store SET quantity=%s, price=%s WHERE item=%s",(quantity,price,item))
    con.commit()
    con.close()

def main():
    #create_tables()
    #insert("Orange",10,15)
    #delete("Orange") # deleting rows where item = Orange
    update(20,15.0,'Apple')
    print(view())

if __name__ == '__main__':
    main()
