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
    parser.add_argument("--channel_id",     type=str, help="the location to read the channel_id text file")
    parser.add_argument("--video_id",       type=str, help="the location to write to the video_id text file")
    parser.add_argument("--is_limit",       action='store_true', default=False, help="check if there is a limit to the scrape per channel")
    parser.add_argument("--limit",          type=int, default=50, help="scrape limit per channel of videoid")
    parser.add_argument("--sleep",          type=int, default=2, help="seconds to sleep between API calls to youtube, in order to prevent getting blocked")  

    return parser.parse_args(sys.argv[1:])


class GetVideoId:
    '''
        a class that takes in the channel_id text file, where the channel_id are manually added from youtube, and outputs all the video ids in the video_id text file
    '''
    def __init__(self, channel_id: str, video_id: str, limit: int, sleep: float, is_limit: bool) -> None:
        self.channel_id = channel_id
        self.video_id = video_id
        self.limit = limit
        self.sleep = sleep
        self.is_limit = is_limit

    def create_new_dir(self, directory: str) -> None:
        '''
            creates new directory and ignore already created ones

            directory: the directory path that is being created
        '''
        try:
            os.mkdir(directory)
        except OSError as error:
            pass # directory already exists!

    def get_video_id(self) -> None:
        '''
            gets the channel id text file and outputs the video id text file
        '''
        # # check if the video id filename exists, if exists, delete it to prevent corruption in appending to the text file
        # if os.path.isfile(self.video_id):
        #     os.remove(self.video_id)

        # make new directory to store the video_id
        video_id_path_split_list = self.video_id.split("/")
        # print(video_id_path_split_list)
        self.create_new_dir(f"{video_id_path_split_list[0]}/") # create the main folder
        self.create_new_dir(f"{video_id_path_split_list[0]}/{video_id_path_split_list[1]}") # create the sub folder

        # check if the video id filename exists, if it exists, throw an error to prevent corruption in appending to the text file
        assert not os.path.isfile(self.video_id), "video id filename already exists, please insert an alternative filename to avoid confusion!"

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