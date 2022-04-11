
import requests

# Task: count the number of words returned by web api call

def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())
