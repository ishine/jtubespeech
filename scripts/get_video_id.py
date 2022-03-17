import scrapetube
import os
import argparse
import sys
from tqdm import tqdm

# parsing arguments
def parse_args():
    parser = argparse.ArgumentParser(
        description="get video id (output) from channel id (input)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("channel_id",    type=str,
                        help="the location to read the channel_id text file")
    parser.add_argument("video_id",    type=str,
                        help="the location to write to the video_id text file")
    parser.add_argument("--is_limit",  action='store_true',
                        default=False, help="check if there is a limit to the scrape per channel")
    parser.add_argument("--limit", type=int, default=50,
                        help="scrape limit per channel of videoid")
    parser.add_argument("--sleep", type=int, default=2,
                        help="seconds to sleep between API calls to youtube, in order to prevent getting blocked")       
    return parser.parse_args(sys.argv[1:])


# get video id from channel id (manually added textfile)
# input: channel_id (manual text file)
# output: video_id
class GetVideoId():
    def __init__(self, channel_id, video_id, limit, sleep, is_limit):
        self.channel_id = channel_id
        self.video_id = video_id
        self.limit = limit
        self.sleep = sleep
        self.is_limit = is_limit

    def get_video_id(self):
        # check if the video id filename exists, if exists, delete it to prevent corruption in appending to the text file
        if os.path.isfile(self.video_id):
            os.remove(self.video_id)

        # read the channel_id text file to get the channel ids
        
        with open(self.channel_id, 'r+') as f:
            for line in f.readlines():

                # a switch to check the presence of a limit to the scrape per channel id
                if self.is_limit:
                    videos = scrapetube.get_channel(channel_id=line.strip(), 
                                                    limit=self.limit,
                                                    sleep=self.sleep)
                else:
                    videos = scrapetube.get_channel(channel_id=line.strip(), 
                                                    sleep=self.sleep)

                # then, get the video ids and write it into the video_id text file
                with open(self.video_id, 'a+') as fp:
                    for video in tqdm(videos):
                        fp.write(f'{video["videoId"]}\n')

    def __call__(self):
        return self.get_video_id()

if __name__ == '__main__':
    args = parse_args()
    get_vid_id = GetVideoId(channel_id=args.channel_id,
                            video_id=args.video_id,
                            limit=args.limit,
                            sleep=args.sleep,
                            is_limit=args.is_limit)
    get_vid_id()