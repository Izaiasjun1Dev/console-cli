from datetime import timedelta
from os import getcwd
from typing import Literal, overload

__all__ = [
    "fromcwd",
    "get_timing",
    "logger",
]

def fromcwd(path: str) -> str:
    """
    Retorna o caminho absoluto a partir do diretorio atual.
    params:
        path: str = caminho relativo a partir do diretorio atual

    raises:
        TypeError: se path nao for uma string

    returns: str = caminho absoluto

    exemplo de uso:
    ```

        path = fromcwd("sql/dql")

        print(path)

        >>> /home/user/project/sql/dql

    ```

    """

    return f"{getcwd()}/{path}"

@overload
def get_timing(timing_type: Literal["all"]) -> dict[str, timedelta]:
    ...