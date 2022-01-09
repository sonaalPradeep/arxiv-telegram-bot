from decouple import config
import arxiv
from loguru import logger

__version__ = "0.1.0"

query_catalogues = ["cs.CV", "cs.LG", "cs.CL", "cs.AI", "cs.NE", "cs.RO"]
query_string = " OR ".join(query_catalogues)

search = arxiv.Search(
    query=query_string,
    max_results=100,
    sort_by=arxiv.SortCriterion.SubmittedDate,
    sort_order=arxiv.SortOrder.Descending,
)

for result in search.results():
    print(
        f"{result.title} - {result.published}\n{result.categories}\n{result.summary}\n\n"
    )
