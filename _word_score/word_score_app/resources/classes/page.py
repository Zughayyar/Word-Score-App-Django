
# Page Class to carry the page attributes for reusability
class Page:
    """A simple Page class to represent the downloaded HTML page."""
    def __init__(self, content: str, url: str):
        self.content = content
        self.url = url

    def get_content(self) -> str:
        return self.content

    def get_url(self) -> str:
        return self.url
