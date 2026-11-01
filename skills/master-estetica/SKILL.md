---
name: master-estetica
description: Consulta e reutiliza padrões estéticos pré-aprovados para gerar imagens do Master e registra o padrão visual de uma campanha. Use ao pedir Livro de Mapas, padrões estéticos salvos, imagens no estilo de uma campanha ou atribuição de um estilo à campanha.
---

# Master — Padrões estéticos

Biblioteca pessoal: `/home/davi/repos/agentes/master/padroes-esteticos`.
Leia `catalogo.json` para descobrir os padrões disponíveis; não dependa de uma lista copiada nesta skill. Cada entrada aponta para a ficha e as referências visuais do padrão. Leia a ficha e visualize as referências antes de gerar uma imagem.

## Escolher e gerar

- Um padrão citado explicitamente no pedido vale para aquela geração. Isso não altera o padrão atribuído à campanha.
- Para “o estilo desta campanha”, consulte a campanha real pela skill `master-ai-assist` e procure seu identificador em `vinculos-campanhas.json`. Resolva o identificador atual, sem reutilizar nomes ou identificadores de outro chat.
- Se não houver padrão explícito nem vínculo, apresente os padrões cadastrados e esclareça a escolha. Não registre uma preferência por inferência.
- Combine a ficha estética com os requisitos do cenário. Use a ferramenta de geração de imagens disponível e as imagens salvas como referências, conforme as instruções da ferramenta. Preserve a distinção entre estilo artístico e disposição do cenário.
- Em pedidos de estilos diferentes, mantenha o conteúdo e a composição semelhantes para comparar traço, cores, textura e simplificação. Em pedidos de variação de cenário, preserve o estilo escolhido.
- Para mapas locais, respeite as dimensões e a escala atuais. As referências aprovam a estética; suas grades ilustrativas não comprovam encaixe exato. Não declare alinhamento verificado apenas porque o gerador desenhou uma grade. Para fundos a importar, prefira imagem sem grade embutida e a grade lógica do Master, salvo pedido diferente.
- Mostre o resultado no chat. Gerar uma imagem não autoriza importá-la, aplicá-la ao mapa ou projetá-la; faça essas operações somente quando pedidas, seguindo `master-ai-assist`.

## Atribuir a uma campanha

Um pedido como “atribua Livro de Mapas a esta campanha” autoriza o vínculo local. Consulte a campanha atual e o catálogo, leia `vinculos-campanhas.json`, preserve as outras entradas e grave apenas o vínculo solicitado. Use uma escrita atômica e releia para verificar.

A chave é o identificador real da campanha. Cada entrada contém `nome_campanha`, `padrao_id`, `escopo` e `atualizado_em` (data no formato ano-mês-dia). Use somente o escopo coberto pela ficha; para o Livro de Mapas, `mapas_locais_quadriculados`. Um pedido explícito de imagem pode adaptar a estética a outro formato sem ampliar o vínculo automaticamente.

O vínculo é uma preferência da biblioteca pessoal lida pelos agentes, não uma configuração gravada dentro do Master. Informe isso ao registrar. Para desvincular ou trocar, altere somente a entrada indicada e verifique o arquivo novamente. Não altere o banco nem o código da aplicação.

## Cadastrar padrões

Registre somente os padrões que o usuário pedir para guardar. Crie uma pasta com nome estável, ficha `PADRAO.md` e imagens em `referencias/`; acrescente a entrada em `catalogo.json`. A ficha deve distinguir a aprovação da estética de eventuais limites de uso. Preserve os originais e não substitua referências aprovadas por novas gerações silenciosamente.

## Exemplos

- “Gere uma ruína no padrão Livro de Mapas.”
- “Mostre os padrões estéticos salvos.”
- “Atribua Livro de Mapas à campanha atual.”
- “Gere uma taverna usando o padrão desta campanha.”
