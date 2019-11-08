import feedparser
import psycopg2
import facebook

def selectQuery(query):
    cur.execute(query)
    return cur.rowcount

def insert_query(query,data):
    log = []
    log.append(data,)
    cur.execute(query,log)
    conn.commit()

url = "URL"
try:
    conn = psycopg2.connect("DBSTRING")
    cur = conn.cursor()
except:
    print("An error has occured")

while(1):
    feed = feedparser.parse(url)
    if len(feed['entries']) != selectQuery("select * from table"):
        for article in feed['entries']:
            query = "select * from articles where title='"+str(article['title']) +"' AND url ='"+str(article['link']+"'")
            if selectQuery(query) == 0:
                insert_query("insert into articles values %s",(article['title'],article['link']))
                token='token'
                fb = facebook.GraphAPI(access_token=token)
                fb.put_object(parent_object='me',connection_name='feed',message='Titolo : '+str(article['title']) + " url : " +str(article['link']))       
