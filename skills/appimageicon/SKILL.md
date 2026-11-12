---
name: appimageicon
description: Garante a exibição correta e persistente de ícones em AppImages no Linux (especialmente Cinnamon, GNOME e Muffin) através do caminho absoluto no arquivo .desktop, sincronização de StartupWMClass e auto-registro dinâmico de localização via $APPIMAGE. Use sempre que for criar, empacotar, atualizar ou diagnosticar um AppImage ou resolver ícones ausentes/invisíveis na barra de tarefas do sistema.
---

# AppImageIcon — Ícones Robustos para AppImages no Linux

Esta habilidade orienta como garantir que um aplicativo empacotado como **AppImage** exiba sempre seu ícone correto no menu de aplicativos e na barra de tarefas / dock do Linux (especialmente Cinnamon, GNOME Shell, XFCE e Muffin), sem que o ícone fique transparente, invisível ou como uma engrenagem genérica, e sem quebrar quando o usuário move o arquivo `.AppImage` para outra pasta.

---

## 1. O Problema Raiz no Linux Desktop

Em desktops baseados em GTK e Mutter/Muffin (como Cinnamon no Linux Mint e GNOME no Ubuntu/Debian), os gerenciadores de janelas e applets de lista de janelas agrupadas (`grouped-window-list`) associam janelas em execução ao seu ícone através de dois elos:
1. **Identificação da Janela (`WM_CLASS`)**: o applet compara a classe da janela (`StartupWMClass` ou o nome do `.desktop`) com os arquivos `.desktop` registrados em `~/.local/share/applications/` e `/usr/share/applications/`.
2. **Resolução do Ícone (`Icon=`)**: quando o `.desktop` declara apenas um nome curto de tema (ex.: `Icon=meu-app`), o tema GTK ativo tenta localizá-lo em `~/.icons/` ou `/usr/share/icons/`. Se o ícone não fizer parte do pacote do tema global instalado, a resolução retorna **`NONE`**, resultando em um espaço vazio/invisível na barra de tarefas.
3. **Movimentação do AppImage**: quando o usuário move o executável `.AppImage` para outra pasta (ex.: de `dist/` para `~/Applications/` ou `~/Desktop`), caminhos fixos de `Exec=` deixam de coincidir e a associação se perde.

---

## 2. A Solução Canônica em 3 Camadas

Toda vez que criar ou atualizar um AppImage, implemente esta arquitetura:

```
┌────────────────────────────────────────────────────────┐
│ AppImage em Execução                                   │
│  ├─ 1. Runtime injeta $APPIMAGE com o caminho atual     │
│  ├─ 2. Binário extrai SVG para diretório canônico local │
│  └─ 3. Atualiza ~/.local/share/applications/<id>.desktop│
└────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ Arquivo .desktop com Caminho Absoluto Direto           │
│  Exec="<caminho_real_de_$APPIMAGE>" %F                 │
│  Icon=/home/usuario/.local/share/icons/.../<id>.svg     │
│  StartupWMClass=<id>                                   │
└────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ Cinnamon / GNOME / Muffin / Wnck                       │
│  Lê o SVG diretamente do disco sem falha de tema GTK!  │
└────────────────────────────────────────────────────────┘
```

---

## 3. Implementação Prática

### Passo A: No Código-Fonte da Aplicação (Auto-integração na Inicialização)

Adicione uma rotina executada logo no início da função `main()`. Ela garante a existência do arquivo SVG e atualiza o lançador `.desktop` refletindo onde quer que o AppImage esteja rodando:

```rust
fn ensure_desktop_integration() {
    let Ok(home) = std::env::var("HOME") else { return };
    let icon_dir = std::path::PathBuf::from(&home).join(".local/share/icons/hicolor/scalable/apps");
    let icon_dest = icon_dir.join("<app_id>.svg");
    let _ = std::fs::create_dir_all(&icon_dir);

    // Garante o arquivo SVG no disco a partir dos bytes embutidos no binário
    let svg_bytes = include_bytes!("../assets/icon.svg");
    if !icon_dest.exists() || icon_dest.metadata().map(|m| m.len() == 0).unwrap_or(true) {
        let _ = std::fs::write(&icon_dest, svg_bytes);
    }

    // $APPIMAGE contém o caminho real do arquivo .AppImage executado pelo usuário
    let actual_exe = std::env::var("APPIMAGE")
        .map(std::path::PathBuf::from)
        .or_else(|_| std::env::current_exe())
        .unwrap_or_else(|_| std::path::PathBuf::from("<app_id>"));

    let apps_dir = std::path::PathBuf::from(&home).join(".local/share/applications");
    let _ = std::fs::create_dir_all(&apps_dir);
    let desktop_file = apps_dir.join("<app_id>.desktop");

    let desktop_content = format!(
        "[Desktop Entry]\n\
         Name={name}\n\
         Comment={comment}\n\
         Exec=\"{}\" %F\n\
         Icon={}\n\
         Type=Application\n\
         Categories=AudioVideo;Audio;Utility;\n\
         Terminal=false\n\
         StartupWMClass=<app_id>\n",
        actual_exe.display(),
        icon_dest.display()
    );

    if std::fs::read_to_string(&desktop_file).map(|s| s != desktop_content).unwrap_or(true) {
        let _ = std::fs::write(&desktop_file, &desktop_content);
        let _ = std::process::Command::new("update-desktop-database")
            .arg(&apps_dir)
            .status();
    }
}
```

