# xkcd-discord
A python script to automatically post the latest xkcd webcomic to a discord channel via a webhook.

The script polls the xkcd.com website every hour, and compared it with the number of the last comic it posted.
This number is stored in a small text file the program creates, called last.txt.
If the file does not exist, such as when the program is run for the first time, the program will jump to the latest comic and mark that as the most recent entry.

After reading the contents of the xkcd.com website, the program:
- extracts the relevant data from the html file of the website
- assembles the data into a JSON-formatted embed
- posts the embed to a discord social media channel

This script assumes all xkcd comics are PNG files.
If an xkcd is uploaded as a different file type (eg JPG), it will not display correctly.
If a special interactive xkcd is uploaded, that won't display correctly either.
No provision has yet been made for these cases.

## It is necessary to create a webhook for this bot in the discord server you intend to use it in.
## Paste the webhook link into the string "\[INSERT\_WEBHOOK\_LINK\_HERE\]".
