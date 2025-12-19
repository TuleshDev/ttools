import re
import subprocess
from pathlib import Path

regex_git = re.compile(
    r'<!--\s*snippet:([0-9a-f]+):([^:#]+)(?::([a-zA-Z0-9_-]+))?(?:#L(\d+)-L(\d+))?\s*-->([\s\S]*?)<!--\s*snippet:end\s*-->',
    re.IGNORECASE
)

regex_inline = re.compile(
    r'<!--\s*snippet:([a-zA-Z0-9_-]+)\s*-->([\s\S]*?)<!--\s*snippet:end\s*-->',
    re.IGNORECASE
)

def get_language(file: str) -> str:
    ext = Path(file).suffix.lower()
    return {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.vue': 'vue',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.html': 'html',
        '.css': 'css',
        '.sh': 'bash',
    }.get(ext, '')

def number_code(code: str, start: int = 1) -> str:
    lines = code.strip('\n').splitlines()
    return "\n".join(f"{i+start}\t{line}" for i, line in enumerate(lines))

def get_label_lang(file_name: str) -> str:
    return 'ru' if file_name.lower().endswith('.ru.md') else 'en'

def get_remote_url() -> str | None:
    try:
        url = subprocess.check_output(["git", "remote", "get-url", "origin"], text=True).strip()
        return url
    except subprocess.CalledProcessError:
        return None

def make_permalink(remote_url: str, commit: str, file: str, start: str, end: str) -> str | None:
    if "github.com" in remote_url:
        base = remote_url.rstrip(".git")
        link = f"{base}/blob/{commit}/{file}"
        if start and end:
            link += f"#L{start}-L{end}"
        return link
    elif "gitlab.com" in remote_url:
        base = remote_url.rstrip(".git")
        link = f"{base}/-/blob/{commit}/{file}"
        if start and end:
            link += f"#L{start}-{end}"
        return link
    elif "bitbucket.org" in remote_url:
        base = remote_url.rstrip(".git")
        link = f"{base}/src/{commit}/{file}"
        if start and end:
            link += f"#lines-{start}:{end}"
        return link
    return None

def make_label(commit: str, file: str, start: str, end: str, lang: str, remote_url: str | None) -> str:
    if lang == 'ru':
        text = f"Из коммита `{commit}`, файл `{file}`"
        if start and end:
            text += f", строки {start}–{end}"
    else:
        text = f"From commit `{commit}`, file `{file}`"
        if start and end:
            text += f", lines {start}–{end}"

    if remote_url:
        permalink = make_permalink(remote_url, commit, file, start, end)
        if permalink:
            return f"> [{text}]({permalink})"
    return f"> {text}"

def expand_snippets(path_dir: str = ".", blanks_dir: str | None = None, add_line_numbers: bool = True) -> None:
    absPath = Path(path_dir).resolve()
    blanks_path = Path(blanks_dir).resolve() if blanks_dir else absPath / "Blanks"

    if not blanks_path.exists():
        raise FileNotFoundError(f"Blanks directory not found: {blanks_path}")

    remote_url = get_remote_url()

    files = [f for f in blanks_path.iterdir() if f.is_file() and re.match(r'^readme(\..+)?\.md$', f.name, re.IGNORECASE)]

    for template_file in files:
        target_file = absPath / template_file.name
        label_lang = get_label_lang(template_file.name)

        text = template_file.read_text(encoding="utf-8")

        def replacer_git(match: re.Match) -> str:
            commit, path_file, lang_override, start, end, _ = match.groups()
            content = subprocess.check_output(["git", "show", f"{commit}:{path_file}"], text=True)
            lines = content.splitlines()

            if start and end:
                start, end = int(start), int(end)
                snippet_lines = lines[start-1:end]
                numbered = number_code("\n".join(snippet_lines), start=start) if add_line_numbers else "\n".join(snippet_lines)
            else:
                numbered = number_code("\n".join(lines)) if add_line_numbers else "\n".join(lines)

            lang = lang_override or get_language(path_file)
            label = make_label(commit, path_file, start, end, label_lang, remote_url)
            snippet = f"```{lang}\n{numbered}\n```"

            # return f"<!-- snippet:{commit}:{path_file}{f':{lang_override}' if lang_override else ''}{f'#L{start}-L{end}' if start and end else ''} -->\n{label}\n\n{snippet}\n<!-- snippet:end -->"
            return f"{label}\n\n{snippet}\n"

        text = regex_git.sub(replacer_git, text)

        def replacer_inline(match: re.Match) -> str:
            lang, code = match.groups()
            numbered = number_code(code) if add_line_numbers else code.strip('\n')
            snippet = f"```{lang}\n{numbered}\n```"
            # return f"<!-- snippet:{lang} -->\n{snippet}\n<!-- snippet:end -->"
            return f"{snippet}\n"

        text = regex_inline.sub(replacer_inline, text)

        target_file.write_text(text, encoding="utf-8")
        print(f"Updated: {target_file}")
