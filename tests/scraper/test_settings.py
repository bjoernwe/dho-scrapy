from scrapy.utils.project import get_project_settings


def test_feeds_have_file_scheme():

    # GIVEN the settings for the Scrapy project
    settings = get_project_settings()

    # WHEN the output feeds are considered
    for out_file in settings["FEEDS"]:

        # THEN they have a file:// scheme
        # (otherwise, on Windows, C: would be interpreted as scheme)
        assert out_file.startswith("file://")
