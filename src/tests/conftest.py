from datetime import datetime

import pytest

from scraper.items import DhOMessage


@pytest.fixture
def msg_with_blockquote() -> DhOMessage:
    return DhOMessage(
        title='RE: Letter and Invitation: Living Buddhas in Pemako Sangha',
        author='George S',
        date=datetime(2022, 6, 30, 17, 41, 42),
        msg='<div class="quote"><div class="quote-content">Kim Katami<br />I haven&#39;t written posts like this in a long time but for some reason I did so today.<br /></div></div><br />If I had to guess:<br /><br />73 x 30 = 2,190<br /><br />Buddha inflation <img alt="emoticon" src="https://www.dharmaoverground.org/o/classic-theme/images/emoticons/tongue.gif" >',
    )
