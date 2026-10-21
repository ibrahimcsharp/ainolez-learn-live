"""Tables from database/schema/0017_website_pages_menus.sql."""

from django.db import models

from shared.models import BaseModel


class SitePage(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100)
    summary = models.CharField(max_length=300, blank=True)
    content_md = models.TextField(null=True, blank=True)
    content_html = models.TextField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "site_pages"
        verbose_name = "page"


class Menu(BaseModel):
    class Location(models.TextChoices):
        HEADER = "header"
        FOOTER = "footer"

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=10, choices=Location)
    sort_order = models.IntegerField(default=0)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "menus"


class MenuItem(BaseModel):
    class LinkType(models.TextChoices):
        PAGE = "page"
        COURSE = "course"
        URL = "url"

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="items")
    label = models.CharField(max_length=100, blank=True)
    link_type = models.CharField(max_length=10, choices=LinkType)
    page = models.ForeignKey(
        SitePage, on_delete=models.CASCADE, null=True, blank=True, related_name="menu_items"
    )
    course_id = models.BigIntegerField(null=True, blank=True)  # catalog module
    url = models.CharField(max_length=500, blank=True)
    open_in_new_tab = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "menu_items"

    @property
    def title(self) -> str:
        """Shown in the Trash and typed to confirm a hard delete."""
        return self.label or f"{self.link_type} link #{self.pk}"
