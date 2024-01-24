
# comandos para o dia a dia de desenvolvimento

# cores
RED=\033[0;31m
GREEN=\033[0;32m
NC=\033[0m # No Color
YELLOW=\033[0;33m

# funação para criar o arquivo de env
define create_env
	@echo "${YELLOW}criando arquivo de env 🏂${NC}"
	@cat devtools/envs/dev.txt > .env
	@echo "${GREEN}Variaveis setadas! 👌${NC}"
endef


define clean
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "*.log" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".pytest_cache" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -f .coverage.NB-SBDEV*
	@rm -rf htmlcov/
	@rm -f coverage.xml
	@rm -f *.log
	@rm -f celerybeat-schedule.bak
	@rm -f celerybeat-schedule.dat
	@rm -f celerybeat-schedule.dir
	@rm -f celerybeat-schedule
	@rm -f celerybeat-schedule.db
endef


env:
	@clear
	$(call create_env)

clear:
	@clear
	$(call clean)

build:
	@clear
	@./scripts/build.sh

up:
	@clear
	@cd docker && docker-compose up -d

down:
	@clear
	@cd docker && docker-compose down

freeze:
	@clear
	@pipenv requirements --dev > devtools/requirements/dev.txt

tag:
	@clear
	@echo "${YELLOW}criando tag git 🏂${NC}"
	@echo "${GREEN}Digite a tag:${NC}"
	@read tag; \
	git tag -a $$tag -m "versao $$tag"; \
	git push origin $$tag

#faz um push force para a ultima tag criada
tag-last:
	@clear
	@echo "${YELLOW}fazendo push force para a ultima tag criada 🏂${NC}"
	@git push --force origin $(shell git describe --abbrev=0 --tags)

# exclui todas as tags e atualia o remoto
tag-delete:
	@clear
	@echo "${YELLOW}excluindo todas as tags e atualizando o remoto 🏂${NC}"
	@git tag -l | xargs -n 1 git push --delete origin
	@git tag -l | xargs git tag -d


