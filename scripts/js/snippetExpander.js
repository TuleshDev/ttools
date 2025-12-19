import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

const regexGit = /<!--\s*snippet:([0-9a-f]+):([^:#]+)(?::([a-zA-Z0-9_-]+))?(?:#L(\d+)-L(\d+))?\s*-->([\s\S]*?)<!--\s*snippet:end\s*-->/gi;
const regexInline = /<!--\s*snippet:([a-zA-Z0-9_-]+)\s*-->([\s\S]*?)<!--\s*snippet:end\s*-->/gi;

function getLanguage(file) {
  const ext = path.extname(file).toLowerCase();
  switch (ext) {
    case '.py': return 'python';
    case '.js': return 'javascript';
    case '.ts': return 'typescript';
    case '.vue': return 'vue';
    case '.java': return 'java';
    case '.cpp': return 'cpp';
    case '.c': return 'c';
    case '.html': return 'html';
    case '.css': return 'css';
    case '.sh': return 'bash';
    default: return '';
  }
}

function numberCode(code, start = 1) {
  const lines = code.trimEnd().split('\n');
  return lines.map((line, i) => `${i + start}\t${line}`).join('\n');
}

function getLabelLang(fileName) {
  return fileName.toLowerCase().endsWith('.ru.md') ? 'ru' : 'en';
}

function getRemoteUrl() {
  try {
    return execSync('git remote get-url origin', { encoding: 'utf-8' }).trim();
  } catch {
    return null;
  }
}

function makePermalink(remoteUrl, commit, file, start, end) {
  if (remoteUrl.includes('github.com')) {
    const base = remoteUrl.replace(/\.git$/, '');
    let link = `${base}/blob/${commit}/${file}`;
    if (start && end) link += `#L${start}-L${end}`;
    return link;
  } else if (remoteUrl.includes('gitlab.com')) {
    const base = remoteUrl.replace(/\.git$/, '');
    let link = `${base}/-/blob/${commit}/${file}`;
    if (start && end) link += `#L${start}-${end}`;
    return link;
  } else if (remoteUrl.includes('bitbucket.org')) {
    const base = remoteUrl.replace(/\.git$/, '');
    let link = `${base}/src/${commit}/${file}`;
    if (start && end) link += `#lines-${start}:${end}`;
    return link;
  }
  return null;
}

function makeLabel(commit, file, start, end, lang, remoteUrl) {
  let text;
  if (lang === 'ru') {
    text = `Из коммита \`${commit}\`, файл \`${file}\``;
    if (start && end) text += `, строки ${start}–${end}`;
  } else {
    text = `From commit \`${commit}\`, file \`${file}\``;
    if (start && end) text += `, lines ${start}–${end}`;
  }

  if (remoteUrl) {
    const permalink = makePermalink(remoteUrl, commit, file, start, end);
    if (permalink) {
      return `> [${text}](${permalink})`;
    }
  }
  return `> ${text}`;
}

export function expandSnippets(pathDir = '.', blanksDir = null, addLineNumbers = true) {
  const absPath = path.resolve(pathDir);
  const blanksPath = blanksDir ? path.resolve(blanksDir) : path.join(absPath, 'Blanks');

  if (!fs.existsSync(blanksPath)) {
    throw new Error(`Blanks directory not found: ${blanksPath}`);
  }

  const remoteUrl = getRemoteUrl();

  const files = fs.readdirSync(blanksPath)
    .filter(f => /^readme(\..+)?\.md$/i.test(f));

  files.forEach(file => {
    const templateFile = path.join(blanksPath, file);
    const targetFile = path.join(absPath, file);
    const labelLang = getLabelLang(file);

    let text = fs.readFileSync(templateFile, 'utf-8');

    text = text.replace(regexGit, (match, commit, pathFile, langOverride, start, end) => {
      const content = execSync(`git show ${commit}:"${pathFile}"`, { encoding: 'utf-8' });
      const lines = content.split('\n');

      let snippetLines;
      let numbered;
      if (start && end) {
        const s = Number(start), e = Number(end);
        snippetLines = lines.slice(s - 1, e);
        numbered = addLineNumbers ? numberCode(snippetLines.join('\n'), s) : snippetLines.join('\n');
      } else {
        numbered = addLineNumbers ? numberCode(lines.join('\n')) : lines.join('\n');
      }

      const lang = langOverride || getLanguage(pathFile);
      const label = makeLabel(commit, pathFile, start, end, labelLang, remoteUrl);
      const snippet = `\`\`\`${lang}\n${numbered}\n\`\`\``;

      // return `<!-- snippet:${commit}:${pathFile}${langOverride ? `:${langOverride}` : ''}${start && end ? `#L${start}-L${end}` : ''} -->\n${label}\n\n${snippet}\n<!-- snippet:end -->`;
      return `${label}\n\n${snippet}\n`;
    });

    text = text.replace(regexInline, (match, lang, code) => {
      const numbered = addLineNumbers ? numberCode(code) : code.trimEnd();
      const snippet = `\`\`\`${lang}\n${numbered}\n\`\`\``;
      // return `<!-- snippet:${lang} -->\n${snippet}\n<!-- snippet:end -->`;
      return `${snippet}\n`;
    });

    fs.writeFileSync(targetFile, text);
    console.log(`Updated: ${targetFile}`);
  });
}
