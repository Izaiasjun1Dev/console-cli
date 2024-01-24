import os
import typer
import shutil
from os import listdir
from colorama import Fore, Style
from console.console_app.utils import fromcwd
from importlib.util import (
    module_from_spec, spec_from_file_location
)
from console.config.cli_config import config



def create_project_structure(path: str, name: str, description: str):
    """
    Args:
    - path (str): Caminho para a pasta onde o projeto será criado.
    - name (str): Nome do projeto.
    - description (str): Descrição do projeto.
    
    Raises:
    - FileExistsError: Se o diretório do projeto já existir.
    - Exception: Se ocorrer um erro desconhecido durante a criação do projeto.
    """

    
    try:
        # pega o root path do projeto
        commands_dir = os.path.dirname(__file__)
        templates_dir = os.path.join(commands_dir, "../templates/new_project")
        
        for i in os.listdir(templates_dir):
            print(i)

    except Exception as e:
        # Log de erro desconhecido
        raise e
    
def process_multiple_arguments(value: str):
    """
    Processa argumentos múltiplos
    """
    if value is None or value == "":
        return []
    
    return value.split(",") \
        or value.split(" ") \
            or value.split(", ")


def available_commands(command_name: str = None):
    """
    retorna os comandos disponíveis
    caso o command_name seja != de None, retorna apenas true caso ele seja encontrado
    """
    commands = listdir(fromcwd(config.cmd.commands_path))
    
    if command_name is not None:
        return [
            command.replace(".py", "")
            .replace("_", "-") for command in commands
        ]
    
    typer.echo(f"{Fore.CYAN}Comandos disponíveis:{Style.RESET_ALL}\n")
    for idx, command in enumerate(commands, start=1):
        typer.echo(f"{idx}. {Fore.GREEN}{command.replace('.py', '').replace('_', '-')}{Style.RESET_ALL}\n")
    
    
def exec_command(
    command_name: str,
    info: list = [],
    parallel: int = 1,
):
    """
    Executa um comando
    """
    try:
        module_name = f"{config.cmd.commands_path}/{command_name}.py"
        
        spec = spec_from_file_location(
            module_name,
            module_name
        )
        
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        
        from console.commands.command import BaseCommand
        
        command: BaseCommand = getattr(
            module, 
            "Command"
        )(
            name=command_name, 
            info=info, 
            parallel=parallel
        )
        

        command._execute()
        
    except Exception as e:
        raise e
        
        