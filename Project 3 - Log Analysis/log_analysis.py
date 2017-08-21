#!/usr/bin/env python3
import psycopg2


DB_NAME = "news"

logSuccessView  = """ CREATE OR REPLACE VIEW view_log_success AS
                      SELECT substring(path,10,length(path)) AS slug,
                             status,
                             time
                        FROM log 
                       WHERE substring(path, 0 , 10) = '/article/'
                         AND status = '200 OK' """

logStatusCountiew  = """ CREATE OR REPLACE VIEW view_log_status_count AS
                      SELECT L1.date AS date, 
                              (SELECT count(1) FROM log L2 WHERE L1.date = date(L2.time)) as total_count,
                              (SELECT count(1) FROM log L3 WHERE L1.date = date(L3.time) AND L3.status = '200 OK') as success_count,
                              (SELECT count(1) FROM log L4 WHERE L1.date = date(L4.time) AND L4.status = '404 NOT FOUND') fail_count                        
                         FROM (SELECT DISTINCT date(L.time) AS date FROM log L) L1 """


query1  = """ SELECT a.title, count(1) 
                FROM view_log_success v,articles a
               WHERE a.slug = v.slug
            GROUP BY a.title
            ORDER BY 2 DESC
               LIMIT 3 """

query2  = """ SELECT au.name, count(1) 
                FROM view_log_success v,articles ar, authors au
               WHERE ar.slug   = v.slug
                 AND ar.author = au.id
            GROUP BY au.name
            ORDER BY 2 DESC """


query3  = """ SELECT to_char(t.date,'Mon DD,YYYY'), round((t.fail_count::NUMERIC/t.total_count)*100,2)
                FROM  view_log_status_count t
               WHERE round((t.fail_count::NUMERIC/t.total_count)*100,2) > 1.00 """

def executeAndPrintQuery(cursor, queryString, string):
  cursor.execute(queryString)
  results = cursor.fetchall()
  for result in results:
    print('\t' + result[0] + ' -- ' + str(result[1]) + string)

if __name__ == "__main__":
  db = psycopg2.connect(database=DB_NAME)
  cursor = db.cursor()
  cursor.execute(logSuccessView)
  cursor.execute(logStatusCountiew)

  print('What are the most popular three articles of all time?');
  executeAndPrintQuery(cursor,query1,' views');
  print('Who are the most popular article authors of all time?');
  executeAndPrintQuery(cursor,query2,' views');
  print('On which days did more than 1% of requests lead to errors?');
  executeAndPrintQuery(cursor,query3,'% errros');
  
  db.close()
