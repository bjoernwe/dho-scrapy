from data_models.sentence import Sentence


def test_different_objects_with_same_content_have_same_sid():

    # GIVEN two sentences with same content
    s1 = Sentence(msg_id=123, sentence_idx=99, sentence="foo")
    s2 = Sentence(msg_id=123, sentence_idx=99, sentence="foo")

    # WHEN their ID is calculated
    # THEN it is the same for both sentences
    assert s1.sid == s2.sid
