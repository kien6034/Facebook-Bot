from crawler import Crawler 


crawler = Crawler()
group_url = "https://www.facebook.com/groups/GhienPhuQuoc"

crawler.login()
crawler.go_to_group(group_url)
crawler.get_group_posts()
crawler.quit()