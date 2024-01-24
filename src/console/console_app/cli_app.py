from typing import List
import typer
from colorama import Fore, Style
from console.config.cli_config import config
from console.commands.cmd import (
    exec_command,
    available_commands,
    process_multiple_arguments,
    create_project_structure,
) 

from console.commands.application import Application

app = Application()

@app.command()
def version():
    """
    Exibe a versão do console cli
    """
    typer.echo(
        f"{Fore.GREEN}{config.name}{Style.RESET_ALL} {Fore.BLUE}{config.version}{Style.RESET_ALL}"
    )


@app.command(
    name="start-project",
)
def start_project(
    path: str = typer.Option(
        "./",
        prompt="Caminho onde o projeto vai ficar",
        help="Caminho para o novo projeto",
        show_default=True,
    ),
    name: str = typer.Option(
        "commands-projeto",
        prompt="Nome do projeto",
        help="Nome do projeto",
        show_default=True,
    ),
    description: str = typer.Option(
        "Novo projeto",
        prompt="Descrição do projeto",
        help="Descrição do projeto",
        show_default=True,
    )
):
    """
    Cria um novo projeto
    """
    try:
        create_project_structure(
            path,
            name,
            description,
        )
    except Exception as e:
        typer.echo(f"{Fore.RED}{e}{Style.RESET_ALL}")
        raise typer.Exit(code=1)

        
@app.command()
def run(
    info: str = typer.Option(
        "",
        help="Argumentos do comando",
        callback=lambda value: process_multiple_arguments(value)
    ),
    command: str = typer.Option(..., help="Nome do comando"),
    parallel: int = typer.Option(1, help="Número de processos paralelos"),
):
    """
    Executa um comando
    """
    try:
        if command not in available_commands(command):
            typer.echo(
                f"{Fore.YELLOW}Comando não encontrado: {Style.RESET_ALL}{Fore.RED}{command}{Style.RESET_ALL}\n"
            )
            available_commands()
            raise typer.Exit(code=1)
        
        command = command.replace("-", "_")
        exec_command(
            command,
            info,
            parallel,
        )
        
    except Exception as e:
        app.logger.error(e)
        raise typer.Exit(code=1)