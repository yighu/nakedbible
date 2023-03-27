import duckdb
import fitz
import re
from PIL import Image
import base64

#https://pymupdf.readthedocs.io/en/latest/pixmap.html#Pixmap.pdfocr_tobytes
pdfdoc = fitz.open("../data/NBPTranscripts1-458.pdf")
MATRIX = fitz.Matrix(1, 1) 

dbfile='../data/nakebibletranscript_v2.parquet'


def searchByPageNumbRange(f, t):
  return toJson(duckdb.query(f''' SELECT PageNumb,EpisodeNum, Title FROM '{dbfile}' WHERE PageNumb BETWEEN {f} AND {t} '''))

def searchByPageNumb(n):
  return toJson(duckdb.query(f''' SELECT PageNumb,EpisodeNum, Title,Text FROM '{dbfile}' WHERE PageNumb = {n} '''))

def getByPageText(n):
  return toJson(duckdb.query(f''' SELECT PageNumb,EpisodeNum, Title,Text FROM '{dbfile}' WHERE PageNumb = {n} '''))

def searchByEpisodNumb(n):
  return toJson(duckdb.query(f''' SELECT PageNumb,EpisodeNum, Title FROM '{dbfile}' WHERE EpisodeNum = {n}'''))

def searchByTitle(tt):
  return toJson(duckdb.query(f''' SELECT PageNumb,EpisodeNum, Title FROM '{dbfile}' WHERE contains(lower(Title), '{tt.lower()}') '''))

def searchByKeyWord(tt):
  return toJson(duckdb.query(f''' SELECT PageNumb,EpisodeNum, Title FROM '{dbfile}' WHERE contains(lower(tokens), '{tt.lower()}') '''))


#pdf page number = display page number - 1 
def getPageImage(n):
    print(n)
    page=pdfdoc.load_page(n-1)
    pix = page.get_pixmap()  
    #pix = page.get_pixmap(MATRIX)  
    file = f"static/t{n}.jpg"
    #pix.write_png(file)  

    #pix.pil_save(file, optimize=True, dpi=(1200, 850))
    #return file
    return convertImage(pix)
def convertImage(pix):
    #data = base64.b64encode(pix.tobytes(output='png'))
    data = base64.b64encode(pix.pil_tobytes(format="JPEG", optimize=True))
    #img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    #img_buffer = cv2.imencode('.jpg', img)[1]
    return data
def getPageSVG(n):
    page=pdfdoc.load_page(n-1)
    return page.get_svg_image(matrix=fitz.Identity)

#print(getPageSVG(1))

def toJson(data):
  return data.df().to_json(orient = 'records')



#x=searchByPageNumb(1)
x= getByPageText(1)
print(x)
