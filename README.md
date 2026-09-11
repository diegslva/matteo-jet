# Matteo & Jet — Aventuras Além do Mar

Jogo de aventura para celular. Versão preparada para publicação: **0.3.1**, build **011d14ddf250**.

## Estado da publicação

Este repositório está sendo preparado para receber o pacote do jogo. A presença deste README **não significa que o jogo já esteja publicado**. A publicação só estará concluída após o envio do pacote, a configuração do Pages e uma execução bem-sucedida do workflow **Publicar Matteo e Jet**.

## Primeira publicação

1. Em **Settings → Pages → Build and deployment → Source**, selecione **GitHub Actions**.
2. Na aba **Code → Add file → Upload files**, envie o arquivo **Matteo_Jet_GitHub_Pages_v0.3.1.zip** fornecido na conversa para a raiz da branch `main` e confirme o commit. Neste fluxo, **envie o ZIP fechado**: a automação extrai os arquivos. Não envie o ZIP da codebase completa.
3. Acompanhe **Actions → Publicar Matteo e Jet**. Após a implantação bem-sucedida, use **Settings → Pages → Visit site**.

Endereço esperado após a publicação: <https://diegslva.github.io/matteo-jet/>.

Se o primeiro envio ocorrer antes de ativar Pages, ative-o e execute **Actions → Publicar Matteo e Jet → Run workflow** na branch `main`.

## O que é publicado

Somente o HTML autocontido, o manifest, o service worker, os ícones, os metadados de build e o marcador `.nojekyll`. Os assets da versão aprovada já estão incorporados ao HTML. A automação valida os arquivos antes de prepará-los e não executa código extraído do ZIP.

O pacote de publicação não substitui a codebase completa. Guarde também `Matteo_Jet_Projeto_v0.3.1.zip` para manutenção e desenvolvimento.

## Atualizações

Cada versão tem nome de pacote e hashes registrados em `deployment.json`. Para atualizar, revise esse manifesto e envie o pacote correspondente. O workflow preserva os bytes da entrega: não refaz as artes nem muda as regras do jogo.

## Privacidade e validação

O destino é público e contém as ilustrações da família cuja publicação foi autorizada nesta conversa. Não envie fotografias originais, credenciais, histórico `.git`, relatórios locais ou outros arquivos da sua máquina.

A música da versão 0.1.4 foi confirmada pelo proprietário em Chrome/Android; isso não equivale a um teste do Safari/iPhone ou de todas as versões posteriores. Testes locais e os requisitos da publicação são documentados separadamente; uma publicação bem-sucedida também não substitui testes em aparelho físico.

Documentação oficial: [GitHub Pages com workflows personalizados](https://docs.github.com/pt/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
