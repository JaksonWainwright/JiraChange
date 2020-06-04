import UrlList


current_url_from_stupid_am = 'https://www.someshit.com/imnotgay'


url_list = UrlList.urls

for url in url_list:
    if url in current_url_from_stupid_am:
        print(url)