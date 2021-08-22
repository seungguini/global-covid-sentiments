import os
from dotenv import load_dotenv
from youcos import scrape_videos, scrape_comments
from process_youtube import process_data
from mongo_youtube import filter_urls, upload_data

def main():
    load_dotenv()
    
    # Authenticate with YouTube API
    KEY = os.environ.get('YOUTUBE_API_KEY')
    
    query = 'stocks'
    
    driver_path = "C:/WebDriver/bin/chromedriver.exe"
    csv_path = "data/youtube_comments.csv"

    video_list = scrape_videos(query, KEY, driver_path=driver_path, maxResults=1)
    
    # Filter out duplicate videos based on DB
    urls_titles_filtered = filter_urls(video_list)
    
    # Scrape comments based on filtered video list
    scrape_comments(urls_titles_filtered, driver_path=driver_path, csv_path=csv_path)
    
    # Process youtube data into youtube_comments_clean.csv
    process_data()
    
    # Upload data to DB
    upload_data()
   

if __name__ == "__main__":
    main() 