Instagram DM helper (app executável em modo seguro)
====================================================

Este app foi feito para quem **não programa**: você abre uma janela, escolhe o JSON,
informa o username da influenciadora e clica em um botão.

Modo seguro
-----------

* Não faz login no Instagram.
* Não envia mensagens automaticamente.
* Apenas analisa um histórico exportado e sugere uma resposta para revisão humana.

Formato do JSON
---------------

O arquivo de entrada deve conter uma lista de conversas:

.. code-block:: json

   [
     {
       "participant": "ana",
       "messages": [
         {"sender": "ana", "text": "Amei seus vídeos!", "timestamp": 1},
         {"sender": "saminho", "text": "Obrigada!", "timestamp": 2}
       ]
     }
   ]

Como abrir o app
----------------

Opção 1 (mais simples):

.. code-block:: bash

   ./executar_app_instagram.sh

Opção 2:

.. code-block:: bash

   python3 utils/instagram_dm_helper_app.py

Como usar
---------

1. Clique em **Selecionar arquivo** e escolha seu JSON.
2. Preencha o campo **Username da influenciadora** (ex.: ``saminho``).
3. (Opcional) informe uma semente aleatória para repetir o mesmo sorteio.
4. Clique em **Analisar conversa**.
5. Revise a sugestão e, se quiser, use **Salvar resposta em TXT**.

Comando único para gerar executável
-----------------------------------

Rode apenas este comando na raiz do projeto:

.. code-block:: bash

   ./gerar_exe_instagram.sh

Esse comando instala o PyInstaller automaticamente e gera o executável em ``dist/``
(com nome ``saminho_dm_helper`` ou ``saminho_dm_helper.exe``, dependendo do sistema).
