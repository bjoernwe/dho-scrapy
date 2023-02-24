from data_models.sentence import Sentence


def test_different_objects_with_same_content_have_same_sid():

    # GIVEN two sentences with same content
    s1 = Sentence(msg_id=123, sentence_idx=99, sentence="foo")
    s2 = Sentence(msg_id=123, sentence_idx=99, sentence="foo")

    # WHEN their ID is calculated
    # THEN it is the same for both sentences
    assert s1.sid == s2.sid


def test_sentences_can_be_concatenated_through_addition():

    # GIVEN two sentences with
    s1 = Sentence(msg_id=123, sentence_idx=0, sentence="foo")
    s2 = Sentence(msg_id=123, sentence_idx=1, sentence="bar")

    # WHEN the sentences are added
    s = s1 + s2

    # THEN their content is concatenated
    assert s.msg_id == 123
    assert s.sentence_idx == 0
    assert s.sentence == f"{s1.sentence} {s2.sentence}"
