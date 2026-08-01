# Snaf Apple

[![Snaf Apple](https://monstyrslayr.github.io/img/snafApple.png)](https://youtu.be/A3jC-4428_U)

[Snaf Apple](https://youtu.be/A3jC-4428_U)

a snafu is a poorly drawn meme or situation. i combined a ton of them into a bad apple music video

note: snafus were filtered to posts above 1k upvotes, sfw, with its image hosted on reddit. i don't have infinite storage space lol. the number of snafus was taken from to 87,500 to 7,242. these settings can be changed in **filterAllPosts.py**

**please download a video of bad apple beforehand and name it "badApple480.mp4"**

if you get an error just download the library i really don't wanna make a requirements.txt

## Important Files (use in this order)

- **videoToFrames.py**: Converts the bad apple music video to frames and puts it in ./frames

- **getAllPosts.py**: Gets all snafus and puts them into redditPosts.csv

- **filterAllPosts.py**: Applies the above filters to posts, and downloads snafus that meet the post to ./snafus

- **buildDatabase.py**: Takes all snafus and makes the database for bad appling, storing it in ./cache

- **renderFrames.py**: Renders frames in ./frames into snafuFrames in ./snafuFrames, using snafus from ./snafus, and outputs usageStats.csv

- **snafuFramesToVideo.py**: Takes the frames and turns it back into a video

- **readAllUsages.py**: Gets statistics from usageStats.csv and parses it

## Statistics
total posts used: 921

most used posts (id):
1. 1rm1zn3: 16107
1. 1psv4nm: 13139
1. 7rirl8: 12644
1. 1q5el0x: 11606
1. 14jst3d: 9998

most used authors:
1. National_Yak5302: 106
1. Treasure-boy: 55
1. SmallTatorTot: 52
1. Objective_Trick_6406: 44
1. PaxGladeus: 39

most appeared authors:
1. u/CalabiYauFan: 16107
1. u/WimboTurtle: 13139
1. u/HeavyMetalZen: 12644
1. u/JacobGoodNight416: 11606
1. u/giant_pulsating_mind: 10636

## Contributing
pull request
