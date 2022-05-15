# JTubeSpeech YouTube Audio and Transcript Scraper Pipeline
A forked repository that scrapes the audio and transcripts from youtube videos based on youtube's channel ID using the `youtube-dl` library. This scraping pipeline have slight differences from the main repository of JTubeSpeech. Please refer to the official [JTubeSpeech](https://github.com/sarulab-speech/jtubespeech) for the original implementation if you are interested.

## Introduction
### Tasks in this pipeline
The tasks in this pipeline are as follows:   
1. [Obtain Channel ID from Youtube (Manual Step)](#obtain-channel-id-from-youtube)
2. [Get Video ID from Channel ID](#get-video-id-from-channel-id)
3. [Check Subtitle Exists](#check-subtitle-exists)
4. [Pruning and Batching of Video ID](#pruning-and-batching-of-video-id)
5. [Download Video and Transcripts](#download-video-and-transcripts) 
6. [Data Preprocessing](#data-preprocessing)
    
Note that some of the codes here will require the ISO 639-1 language code of the target audio and transcript language that you want to scrape. You can get the ISO 639-1 language code of all the languages [here](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).
    
## Project Organization
There will be some folders generated along the way as the codes are executed in this pipeline. The instructions will be shown below in the repository structure on what will be generated as the codes are being executed.   
  
The repository structure will be as shown below:   
TODO: UPDATE THE TREE STRUCTURE
```
    .
    ├── docker-compose.yml      <--- the file used to build the docker container which will make use of the Dockerfile
    ├── Dockerfile              <--- storing all the dependencies required to build the container, including requirements.txt, building packages from source etc.
    ├── img                     <--- a directory of the images just for the readme
    ├── kenlm
    │   └── kenlm               <--- a folder with all the kenlm dependencies
    ├── LICENSE
    ├── README.md               
    ├── requirements.txt        <--- all the dependencies that are required to pip install
    └── tasks                   <--- main directory where all the execution of code takes place
        ├── preprocessing       <--- directory to store all the code (logic), also the directory where execution of code is done locally
        │   ├── datasets        <--- <CREATE THIS FOLDER>
        │   │    └── <PUT YOUR DATASETS HERE>
```
   
## Executing the code
### Getting Started - Via Docker
**Preferably, a Linux OS should be used**   
1. Ensure that docker is installed in your computer   
2. Clone this repository  
```shell
git clone https://github.com/nicholasneo78/jtubespeech
```
3. Open the terminal and go to the root directory of this repository  
4. Build the Dockerfile that is created in the repository using the docker-compose.yml file
```shell
docker-compose up --build -d
```
5. After building the docker image, check if the image is successfully built, by typing the following command
```shell
docker images
```
You should see the image `jtubespeech` with the tag `latest` in the list of docker images   

### Entering the docker container
To enter into the docker container with the build dependencies, execute the command
```shell
docker-compose run local bash
```
The codes are then ready to be executed inside the docker image, more information about executing each code will be discussed below.   

## Obtain Channel ID from YouTube
This is the **only** manual step needed by the users to retrieve the [YouTube](https://youtube.com) Channel ID. Users are to decide the language of the audio that they want to scrape and proceed to source for the Channel ID of that language domain. The subsequent tasks in the pipeline will be automated with scripts.    

#### How to do it?
Go to YouTube, search your query and go to the video's channel home page. Look out for the url at the top of the webpage, for example:   
  
![img1](./img/channel_id_1.jpg)   
  
The Channel ID in this case will be the one underlined in green, which is `UCehF8ZcRIFXFEXKuby3aOvQ`. Create a text file with the command shown below, copy the Channel ID and paste it in that text file.     
```shell
# inside docker container
cd /jtubespeech/channel_id
mkdir <YOUR_LANGUAGE_ID>  # if it is indonesian, then can skip it since there is already an example .txt file containing the channel id of the indonesian language domain
cd <YOUR_LANGUAGE_ID>
vi <YOUR_TEXT_FILENAME_CONTAINING_YOUR_CHANNEL_ID>.txt (proceed to paste the channel ID in the text file)
```
   
There will be an example text file with some channel ID in this repository, at `./jtubespeech/channel_id/id/id_1.txt` (indonesian language domain channels).   
    
#### Note
There may be instances where the Channel ID uses personalized links as shown below.   
  
![img2](./img/channel_id_2.jpg)   
   
As such, an extra step of inspecting the web element is required. You can do so by inspecting the web element, then search for the keyword `canonical`. There will be a few search results, search for the one with the tag `<link rel="canonical" href= ...`, the Channel ID will appear on this line. An example is as shown below:   
   
![img3](./img/channel_id_3.jpg)    
  
You can then copy the Channel ID from the web elements and proceed to add it into the text file.   
    
## Get Video ID from Channel ID   
To read in the Channel ID text file, with all the target channel ID, and output all the Video ID of the channels into another text file.   
   
#### Arguments
`channel_id`: (str) the input channel .txt filepath with all the target Channel IDs   
`video_id`: (str) the output video .txt filepath with all the Video IDs in the channel   
`is_limit`: [optional] (bool) to check if there is a limit to the scrape per channel   
`limit`: [optional] (int) scrape limit per channel of videoid   
`sleep`: [optional] (int) how many seconds to sleep between API calls to youtube, in order to prevent getting blocked   
   
#### Return
None, but outputs the text file with all the Video ID

**TODO: Continue from here**   
   
## Contributors of the main JtubeSpeech repository
- [Shinnosuke Takamichi](https://sites.google.com/site/shinnosuketakamichi/home) (The University of Tokyo, Japan) [main contributor]
- [Ludwig Kürzinger](https://www.ei.tum.de/mmk/personen/mitarbeiter/ludwig-kuerzinger/) (Technical University of Munich, Germany)
- [Takaaki Saeki](https://takaaki-saeki.github.io/) (The University of Tokyo, Japan)
- [Sayaka Shiota](http://www-isys.sd.tmu.ac.jp/) (Tokyo Metropolitan University, Japan)
- [Shinji Watanabe](https://sites.google.com/view/shinjiwatanabe) (Carnegie Mellon University, USA)

## Useful Link
- [youtube-dl](https://github.com/ytdl-org/youtube-dl)
- [JTubeSpeech Research Paper](https://arxiv.org/abs/2112.09323)
- [Other corpora by main contributor](https://sites.google.com/site/shinnosuketakamichi/publication/corpus)
