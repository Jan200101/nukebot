def escape(content):
    content = (content.replace("*", "\\*")
                      .replace("_", "\\_")
                      .replace("`", "\\`")
                      .replace("~", "\\~"))

    return content