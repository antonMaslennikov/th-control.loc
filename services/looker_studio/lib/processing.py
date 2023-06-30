from django.db import models
from sites.looker.models import PbnSites, PbnArticles
from .wordpress_api import WordPressAPI
from sites.looker.settings import DB

pbn_sites = PbnSites.objects.using(DB).all()

# Loop through each PbnSite and retrieve the corresponding data using WordPressAPI
for pbn_site in pbn_sites:
    wp_api =WordPressAPI(pbn_site.site_url)
    # Assuming you have a method in WordPressAPI to retrieve PbnArticles
    pbn_articles = wp_api.retrieve_pbn_articles()

    # Save the retrieved PbnArticles in the database
    for pbn_article_data in pbn_articles:
        pbn_article = PbnArticles(
            id_row=pbn_article_data['id'],
            id_article=pbn_article_data['id_article'],
            date_create=pbn_article_data['date_create'],
            date_modified=pbn_article_data['date_modified'],
            text_article=pbn_article_data['text_article'],
            article_name=pbn_article_data['article_name'],
            article_url=pbn_article_data['article_url'],
            pbn_site=pbn_site
        )
        pbn_article.save()
