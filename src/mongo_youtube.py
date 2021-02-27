from dotenv import load_dotenv
import os
import pymongo
import pandas as pd

def call_mongo():
    # load onto MongoDB
    load_dotenv()
    
    # grab credentials
    user = os.environ.get('USER')
    password = os.environ.get('PASSWORD')
    
    client = pymongo.MongoClient(f'mongodb+srv://{user}:{password}@initial.r4nwp.mongodb.net/')
    
    # access database called comments
    return client.comments
    
# check if csv data exists on mongodb
def filter_urls(video_list):
    
    db = call_mongo()
    youtube_collection = db.youtube_collection
    
    # extract urls/titles
    
    for index, video in enumerate(video_list):
        url = video_list['url']
        num = youtube_collection.count_documents({'url': url})
        
        # remove title if data already exists
        if num > 0:
            print("skipping ", video['title'])
            video_list.pop(index)
        else:
            print("confirming ", video['title'])
    
    return video_list

# upload cleaned csv data onto mongodb
def upload_data():
    db = call_mongo()
    youtube_collection = db.youtube_collection
    
    # read in cleaned data
    with open('../../data/youtube_comments_clean.csv',encoding="utf8") as file:
        df = pd.read_csv(file,dtype=str)
    file.close()
     
    # convert data into a dictionary
    df.reset_index(inplace=True)
    df_dict = df.to_dict("records")
    
    print("-" * 10)
    print(df_dict)
        
    inserted = youtube_collection.insert_many(df_dict)
    print("inserted ", len(inserted.inserted_ids), " data points")

