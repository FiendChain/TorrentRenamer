## Torrent Renamer
Renames all torrents to the format {TITLE}-SxxExx-{NAME}.{ext} and places them inside a folder "Season xx". This is useful especially for Plex Media Center, so that it can fetch the correct metadata for each episode.

E.g. A.TV.Show//Season 01//A.TV.Show-S01E01-The.Name.mp4

Uses the 
[tvdb API](https://api.thetvdb.com/swagger)
to get names for the files, then does regex and filtering to rename and delete files.

## Gallery
![alt text](docs/window_v1.png "GUI")

## Gui Usage
```bash
# activate your virtual environment or install dependencies
pip install -r requirements.txt

# start the qt gui app
# use python main.py -h for help
python main.py [ROOTDIR] [OPTIONS]
```

## CLI Usage
Run the following scripts (1-4) in the following order.

```bash
# 1. Cache all data about each tv show in each folder inside base
#    For each folder, it will prompt a list of possible tv shows
#    Generates a series.json at the root of the subdirectory
python cache_series_data.py (base_dir)

# 2. Cache all data about the episodes for each tv show
#    For each folder it generates an episodes.json file
#    This contains a list of data for each episode (to the date)
python cache_episodes_data.py (base_dir)

# 3. Rename the files inside each folder
#    Uses series.json and episodes.json cache to rename
#    Formats to common format shown at start of readme
#    If out of date, then refresh the cache
#    This can be done by deleting the series.json and episodes.json 
#    then run steps 1 and 2 manually
python rename_episodes.py (base_dir)

# 4. Remove garbage files inside each folder
#    These are usually .txt or .nfo files that come with the torrent
#    Will ask a prompt for each tv show folder (y/n)
python delete_garbage.py (base_dir)
```

## Todo
- Move "deleted" files to the recycle bin
- Add a mapping file, which links the original filepath to new filepath
- Implement support for active torrents 
  - Allow for rename while torrent is active
  - Could use symlinks or simply clone files
  - Would require a designated torrenting folder
  - Auto detect when a torrent is active (read state files or use web api)