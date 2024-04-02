import asyncio
from dataclasses import dataclass
from typing import Annotated, Optional, Any, Iterable

import aiohttp
import typer
from aiohttp import ClientSession

REDDIT_URL = "https://www.reddit.com"
DEFAULT_SUBS = ["rust", "python", "programming", "math"]


@dataclass
class Post:
    title: str
    score: int
    link: str
    permalink: str

    def __repr__(self) -> str:
        lines = [
            f"{self.score:>6}: {self.title}",
            f"{'':>8}  Discussion: {REDDIT_URL + self.permalink}",
        ]
        if self.permalink not in self.link:
            lines.append(f"{'':>8}  Link: {'':>6}{self.link}")
        return "\n".join(lines)


@dataclass
class Sub:
    name: str
    posts: list[Post]

    def __repr__(self) -> str:
        return self.name.title() + "\n" + "\n".join(str(post) for post in self.posts)


async def get_json(session: ClientSession, url: str) -> Any:
    async with session.get(url) as response:
        assert response.status == 200
        return await response.json()


async def get_top_posts(sub: str, session: ClientSession, limit: int) -> Sub:
    json_dict = await get_json(
        session, f"{REDDIT_URL}/r/{sub}/top.json?sort=top&t=day&limit={limit}"
    )
    return Sub(
        name=sub,
        posts=[
            Post(
                title=data["title"],
                score=data["score"],
                link=data["url"],
                permalink=data["permalink"],
            )
            for child in json_dict["data"]["children"]
            for data in [child["data"]]
        ],
    )


async def print_top_posts(sub_names: Iterable[str], limit=5) -> None:
    async with aiohttp.ClientSession() as session:
        tasks = (get_top_posts(name, session, limit) for name in sub_names)
        subs = await asyncio.gather(*tasks)
        for sub in sorted(subs, key=lambda t: t.name):
            print(sub)


def run(
    subs: Annotated[Optional[list[str]], typer.Argument()] = None,
    n_results: Annotated[int, typer.Option("-n")] = 5,
):
    """
    Retrieves top posts for given subs.
    """
    if subs is None:
        subs = DEFAULT_SUBS
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_top_posts(subs, n_results))


def main():
    typer.run(run)


if __name__ == "__main__":
    main()
