import requests
import bs4
import re


def search(name: str):
    name_string = f"data+robot+{name.replace(' ', '+')}"
    link = get_linkedin(f"https://www.google.com/search?q=linkedin+{name_string}&num1")
    return link


def get_linkedin(target: str):
    request_result = requests.get(target)

    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
    link_list = []

    # find all the anchor tags with "href"
    # attribute starting with "https://"
    for link in soup.find_all('a', attrs={'href': re.compile("q=https://")}):
        link_list.append(link.get('href'))

    # split string for usable hyperlink to LinkedIn
    # print(link_list[0])
    link = link_list[0]
    new_link = link[7:100]
    # print(new_link.rsplit('&')[0])
    link_final = new_link.rsplit('&')[0]
    # print(link_final)
    return link_final

#
# # url4 = "https://www.google.com/search?q=linkedin+datarobot+olha+ruban&num=1"
# url5 = search('evan fournier')
#
# request_result = requests.get(url5)
#
# soup = bs4.BeautifulSoup(request_result.text, "html.parser")
# soup2 = bs4.BeautifulSoup(request_result.content, "html.parser")
#
# link_list = []
#
# # find all the anchor tags with "href"
# # attribute starting with "https://"
#
# for link in soup.find_all('a', attrs={'href': re.compile("q=https://")}):
#     link_list.append(link.get('href'))
#
# #split string for usable hyperlink to LinkedIn
# # print(link_list[0])
# link = link_list[0]
# new_link = link[7:100]
# # print(new_link.rsplit('&')[0])
# link_final = new_link.rsplit('&')[0]
# print(link_final)
