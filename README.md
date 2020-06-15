# Buy Canadian Wiki Bot (wiki-replier)


This is a Reddit bot that replies to [/r/BuyCanadian](https://www.reddit.com/r/BuyCanadian/) posts with relevant pages and info from [OurCanadianWiki](https://wiki.ourcanadian.ca/)

To install and run the Wiki-Replier you need have [git](https://git-scm.com/downloads), [python3](https://www.python.org/downloads/), and [pip3](https://vgkits.org/blog/pip3-windows-howto/) installed (these are all included in Mac dev-tools but will need to be added manually on Windows).

Open your command terminal in the directory in which you would like to Ocwa and clone the repo.
```
git clone https://github.com/ourcanadian/wiki-replier.git
```

Enter the repo and install the neccassary libraries.
```
cd wiki-replier
pip3 install -r requirements.txt
```

In order to get to the good stuff, you will need the API Token and login info, which are kept private to prevent security risks. These things are only ever stored in local `praw.ini` files. Request the `praw.ini` content from an admin or via rylancole@ourcanadian.ca. Once you have the content, create a `praw.ini` file in the `wiki-replier/` directory, and don't worry `.gitignore` will make sure you don't push the `praw.ini` file up to github. That would be trouble.

Now you can run the bot from within the directory and it will fetch posts from the last 30 minutes, up to 20 posts.
```
python3 main.py
```

You can customize the amount of time it goes back with an argument. (e.g. 2 hours)
``` 
python3 main.py 120
```

You can customize the limit to how many posts it fetches with a second argument. (e.g. 24 hours, 100 posts)
``` 
python3 main.py 1440 100
```

---

## How does the bot message slack?

It won't from your local instance unless you have a Slack web hook saved as an eviroment variable named `BCWB_SLACK_URL`
