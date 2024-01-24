from enum import Enum
from colorama import Fore, Style
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field, BaseModel


class Environment(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    TESTING = "TESTING"
    PRODUCTION = "PRODUCTION"
    
class ExitCode(Enum):
    SUCCESS = 0
    ERROR = 1
    FAILURE = 2
    NOT_IMPLEMENTED = 3
    NOT_FOUND = 4
    INVALID_INPUT = 5
    INVALID_OUTPUT = 6
    INVALID_CONFIG = 7
    INVALID_STATE = 8
    INVALID_OPERATION = 9    
    
class AwsConfig(BaseModel):
    aws_access_key_id: str = Field(default="teste")
    aws_secret_access_key: str = Field(default="teste")
    region: str = Field(default="us-east-1")
    endpoint_url: str = Field(default="http://localhost:4566")

class CmdConfig(BaseModel):
    commands_path: str = Field(default="commands")
    
class LoggerConfig(BaseModel):
    level: str = Field(default="INFO")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    datefmt: str = Field(default="%d-%b-%y %H:%M:%S")
    
    def formater(self, worker_name: str = f"{__name__}"):
        if config.environment == Environment.DEVELOPMENT:
            return f"{Fore.GREEN}%(asctime)s{Style.RESET_ALL} - {Fore.BLUE}%(name)s{Style.RESET_ALL} - {Fore.YELLOW}%(levelname)s{Style.RESET_ALL} - %(message)s"
        
        return self.format
    
class OpenElasticConfig(BaseModel):
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=9200)
    scheme: str = Field(default="http")
    user: str = Field(default="admin")
    password: str = Field(default="admin")
    use_ssl: bool = Field(default=True)
    verify_certs: bool = Field(default=False)
    ssl_assert_hostname: bool = Field(default=False)
    ssl_show_warn: bool = Field(default=False)
    
    def get_url(self):
        return f"{self.scheme}://{self.host}:{self.port}"
    
    def get_auth(self) -> tuple[str, str]:
        
        return (self.user, self.password)
    
    
class Application(BaseSettings):
    environment: Environment = Field(default=Environment.DEVELOPMENT)
    name: str = Field(default="Console", env="APPLICATION_NAME")
    version: str = Field(default="0.0.1", env="APPLICATION_VERSION")
    cmd: CmdConfig = Field(default=CmdConfig())
    logger: LoggerConfig = Field(default=LoggerConfig())
    open_elastic: OpenElasticConfig = Field(default=OpenElasticConfig())
    exit_code: ExitCode = Field(default=ExitCode.SUCCESS)
    aws: AwsConfig = Field(default=AwsConfig())
   
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


load_dotenv(verbose=True)

config = Application()