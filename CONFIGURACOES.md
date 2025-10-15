# Guia de Configurações

Este guia explica como configurar cores ANSI, sessão e auto-login no BarcaExpert.

## Onde ficam as configurações

- Arquivo `.env` na raiz do projeto.
- Algumas opções também podem ser alteradas pelo próprio sistema: Menu Principal → 7. Configurações (atalho F9).

## Variáveis do .env

```env
# Cores ANSI
ANSI_ENABLED=sim            # sim|nao — habilita cores no console
ANSI_HEADER_COLOR=yellow    # yellow|cyan|blue|green|red|magenta|white
ANSI_FOOTER_COLOR=cyan      # yellow|cyan|blue|green|red|magenta|white

# Sessão e Auto-login
AUTO_LOGIN=nao              # sim|nao — entra automaticamente com a última sessão salva
SESSION_USER=               # preenchido automaticamente no login
SESSION_USER_ID=            # preenchido automaticamente no login
SESSION_USER_LEVEL=         # preenchido automaticamente no login
```

## Como usar pelo sistema (recomendado)

1. Abra o sistema e vá em "Configurações" (F9 no Menu Principal).
2. Ajuste:
   - "ANSI Enabled" para ativar/desativar cores.
   - "ANSI Header Color" e "ANSI Footer Color" para personalizar cores.
   - "Auto Login" para habilitar o login automático.
3. Salve e retorne. As alterações são gravadas automaticamente no `.env`.

## Como funciona o Auto-login

- Ao fazer login, o sistema salva `SESSION_USER`, `SESSION_USER_ID` e `SESSION_USER_LEVEL` no `.env`.
- Se `AUTO_LOGIN=sim`, na próxima execução o sistema usa esses dados para entrar direto.
- Para desativar, mude `AUTO_LOGIN` para `nao` nas Configurações ou edite o `.env`.

## Dicas de Cores ANSI

- `ANSI_ENABLED=sim` ativa o cabeçalho com título em destaque e rodapés com atalhos coloridos.
- Ideal para monitores onde o contraste ajuda a leitura rápida.
- Se o terminal não renderizar cores corretamente, defina `ANSI_ENABLED=nao`.

## Perguntas Frequentes

- "Minhas cores não mudam": confirme `ANSI_ENABLED=sim` e que o terminal suporta ANSI.
- "Quero voltar às cores padrão": defina `ANSI_ENABLED=nao`.
- "Esqueci a sessão salva": defina `AUTO_LOGIN=nao` e faça login normalmente.


