from tools.config import youtube_api_key

from googleapiclient.discovery import build
from dataclasses import dataclass
from datetime import datetime

@dataclass
class VideoSnippet:
    id: str
    title: str
    channelId: str
    channelTitle: str
    publishedAt: str
    daysSincePublished: int = None

@dataclass
class VideoDetails:
    videoString: str
    title: str
    viewCount: int
    likeCount: int
    commentCount: int
    subscriberCount: int
    score: float

def get_videos_by_topic(topic, number_of_results):
    # Set up the YouTube Data API client
    api_service_name = "youtube"
    api_version = "v3"
    api_key = youtube_api_key  # Replace with your own API key
    youtube = build(api_service_name, api_version, developerKey=api_key)

    # Call the search.list method to search for videos based on the topic
    request = youtube.search().list(
        part="snippet",
        q=topic,
        type="video",
        maxResults=number_of_results,  # Adjust the number of results as needed
    )
    response = request.execute()

    # Process the response and return a generator of video information
    for item in response["items"]:
        published_date = datetime.strptime(item["snippet"]["publishedAt"][:10], "%Y-%m-%d")
        current_date = datetime.now()
        days_since_published = (current_date - published_date).days
        snippet = VideoSnippet(
            item["id"]["videoId"],
            item["snippet"]["title"],
            item["snippet"]["channelId"],
            item["snippet"]["channelTitle"],
            item["snippet"]["publishedAt"],
            days_since_published
        )
        yield snippet

def get_video_details(snippet: VideoSnippet):
    # Set up the YouTube Data API client
    api_service_name = "youtube"
    api_version = "v3"
    api_key = youtube_api_key  # Replace with your own API key
    youtube = build(api_service_name, api_version, developerKey=api_key)

    vid_request = youtube.videos().list(
        part="snippet,statistics",
        id=snippet.id
    )
    vid_response = vid_request.execute()

    channel_request = youtube.channels().list(
        part="statistics",
        id=snippet.channelId
    )
    channel_response = channel_request.execute()

    title = snippet.title
    view_count = int(vid_response["items"][0]["statistics"]["viewCount"])
    like_count = int(vid_response["items"][0]["statistics"]["likeCount"])
    comment_count = int(vid_response["items"][0]["statistics"]["commentCount"])
    subscriber_count = int(channel_response["items"][0]["statistics"]["subscriberCount"])

    video_string = f"   - Title: {title}\n   - Channel: {snippet.channelTitle}\n   - View Count: {view_count}\n   - Days Since Published: {snippet.daysSincePublished}\n   - Likes: {like_count}\n   - Subscriber Count: {subscriber_count}\n   - Video URL: https://www.youtube.com/watch?v={snippet.id}\n"
    if subscriber_count != 0 and view_count != 0 and snippet.daysSincePublished != 0:
        score = (((view_count / subscriber_count) * 0.4) + ((like_count / view_count) * 0.3) + ((comment_count / view_count) * 0.2)) * (1 / snippet.daysSincePublished)
    else:
        score = 0

    video_details = VideoDetails(
        video_string,
        title,
        view_count,
        like_count,
        comment_count,
        subscriber_count,
        score
    )

    return video_details