from scraper.pipelines import RemoveDhOBlockquotesPipeline


def test_dho_blockquotes_are_removed():

    # GIVEN some HTML with DhO-style block quote tag
    html = '<div class="quote other">A QUOTE</div>OTHER TEXT'

    # WHEN the HTML is filtered
    filtered = RemoveDhOBlockquotesPipeline._remove_blockquotes(html)

    # THEN the result does not contain quotes anymore (but other text)
    assert 'OTHER TEXT' in filtered
    assert 'A QUOTE' not in filtered
