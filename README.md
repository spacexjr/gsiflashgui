GSI Flasher com Deleção de Partição Product
Descrição
Ferramenta gráfica (GUI) em Python para facilitar o flash de imagens GSI compactadas em .xz.
Ela extrai o arquivo .xz, flashea a imagem na partição system do dispositivo via fastboot e permite apagar a partição product com um botão.

Funcionalidades
Seleção de arquivo .xz contendo a imagem GSI

Extração automática do arquivo .xz para .img

Flash da imagem .img na partição system via fastboot

Opção para apagar a partição lógica product usando fastboot delete-logical-partition product

Log em tempo real dos comandos e respostas

Pré-requisitos
Python 3.8 ou superior

fastboot instalado e disponível no PATH do sistema

Bootloader do dispositivo desbloqueado

Drivers ADB/Fastboot instalados no computador

Arquivo GSI compactado no formato .xz

Como usar
Instale o Python: https://www.python.org/downloads/

Certifique-se que o fastboot está instalado e configurado no PATH

Salve o script flash_gsi.py

Execute o script:

bash
Copiar
Editar
python flash_gsi.py
Na interface, clique em Procurar e selecione o arquivo .xz do GSI

Clique em 🔁 Flashar GSI (em 'system') para extrair e flashear

Para apagar a partição product, clique em ❌ Apagar Partição Product

Acompanhe o log para ver a saída dos comandos

Observações
O dispositivo deve estar no modo fastboot e conectado via USB

O bootloader deve estar desbloqueado para permitir flash e deleção de partições
