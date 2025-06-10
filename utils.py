def format_post(post, hashtag=""):
    text = post["text"] or ""
    if hashtag:
        text += f"\n\n{hashtag}"
    return text