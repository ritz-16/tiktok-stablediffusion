#Python 1 code goes here
import datetime
import mysql.connector
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent,LikeEvent
import tracemalloc

mydb=mysql.connector.connect(host='localhost',user='root',password='@Padartha1',database='tiktoksd')#connector to database
client=None


async def on_comment(event: CommentEvent):
    #print(f"{event.user.nickname} -> {event.comment}")
    tm=datetime.datetime.now()
    imagePath=f'/Users/ritamghosh/Desktop/stable-diffusion/outputs/img-samples/{event.user.nickname}_{tm}.png'
    sql1=('insert into data1(username,comment,imagePath,status,createdAt) values(%s,%s,%s,%s,%s)')
    data1=(event.user.nickname,event.comment,imagePath,'null',datetime.datetime.now())
    x=mydb.cursor()
    x.execute(sql1,data1)
    mydb.commit()

async def on_like(event: LikeEvent):
    print(f"{event.user.nickname} liked the stream!")
    tm=datetime.datetime.now()
    imagePath=f'/Users/ritamghosh/Desktop/stable-diffusion/outputs/img-samples/{event.user.nickname}_{tm}.png'
    sql2=('insert into data1(username,comment,imagePath,status,createdAt,EventType) values(%s,%s,%s,%s,%s,%s)')
    data2=(event.user.nickname,f"{event.user.nickname} liked your live",imagePath,'null',datetime.datetime.now(),1)
    x=mydb.cursor()
    x.execute(sql2,data2)
    mydb.commit()
    
    
    
def tiktokapi(unique_id):
    tracemalloc.start()
    global client
    client=TikTokLiveClient(unique_id)
    client.add_listener("comment", on_comment)
    client.add_listener("like", on_like)
    client.run()
    




