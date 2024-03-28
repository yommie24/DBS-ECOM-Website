from fastapi import APIRouter, HTTPException, Depends
import aiosqlite
import bs4, requests
import datetime
from ..util import utils
from ..models import datamodels

router = APIRouter(
    prefix="/scrapes"
)


@router.post("/add")
async def add_scrape(to_scrape: datamodels.ScrapeTarget):
    """Add a resource to scrape from. Accepts ScrapeTarget(url, frequency_minutes, selector)."""
    async with aiosqlite.connect("./prime.db") as db:
        await db.execute("INSERT INTO tracking VALUES (?, ?, ?)",
                         (to_scrape.url, to_scrape.frequency, to_scrape.selector,))
        await db.commit()


@router.get("/latest")
async def scrape_now():
    """[Unfinished, time constraints] Scrape and post to a webhook immediately."""
    async with aiosqlite.connect("./prime.db") as db:
        db.row_factory = utils.dict_factory
        cursor = await db.execute("SELECT * FROM tracking")
        targets = [datamodels.ScrapeTarget.model_validate(row) for row in await cursor.fetchall()]
    return [await scrape(target) for target in targets]


async def scrape(target: datamodels.ScrapeTarget):
    html = requests.get(target.url)
    bs = bs4.BeautifulSoup(html.content, "html.parser")
    out = []
    async with aiosqlite.connect("./prime.db") as db:
        for line in bs.select(target.selector):
            news = datamodels.ScrapedNews()
            news.title = line.get_text()
            news.time = datetime.datetime.now().isoformat()
            news.content = line['href']
            news.source = target.url
            out.append(news)
            send_webhook(news)
            await db.execute("INSERT INTO news VALUES (?, ?, ?, ?, ?)",
                             (news.time, news.title, news.content, news.thumbnail, news.source)
                             )
        await db.commit()
    return out


def send_webhook(news: datamodels.ScrapedNews):
    requests.post(utils.get_webhook_url(),
                  {"content": f"[{news.title}]({news.content})",
                   "name": f"News from [Tracked Site]({news.source})"
                   })