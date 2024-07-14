from dotenv import load_dotenv
load_dotenv()

from tools.video.main import print_video

def run():
    print_video()

if __name__ == "__main__":
    run()