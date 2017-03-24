#!/usr/bin/env python
import jcc
from lucene import \
    QueryParser, IndexSearcher, StandardAnalyzer, SimpleFSDirectory, File, \
    VERSION, initVM, Version, getVMEnv


"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""
def run(searcher, analyzer,command):
    # print "Searching for:", command
    query = QueryParser(Version.LUCENE_CURRENT, "contents",
                        analyzer).parse(command)
    scoreDocs = searcher.search(query, 10).scoreDocs
    # print "%s total matching documents." % len(scoreDocs)
    rankedfiles = []
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        # print 'path:', doc.get("path"), 'name:', doc.get("name")
        rankedfiles.append(int(doc.get("name")))
    return rankedfiles

def SearchFiles(command):
    STORE_DIR = "lucene/index"
    getVMEnv().attachCurrentThread()
    # print 'lucene', VERSION
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(directory, True)
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    rankedfiles = run(searcher, analyzer,command)
    searcher.close()
    return rankedfiles
    
if __name__ == '__main__':
    SearchFiles()
