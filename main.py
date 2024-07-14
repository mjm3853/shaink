from tools.video.main import get_videos_by_topic, get_video_details


def run():
    scored_videos = []
    for video in get_videos_by_topic("golf tips", 50):
        details = get_video_details(video)
        scored_videos.append((video, details))
        scored_videos.sort(key=lambda x: x[1].score, reverse=True)
        scored_videos = scored_videos[:15]

    for scored_video in scored_videos:
        print(f"{scored_video[0].title} ({scored_video[1].score})")
        print(scored_video[1].videoString)


if __name__ == "__main__":
    run()
