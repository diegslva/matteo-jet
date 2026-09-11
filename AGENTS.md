# Matteo & Jet — repositório de publicação

Leia README.md, deployment.json, scripts/prepare_pages.py, Makefile e .github/workflows/pages.yml antes de modificar a publicação.

- Este repositório distribui o pacote aprovado; não reconstrói nem refatora o jogo.
- Preserve os bytes do HTML e dos assets. Alterações de jogabilidade pertencem à codebase completa.
- Use `make check` para testar e preparar o site; não publique se a validação falhar.
- Mantenha somente os oito arquivos públicos permitidos em `_site/`. Nunca publique `.git`, credenciais ou arquivos privados.
- Não execute código contido no ZIP recebido; valide nomes, hashes, tamanhos e metadados antes da extração.
- Mantenha versões do jogo, build de conteúdo e versão da ferramenta de publicação separados.
- Preserve erros, causa e stack trace. Logs devem ser estruturados e não conter segredos.
- Mantenha permissões mínimas por job e actions oficiais fixadas por SHA verificado.
- Não remova proteções do repositório, não altere sua visibilidade e não solicite tokens no chat.
- Diferencie preparação local, commit remoto, execução do workflow e site publicado. Só afirme publicação após verificar o deploy.
