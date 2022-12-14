import urllib, urllib.request
import xmltodict
import praw
import datetime


#Scrapping pour les données arxiv
def arxiv_scrapping():
    url = 'http://export.arxiv.org/api/query?search_query=all:basketball&max_results=100'
    data = urllib.request.urlopen(url)
    data_dict = xmltodict.parse(data)
    feed = data_dict["feed"]
    entry = feed["entry"]
    docs = []
    for elem in entry:
        elem["summary"] = elem["summary"].replace('\n', ' ')
        elem["title"] = elem["title"].replace('\n', '')
        elem["published"] = datetime.datetime.strptime(elem["published"], '%Y-%m-%dT%H:%M:%SZ')
        try:
            elem["author"] = ", ".join([a["name"] for a in elem["author"]])  # On fait une liste d'auteurs, sÃ©parÃ©s par une virgule
        except:
            elem["author"] = elem["author"]["name"]
        docs.append(("arxiv" , elem))
    return docs

#Scrapping pour les données Reddit
def reddit_scrapping():
    reddit = praw.Reddit(client_id='IVZ3ND2OTMImg7UQ5wVcvg', client_secret='LQJqPfFFWvRVI5wEMhtG0GSckNmvoQ', user_agent='TD3_scrapping', check_for_async=False)
    hot_posts = reddit.subreddit('basketball').top()
    docs = []
    for post in hot_posts:
        if post.selftext == "":
            continue
        if post.author == None:
            continue
        post.selftext = post.selftext.replace('\n', ' ')
        post.title = post.title.replace('\n', ' ')
        post.author.name = str(post.author.name)
        post.created = datetime.datetime.fromtimestamp(post.created)
        docs.append(("reddit" , post))
    return docs