# InstaBOT
program for collecting activity and automatic photo posts in Instagram.

- create file key.py with contents: \
`login = 'your_login'`\
`password = 'your_password'`
- `./main.py` - collecting activity to db (InstaBot.sqlite)
- `./statistic.py` - html report about activity (1.html)
- automatic posts:
  - create directories: `./photos/` and `./caption/`
  - place your files, example: `./photos/IMAGE321.jpg` and `./caption/IMAGE321.txt` (caption text for post)
  - for add many photos in one post just add indexes, example `./photos/IMAGE321_001.jpg` `./photos/IMAGE321_002.jpg` `./photos/IMAGE321_003.jpg`
  - standard posting period - 72 hours = 3 days (change it - `POST_PERIOD` in `main.py`)