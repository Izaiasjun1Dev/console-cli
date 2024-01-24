#bin/bash

# Instalar o módulo build no ambiente virtual
pipenv install build

# Construir o pacote
python -m build .

# Desinstalar a versão anterior do pacote (se existir)
pip3 uninstall -y console

# Encontrar o arquivo Wheel mais recente
path_to_file=$(find dist -type f -name "*.whl" | sort -V | tail -n 1)

# Verificar se o arquivo Wheel foi encontrado
if [ -z "$path_to_file" ]; then
  echo "Erro: Nenhum arquivo Wheel encontrado na pasta dist."
  exit 1
fi

# Instalar o pacote mais recente
pip install --ignore-installed --no-cache-dir -U "$path_to_file"

# Verificar se a instalação foi bem-sucedida
if [ $? -ne 0 ]; then
  echo "Erro: Falha ao instalar o pacote."
  exit 1
fi

# Testar a importação do pacote
if ! python -c "import console"; then
  echo "Erro: Falha ao importar o pacote."
  exit 1
fi

# Testar o script console
console --help

# Limpar variáveis
unset path_to_file
