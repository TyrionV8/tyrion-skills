---
name: limpeza-final-segura
description: Acione quando o usuário mencionar $limpeza-final-segura em qualquer parte do pedido, inclusive junto com outras skills ou comandos. Limpe com segurança rascunhos, backups e arquivos auxiliares criados na tarefa.
---

# Limpeza final segura

Esta skill é complementar à tarefa principal. A menção a `$limpeza-final-segura` em qualquer parte do pedido é suficiente para aplicá-la; não exija uma frase como "use esta skill". Sem essa menção, não a aplique.

Ao longo da tarefa, registre os caminhos dos arquivos que você próprio criar e identifique quais são finais, temporários, backups ou ainda necessários para execução, testes e recuperação. Inclua arquivos gerados por comandos, testes e editores.

Antes de remover qualquer arquivo, confirme sua origem e seu uso atual. Verifique se o resultado final continua íntegro e utilizável sem ele, por teste funcional quando possível. Se não for possível testar, faça uma inspeção concreta do conteúdo, das referências e das dependências pertinentes. Registre a limitação e a evidência usada. Não apague a única cópia de dados necessários para recuperação.

Remova automaticamente os arquivos auxiliares e backups criados por você nesta tarefa quando os testes ou a inspeção indicarem que não são mais necessários. Use caminhos específicos e limite a remoção aos arquivos identificados. Não trate arquivos preexistentes, alterações do usuário ou arquivos de origem incerta como lixo. Se houver dúvida concreta sobre propriedade, necessidade ou efeito da remoção, apresente os caminhos exatos e pergunte ao usuário antes de agir.

Ao concluir, informe os arquivos finais mantidos, os auxiliares e backups removidos, a verificação realizada e qualquer item cuja remoção dependa de decisão do usuário.
