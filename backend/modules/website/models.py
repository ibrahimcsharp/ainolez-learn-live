"""Tables from database/schema/0017_website_pages_menus.sql, 0018-0020."""

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

    class ShowAs(models.TextChoices):  # header only (0019)
        LINKS = "links"  # its links side by side in the bar
        DROPDOWN = "dropdown"  # its name in the bar, its links under it

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=10, choices=Location)
    show_as = models.CharField(max_length=10, choices=ShowAs, default=ShowAs.DROPDOWN)
    sort_order = models.IntegerField(default=0)
    header_position = models.IntegerField(null=True, blank=True)  # 0020: place in the bar

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "menus"


def delete_links(collector, field, sub_objs, using):
    """CASCADE, minus Django's first step of setting the column to NULL (MySQL
    cannot defer constraint checks), which ck_menu_items_target would refuse.
    The links are simply deleted before the page."""
    collector.collect(
        sub_objs,
        source=field.remote_field.model,
        source_attr=field.name,
        nullable=False,
        fail_on_restricted=False,
    )


class MenuItem(BaseModel):
    class LinkType(models.TextChoices):
        PAGE = "page"
        COURSE = "course"
        URL = "url"
        NONE = "none", "Heading only"  # top level, holds a sub-menu

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="items")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )  # one level: a sub-menu link sits under a top-level link of the same menu
    label = models.CharField(max_length=100, blank=True)
    link_type = models.CharField(max_length=10, choices=LinkType)
    page = models.ForeignKey(
        SitePage, on_delete=delete_links, null=True, blank=True, related_name="menu_items"
    )
    course_id = models.BigIntegerField(null=True, blank=True)  # catalog module
    url = models.CharField(max_length=500, blank=True)
    open_in_new_tab = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    header_position = models.IntegerField(null=True, blank=True)  # 0020: place in the bar

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "menu_items"

    @property
    def title(self) -> str:
        """Shown in the Trash and typed to confirm a hard delete."""
        return self.label or f"{self.link_type} link #{self.pk}"
