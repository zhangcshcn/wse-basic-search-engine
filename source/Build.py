import sys, os

cwd = os.getcwd()
os.chdir("source")
sys.path.append(os.getcwd())
os.chdir("../lucene")
sys.path.append(os.getcwd())
os.chdir(cwd)
from crawler import spider
from IndexFiles import IndexDir



def BuildSearchEngine(start,number,domain):
    if "cache" in os.listdir(os.getcwd()):
        os.chdir("cache")
        for pages in os.listdir(os.getcwd()):
            os.remove(pages)
        os.chdir("..")
        # print 'pwd: ', os.getcwd()
    else:
        os.mkdir("cache")           
    fHash = spider(start,number,domain)
    IndexDir()
    return fHash
    
if __name__ == "__main__":
    start = sys.argv[1]
    number = int(sys.argv[2])
    domain = sys.argv[3]
    BuildSearchEngine(start,number,domain)
