# Perfis visuais

Este arquivo guarda padrões por categoria de artefato. Apenas perfis explicitamente aprovados pelo usuário devem ser usados como padrões reutilizáveis. Aprovar uma aplicação isolada não aprova a inclusão ou alteração de um perfil.

## Perfis aprovados

### Terminal — azul vivo e ciano

Aprovado com base na terceira prévia de menu. Use para scripts e programas de terminal semelhantes. A referência visual está em [terminal-aprovado.html](../assets/terminal-aprovado.html); abra-a no navegador para consultar a aparência. É uma demonstração estática, não um menu executável.

As cores abaixo são referências hexadecimais (códigos de cor) da prévia aprovada. Adapte-as ao suporte e ao tema do terminal preservando contraste e funções; não altere a configuração global do terminal.

| Elemento | Tema escuro | Tema claro |
|---|---|---|
| Fundo | `#141b24` | `#f8fafc` |
| Texto principal | `#e2e8f0` | `#253244` |
| Títulos gerais | `#67dbe8` | `#006b7a` |
| Título do menu | `#20e4ff` | `#007285` |
| Nomes dos scripts | `#419dff` | `#075dcc` |
| Nome selecionado e título dos detalhes | `#63bcff` | `#064fc4` |
| Fundo da seleção | `#173956` | `#d9eaff` |
| Marcador da seleção | `#38c9ff` | `#005bc4` |
| Caminhos e comandos | `#91baff` | `#225db0` |
| Rótulos Diretório e Comando | `#ffb454` | `#854300` |
| Linha lateral dos detalhes | `#20d9ef` | `#00879a` |
| Texto secundário | `#a4b1c2` | `#586679` |
| Sucesso | `#8cdb9e` | `#24713c` |
| Aviso | `#edca79` | `#865b00` |
| Erro | `#ff929b` | `#b52b39` |

- Use azul vivo nos nomes do menu; o amarelo nessa função foi rejeitado. Evite cores apagadas nas opções.
- Use títulos destacados, separação entre seções e linhas compactas no formato nome — descrição. Destaque a seleção com fundo e marcador `❯`.
- Nos detalhes, mostre nome destacado, descrição, Diretório e Comando quando aplicáveis. Use o termo “Diretório”, não “Pasta”.
- Mensagens: `✓ Sucesso:`, `! Aviso:`, `✗ Erro:`; etapas com `◆`. Preserve texto e símbolos para que a informação não dependa só da cor.
- Respeite `NO_COLOR`, opção para desativar cores, e saída redirecionada. Não introduza códigos de cor em dados usados por outros programas. Adapte símbolos quando o ambiente não puder exibi-los.
- Preserve comandos, confirmações e comportamento aceito ao aplicar o perfil. Não adicione funções apenas para reproduzir os dados da demonstração.

## Outras categorias

Interfaces de programas, imagens e outros artefatos ainda não têm perfis aprovados. Proponha uma prévia pertinente ao caso e peça aprovação separada antes de guardar um novo padrão.

Ao registrar um perfil aprovado, descreva seu nome, categoria, situações de uso, cores e suas funções, regras de apresentação e adaptações necessárias ao meio. Registre escolhas concretas; não preencha propriedades sem aplicação ao perfil.
