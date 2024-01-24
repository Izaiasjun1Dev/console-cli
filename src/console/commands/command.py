import logging
import datetime
from typing import List
from opensearchpy import OpenSearch
from pydantic import BaseModel, Field
from concurrent.futures import ThreadPoolExecutor
from boto3 import client
from console.config.cli_config import config
from console.config.open_search import ClientOpenSearh


class BaseCommand(BaseModel):
    name: str = Field(default="", description="Nome do comando")
    info: List[str | int] | str = Field(default=[], description="Argumentos do comando")
    parallel: int = Field(default=1, description="Número de processos paralelos")

    class Config:
        arbitrary_types_allowed = True
        
        
    @property
    def opensearch(self) -> OpenSearch:
        try:
            return ClientOpenSearh.client()
        except Exception as e:
            raise e
        
    @property
    def args(self) -> List[str | int]:
        try:
            # verifica se o info é um lista vazia
            if isinstance(self.info, list) and len(self.info) == 0:
                return []        
            
            informed_args = []
            for arg in self.info:
                if isinstance(arg, int):
                    informed_args.append(int(arg))
                else:
                    informed_args.append(str(arg))
                
            return informed_args
        except Exception as e:
            raise e
        
    @property
    def logger(self):
        logger_name = f"{__name__}.{self.name}.{self.__class__.__name__}"

        # Usa um logger compartilhado para evitar duplicatas
        if logger_name not in logging.Logger.manager.loggerDict:
            logger = logging.getLogger(logger_name)
            logger.setLevel(config.logger.level)
            formatter = logging.Formatter(config.logger.formater())
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logging.getLogger(logger_name)
    
    @property
    def aws(service_name: str) -> client:
        """
        Retorna um client do AWS
        """
        if config.environment == "DEVELOPMENT":
            return client(
                service_name=service_name,
                region_name=config.aws.region,
                aws_access_key_id=config.aws.aws_access_key_id,
                aws_secret_access_key=config.aws.aws_secret_access_key,
                endpoint_url=config.aws.endpoint_url,
            )
        
        return client(
            service_name=service_name,
            region_name=config.aws.region,
            aws_access_key_id=config.aws.aws_access_key_id,
            aws_secret_access_key=config.aws.aws_secret_access_key,
        )

        
    @classmethod
    def execute(cls):
        ...
            
    def _configure(self):
        pass
    
    def __hash__(self) -> int:
        return hash(f"{self.__class__.__name__}-{datetime.datetime.now()}")
    
    def _execute(self):
        # executa o metodo execute em paralelo ou não
        try:
            if self.parallel > 1:
                with ThreadPoolExecutor(max_workers=self.parallel) as executor:
                    futures = [executor.submit(self.execute) for _ in range(self.parallel)]
                    # Aguarda a conclusão de todas as execuções
                    for future in futures:
                        future.result()
            else:
                self.execute()
        except Exception as e:
            raise e
        