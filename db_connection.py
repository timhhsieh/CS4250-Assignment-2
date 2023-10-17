#-------------------------------------------------------------------------
# AUTHOR: Tim Hsieh
# FILENAME: db_connection.py
# SPECIFICATION: Creating an inverted index 
# FOR: CS 4250- Assignment #2
# TIME SPENT: 5 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
import psycopg2

# Database connection parameters
db_params = {
    "dbname": "Assignment 2",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": "5432"
}

def connectDataBase():

    # Create a database connection object using psycopg2
    try:
        # Create a database connection
        conn = psycopg2.connect(**db_params)
        return conn
    except Exception as e:
        print("Error: Unable to connect to the database.")
        print(e)
        return None

def createCategory(cur, catId, catName):

    # Insert a category in the database
    try:
        # Insert a category into the database
        cur.execute("INSERT INTO public.\"Categories\" (category_id, category_name) VALUES (%s, %s);", (catId, catName))
    except Exception as e:
        print("Error: Unable to create a category.")
        print(e)

def createDocument(cur, docId, docText, docTitle, docDate, docCat):
    
    try:
        # 1. Get the category id based on the informed category name
        cur.execute("SELECT category_id FROM public.\"Categories\" WHERE category_name = %s;", (docCat,))
        catId = cur.fetchone()[0]

        # 2. Insert the document into the database
        cur.execute("INSERT INTO public.\"Documents\" (doc_id, num_chars, text, title, doc_date, category_id) VALUES (%s, %s, %s, %s, %s, %s);", (docId, len(docText), docText, docTitle, docDate, catId))

        # 3. Update the potential new terms
        terms = set([term.strip('.,!?').lower() for term in docText.split()])
        for term in terms:
            cur.execute("INSERT INTO public.\"Terms\" (term_text) VALUES (%s) ON CONFLICT (term_text) DO NOTHING;", (term,))

        # 4. Update the index
        term_counts = {}
        for term in terms:
            term_counts[term] = term_counts.get(term, 0) + 1
        for term, count in term_counts.items():
            cur.execute("INSERT INTO public.\"Document Terms\" (doc_id, term_id, count) VALUES (%s, (SELECT term_id FROM public.\"Terms\" WHERE term_text = %s), %s);", (docId, term, count))

    except Exception as e:
        print("Error: Unable to create a document.")
        print(e)

def deleteDocument(cur, docId):
    try:
        # 1. Query the index based on the document to identify terms
        cur.execute("SELECT term_id, count FROM public.\"Document Terms\" WHERE doc_id = %s;", (docId,))
        term_counts = cur.fetchall()
        for term_id, count in term_counts:
            cur.execute("UPDATE public.\"Document Terms\" SET count = count - %s WHERE term_id = %s;", (count, term_id))
            cur.execute("DELETE FROM public.\"Document Terms\" WHERE doc_id = %s;", (docId,))
            cur.execute("SELECT doc_id FROM public.\"Document Terms\" WHERE term_id = %s;", (term_id,))
            if not cur.fetchone():
                cur.execute("DELETE FROM public.\"Terms\" WHERE term_id = %s;", (term_id,))

        # 2. Delete the document from the database
        cur.execute("DELETE FROM public.\"Documents\" WHERE doc_id = %s;", (docId,))

    except Exception as e:
        print("Error: Unable to delete a document.")
        print(e)

def updateDocument(cur, docId, docText, docTitle, docDate, docCat):

    # 1 Delete the document
    deleteDocument(cur, docId)

    # 2 Create the document with the same id
    createDocument(cur, docId, docText, docTitle, docDate, docCat)

def getIndex(cur):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    cur.execute("""
    SELECT T.term, STRING_AGG(CAST(DT.doc_id AS VARCHAR), ':') AS documents
    FROM Terms AS T
    LEFT JOIN Document_Terms AS DT ON T.term_id = DT.term_id
    GROUP BY T.term
    ORDER BY T.term;
    """)
    index = {record[0]: record[1] for record in cur.fetchall()}

    return index