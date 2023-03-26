from data_tools.textsnippet import TextSnippet


def test_different_objects_with_same_content_have_same_sid():

    # GIVEN two sentences with same content
    s1 = TextSnippet(source_msg_id=123, text="foo")
    s2 = TextSnippet(source_msg_id=123, text="foo")

    # WHEN their ID is calculated
    # THEN it is the same for both sentences
    assert s1.sid == s2.sid


def test_sentences_can_be_concatenated_through_addition():

    # GIVEN two sentences with
    s1 = TextSnippet(source_msg_id=123, text="foo")
    s2 = TextSnippet(source_msg_id=123, text="bar")

    # WHEN the sentences are added
    s = s1 + s2

    # THEN their content is concatenated
    assert s.source_msg_id == 123
    assert s.text == f"{s1.text} {s2.text}"
