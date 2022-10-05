from time import sleep
from bot.crawler import Crawler
from bot.thinker import Thinker

crawler = Crawler()
group_url = [
    "https://www.facebook.com/groups/GhienPhuQuoc",
   
]

#  "https://www.facebook.com/groups/799500246879488",
#     "https://www.facebook.com/groups/reviewphuquockiengiang/",
#     "https://www.facebook.com/groups/314463613422569/",
#     "https://www.facebook.com/groups/1105257046642653"
crawler.login()

for url in group_url:
    crawler.go_to_group(url)
    crawler.get_group_posts()

#crawler.quit()

# thinker = Thinker()
# thinker.run()


# crawler = Crawler()

# crawler.login()
# crawler.go_to_post("https://www.facebook.com/groups/GhienPhuQuoc/posts/2316795068483324/")
# sleep(2)
# crawler.comment()