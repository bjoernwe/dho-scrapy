import pytest

from data_tools.dho_message import ForumMessage
from scraper.pipelines.pipelines import HtmlToTextPipeline
from scraper.pipelines.pipelines import RedactUserPipeline
from scraper.pipelines.pipelines import RemoveDhOBlockquotesPipeline
from scraper.pipelines.pipelines import RemoveDuplicateSpacesPipeline
from scraper.pipelines.pipelines import RemoveShortMessagePipeline
from scraper.pipelines.pipelines import ReplaceNonStandardWhitespacesPipeline


def test_dho_blockquote_title_tags_are_removed():

    # GIVEN some HTML with DhO-style block quote title tag
    html = '<div class="quote-title other">TITLE</div>OTHER TEXT'

    # WHEN the HTML is filtered
    filtered = RemoveDhOBlockquotesPipeline._remove_blockquotes(html)

    # THEN the result does not contain quote title anymore (but other text)
    assert "OTHER TEXT" in filtered
    assert "TITLE" not in filtered


def test_dho_blockquote_tags_are_removed():

    # GIVEN some HTML with DhO-style block quote tag
    html = '<div class="quote other">A QUOTE</div>OTHER TEXT'

    # WHEN the HTML is filtered
    filtered = RemoveDhOBlockquotesPipeline._remove_blockquotes(html)

    # THEN the result does not contain quotes anymore (but other text)
    assert "OTHER TEXT" in filtered
    assert "A QUOTE" not in filtered


def test_html_is_removed_from_message(dho_msg: ForumMessage):

    # GIVEN a DhO message with HTML tags
    html = dho_msg.msg
    assert "<" in html

    # WHEN the HTML is turned into text
    text = HtmlToTextPipeline._html_to_text(html)

    # THEN tags are removed and regular text preserved
    assert "brain wave" in text
    assert "<" not in text


def test_non_standard_whitespace_is_removed_from_message():

    # GIVEN a string with non-standard whitespaces
    whitespaces = ["\u00a0", "\u200b"]
    unfiltered_message = "".join(whitespaces)
    for ws in whitespaces:
        assert ws in unfiltered_message

    # WHEN the string is filtered
    filtered_message = ReplaceNonStandardWhitespacesPipeline._normalize_whitespaces(
        unfiltered_message
    )

    # THEN the non-standard whitespaces are removed
    for ws in whitespaces:
        assert ws not in filtered_message


def test_duplicate_spaces_are_removed_from_message():

    # GIVEN a string with duplicate white spaces
    unfiltered_message = " foo   bar  "

    # WHEN the message is filtered
    filtered_message = RemoveDuplicateSpacesPipeline._remove_duplicate_spaces(
        unfiltered_message
    )

    # THEN the duplicates are removed
    assert filtered_message == "foo bar"


@pytest.mark.parametrize(
    argnames=["msg", "min_words", "too_short"],
    argvalues=[("foo", 2, True), ("foo bar", 2, False)],
)
def test_messages_can_be_filtered_for_number_of_words(
    msg: str, min_words: int, too_short: bool
):

    # GIVEN a message and a min number of words
    # WHEN the message is filtered for length
    is_msg_too_short = RemoveShortMessagePipeline._is_too_short(
        msg=msg, min_words=min_words
    )

    # THEN it is filtered as expected
    assert is_msg_too_short == too_short


def test_user_name_can_be_redacted(dho_msg: ForumMessage):

    # GIVEN a RedactUserPipeline
    redact_pipeline = RedactUserPipeline()

    # WHEN a message is processed
    dho_msg.author = "TEST AUTHOR"
    processed_msg = redact_pipeline.process_item(item=dho_msg.copy())

    # THEN the author has been redacted
    assert processed_msg.author != dho_msg.author
    assert processed_msg.author == "squalid-big"
