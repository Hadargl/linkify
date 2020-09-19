from imagetotext import build_url_path


def test_delete_domain():
    input_ = 'youtube.com/jksfgksfgk'
    desired_output = '/jksfgksfgk'
    match = 'youtube.com'

    actual_output = build_url_path(input_, match)

    assert actual_output == desired_output


def test_delete_reddit_domain():
    input_ = 'oldsedditcom/1/LivestreamFail/'
    desired_output = 'LivestreamFail/'
    match = 'old.reddit.com/r/'

    actual_output = build_url_path(input_, match)

    assert actual_output == desired_output


