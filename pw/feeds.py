import datetime as dt
from typing import Any
from pathlib import Path

import django.utils.timezone as timezone
from django.contrib.syndication.views import Feed
from django.utils import feedgenerator
from coltrane.config.settings import get_description, get_site_url, get_title
from coltrane.retriever import ContentItem, get_content_items


class CustomFeedGenerator(feedgenerator.Atom1Feed):
    def item_attributes(self, item: dict[str, Any]) -> dict[Any, Any]:
        return {"content": item["content"]}


class ContentFeed(Feed):
    title = get_title()
    description = get_description()
    feed_type = CustomFeedGenerator

    @property
    def site_url(self):
        site_url = get_site_url()
        assert (
            site_url
        ), "COLTRANE_SITE_URL in .env or COLTRANE.SITE_URL in settings file is required"

        return site_url

    def items(self):
        return get_content_items()

    def item_title(self, item: ContentItem):
        return item.metadata.get("title")

    def item_description(self, item: ContentItem):
        return item.metadata.get("description")

    def item_link(self, item: ContentItem):
        site_url = self.site_url

        if site_url.endswith("/"):
            site_url = site_url[:-1]

        link = f"{site_url}{item.relative_url}"

        return link

    def item_pubdate(self, item: ContentItem):
        publish_date = item.metadata.get("publish_date")
        if not publish_date:
            return None

        if isinstance(publish_date, dt.date):
            publish_date = dt.datetime(
                publish_date.year, publish_date.month, publish_date.day, 16, 0, 0
            )

        return timezone.make_aware(publish_date, timezone.get_current_timezone())

    def link(self, obj):
        return self.site_url

    def item_extra_kwargs(self, item: ContentItem):
        return {"content": Path(item.path).read_text()}
