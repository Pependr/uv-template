# @https://raw.githubusercontent.com/Pependr/uv-template/refs/heads/master/covplugin.py
import honk
import click

import json
import itertools

from collections.abc import Mapping, Callable, Sequence


type Input = Mapping[str, Mapping[str, Sequence[int]]]


def group_by[T](
    items: Sequence[T], key: Callable[[T, T], bool]
) -> list[list[T]]:
    if len(items) == 0:
        return []

    result: list[list[T]] = [[]]

    for a, b in itertools.pairwise(items):
        result[-1].append(a)
        if not key(a, b):
            result.append([])

    result[-1].append(items[-1])

    return result


def compress(items: Sequence[int]) -> str:
    if len(items) > 1:
        return f"{items[0]}-{items[-1]}"
    return str(items[0])


@honk.template("group", help="Group sequences of numbers in chosen fields")
@click.option("-i", "--include", multiple=True)
def _(data: Input, include: tuple[str, ...]) -> None:
    def pipe(items: Sequence[int]) -> str:
        return ", ".join(
            map(compress, group_by(items, lambda a, b: b - a == 1))
        )

    click.echo(
        json.dumps(
            {k: {key: pipe(v[key]) for key in include} for k, v in data.items()}
        )
    )
