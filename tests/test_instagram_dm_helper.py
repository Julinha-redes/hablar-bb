from utils.instagram_dm_helper import analyze_and_suggest


def test_analyze_and_suggest_generates_caring_reply():
    conversations = [
        {
            "participant": "ana",
            "messages": [
                {"sender": "ana", "text": "Amei seus vídeos, você é incrível!", "timestamp": 1},
                {"sender": "saminho", "text": "Obrigada!", "timestamp": 2},
            ],
        }
    ]

    result = analyze_and_suggest(conversations, influencer_username="saminho", seed=1)

    assert result.participant == "ana"
    assert "Amei seus vídeos" in result.first_message
    assert result.sentiment == "positivo"
    assert "Oii" in result.suggested_reply
    assert "Me conta uma coisa" in result.suggested_reply
