#-------------------------------------------------------------------------
# AUTHOR: Tim Hsieh
# FILENAME: db_connection_mongo.py
# SPECIFICATION: Creating an inverted index 
# FOR: CS 4250- Assignment #2
# TIME SPENT: 7 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
import pymango

def connectDataBase():

    # Create a database connection object using pymongo
    client = pymango.MongoClient("mongodb://localhost:27017/")
    database = client["Assignment2"]
    collection = database["Documents"]
    return collection

def createDocument(col, docId, docText, docTitle, docDate, docCat):

    # create a dictionary to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.
    terms = docText.lower().split()
    term_count = {}
    for term in terms:
        if term in term_count:
            term_count[term] += 1
        else:
            term_count[term] = 1

    # create a list of dictionaries to include term objects.
    term_objects = [{"term": term, "count": count} for term, count in term_count.items()]

    #Producing a final document as a dictionary including all the required document fields
    document = {
        "_id": docId,
        "text": docText,
        "title": docTitle,
        "date": docDate,
        "category": docCat,
        "terms": term_objects
    }

    # Insert the document
    col.insert_one(document)

def deleteDocument(col, docId):

    # Delete the document from the database
    col.delete_one({"_id": docId})

def updateDocument(col, docId, docText, docTitle, docDate, docCat):

    # Delete the document
    col.delete_one({"_id": docId})

    # Create a new document with the same id
    createDocument(col, docId, docText, docTitle, docDate, docCat)

def getIndex(col):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    inverted_index = {}
    documents = col.find()
    
    for document in documents:
        for term_obj in document["terms"]:
            term = term_obj["term"]
            count = term_obj["count"]
            if term in inverted_index:
                inverted_index[term].append(f"{document['title']}:{count}")
            else:
                inverted_index[term] = [f"{document['title']}:{count}"]
    
    return inverted_index