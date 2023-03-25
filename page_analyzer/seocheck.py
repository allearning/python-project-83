'SEOCheck class'
import datetime


class SEOCheck:
    """
    Class representing SEO Check data.

    Attributes
    ----------
    url_id : int
        page to check id
    id : int
        id of check
    status_code : int
        HTML Response code for check
    h1 : str
        h1 tag f page
    title : str
        title of page
    description : str
        content description of page in meta
    """

    def __init__(
        self,
        url_id: int,
        status_code: int,
        h1: str,
        title: str,
        description: str,
        check_id: int = 0,
        created_at: datetime.date = None,
    ) -> None:
        """Init SEOCheck."""
        self.url_id = url_id
        self.id = check_id
        self.status_code = status_code
        self.h1 = h1
        self.title = title
        self.description = description
        if not created_at:
            created_at = datetime.date.today()
        self.created_at = created_at
