import mysql.connector
import json

def connection():
    return mysql.connector.connect(
        host = 'localhost',
        user = 'docent',
        passwd = 'hoppekee',
        database = 'dreadnought',
        charset = 'utf8',
    )

def get_timeline(hoofdstuk):
    conn = connection()
    try:
         cursor = conn.cursor(dictionary=True)
         sql = "select * from timeline where hoofdstuk=%s order by volgnummer"
         cursor.execute(sql, (hoofdstuk,))
    except mysql.connector.Error as error:
        print (error)
    return list(cursor)

def get_time_item(id):
    conn = connection()
    try:
        cursor = conn.cursor(dictionary=True)
        sql = "select * from timeline where id=%s"
        cursor.execute(sql, (id,))
    except mysql.connector.Error as error:
        print (error) 
    return list(cursor)[0]

def update(data):
    foo = (int(data['jaar']), data['datum'], int(data['paginanummer']), data['koptekst'], data['broodtekst'], int(data['id']))
    conn = connection()
    sql = "update timeline set jaar=%s, datum=%s, paginanummer=%s, koptekst=%s, broodtekst=%s where id=%s"
    cursor = conn.cursor()
    cursor.execute(sql, foo)
    conn.commit()
    return data['id']

def update_position(id, data):
    hoofdstuk = get_time_item(id)['hoofdstuk']
    conn = connection()
    cursor = conn.cursor()
    old, new = data['old'], data['new']
    if (old>new):
        sql = """update timeline set volgnummer=volgnummer+1 
                where volgnummer between %s and %s-1
                and hoofdstuk=%s"""
        cursor.execute(sql, (new,old,hoofdstuk))
    else:
        sql = """update timeline set volgnummer=volgnummer-1 
                where volgnummer between %s and %s
                and hoofdstuk=%s"""
        cursor.execute(sql, (old,new,hoofdstuk))
    sql = "update timeline set volgnummer=%s where id=%s"
    cursor.execute(sql, (new,id))
    conn.commit() 

def insert(data):
    foo = (int(data['jaar']), data['datum'], int(data['paginanummer']), data['koptekst'], data['broodtekst'])
    conn = connection()
    sql = "insert into timeline(jaar, datum, paginanummer, koptekst, broodtekst) values (%s,%s,%s,%s,%s)" 
    cursor = conn.cursor()
    cursor.execute(sql, foo)
    conn.commit()
    id = cursor.lastrowid
    # default volgnummer naar id; aanpassen doen we via de gui
    sql = "update timeline set volgnummer=%s where id=%s"
    cursor.execute(sql, (id, id)) 
    conn.commit()
    return id

def delete(id):
    conn = connection()
    sql = "delete from timeline where id=%s"
    conn.cursor().execute(sql, (id,))
    conn.commit()

#{"id":"1","jaar":"1910","datum":"12-01","paginanummer":"720","koptext":"Germany will defend the interests of German merchants in Morocco.","broodtekst":"The south of Morocco is thought to be exceedingly fertile. German merchants want to settle there, but the road is blocked by the French as a result of the Act of Algeciras. "}
#data = {"jaar":"1921","datum":"12-05","paginanummer":"123","koptekst":"dit is de awesome koptekst","broodtekst":"En hier allemaal mooie <a href='hallo daar'>dingen</a>...", "id":28}
#foo = (int(data['jaar']), data['datum'], int(data['paginanummer']), data['koptekst'], data['broodtekst'], int(data['id']))
#update(foo)
#print (get_timeline(39)[0])
#print (get_time_item(13))
#delete(28)
#insert (data)d
data = {'old':2, 'new':23}
update_position(8, data)