> [!IMPORTANT]
> O segredo principal é a linha `Icon={}` receber o **caminho absoluto** até o arquivo SVG (ex.: `/home/usuario/.local/share/icons/hicolor/scalable/apps/<app_id>.svg`), e **nunca** apenas um nome sem barra (`Icon=<app_id>`).

### Passo B: No Script de Construção do AppImage (`build_appimage.sh`)

Na estrutura interna do `AppDir`:
1. Copie o arquivo SVG original para a raiz do `AppDir` como `<app_id>.svg`.
2. Gere ou copie um ícone para `.DirIcon` (usado por gerenciadores de arquivos para miniaturas).
3. Crie o arquivo `<app_id>.desktop` com a propriedade `StartupWMClass=<app_id>`:

```bash
# Estrutura do AppDir
cp "assets/icon.svg" "$APPDIR/<app_id>.svg"
cp "assets/icon.svg" "$APPDIR/usr/share/icons/hicolor/scalable/apps/<app_id>.svg"
cp "assets/icon_256.png" "$APPDIR/.DirIcon" 2>/dev/null || cp "$APPDIR/<app_id>.svg" "$APPDIR/.DirIcon"

cat > "$APPDIR/<app_id>.desktop" <<EOF
[Desktop Entry]
Name=NomeDoApp
Exec=<binario_interno>
Icon=<app_id>
Type=Application
Categories=Utility;
Terminal=false
StartupWMClass=<app_id>
EOF

# Após gerar o .AppImage final, atualize também o lançador local do host:
cat > "$HOME/.local/share/applications/<app_id>.desktop" <<EOF
[Desktop Entry]
Name=NomeDoApp
Exec=$OUT_APPIMAGE %F
Icon=$HOME/.local/share/icons/hicolor/scalable/apps/<app_id>.svg
Type=Application
Categories=Utility;
Terminal=false
StartupWMClass=<app_id>
EOF
update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
```

---

## 4. Script de Auditoria e Diagnóstico Rápido

Para conferir imediatamente se o sistema está encontrando o ícone ou retornando `NONE`, execute este comando no terminal:

```bash
python3 -c '
import gi
gi.require_version("Gio", "2.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gio, Gtk

desktop_file = "/home/'"$USER"'/.local/share/applications/<app_id>.desktop"
app = Gio.DesktopAppInfo.new_from_filename(desktop_file)
if not app:
    print("ERRO: Arquivo desktop não encontrado:", desktop_file)
    exit(1)

icon = app.get_icon()
print("Icon declarado:", icon.to_string() if icon else "NENHUM")
theme = Gtk.IconTheme.get_default()
resolved = theme.lookup_by_gicon(icon, 48, 0) if icon else None
print("Arquivo resolvido pelo tema GTK:", resolved.get_filename() if resolved else "NONE (ÍCONE FICARÁ INVISÍVEL!)")
'
```

- Se a saída for `NONE (ÍCONE FICARÁ INVISÍVEL!)`: o arquivo `.desktop` ainda está com nome temático curto sem caminho absoluto.
- Se a saída for o caminho do `.svg`: o Cinnamon/GNOME carregará o ícone na barra de tarefas perfeitamente.

---

## 5. Checklist de Verificação

- [ ] O binário tem o arquivo SVG embutido (`include_bytes!`) e garante sua extração para `~/.local/share/icons/...`.
- [ ] O arquivo `.desktop` usa `Icon=/caminho/absoluto/do/arquivo.svg`.
- [ ] A propriedade `StartupWMClass` no `.desktop` corresponde exatamente à classe da janela gerada pelo toolkit (`WM_CLASS`).
- [ ] O aplicativo lê `$APPIMAGE` ao iniciar para atualizar o `Exec=` caso o usuário tenha movido o arquivo `.AppImage` de diretório.
- [ ] O teste com `Gio.DesktopAppInfo` confirma que a resolução retorna o caminho do arquivo e não `NONE`.
