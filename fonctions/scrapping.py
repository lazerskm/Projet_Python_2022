import urllib, urllib.request
import xmltodict
import praw
import datetime



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
        
        
        """auts = []
        if type(elem["author"]) == list:
            for a in elem["author"]:
                auteur = Author(a.get('name'), 0, {})
                auts.append(auteur)
        else:
            auteur = Author(elem["author"].get('name'), 0, {})
            auts.append(auteur)
        date = datetime.datetime.strptime(elem["published"], '%Y-%m-%dT%H:%M:%SZ')
        doc = Document(elem["title"], auts, date, elem["link"][0]["@href"], elem["summary"].replace('\n', ' '))
        docs.append(doc)"""
    return docs


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
        
        
        """auts = []
        if post.author != None:
            auteur = Author(post.author.name, 0, {}) 
            auts.append(auteur)
        else:
            auts.append(None)
        date = post.created
        doc = Document(post.title, auts, datetime.datetime.fromtimestamp(date), post.url, post.selftext.replace('\n', ' '))
        docs.append(doc)"""
    return docs