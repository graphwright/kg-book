#!/usr/bin/env python3
"""
split_for_mkdocs.py -- Split text.md into an mkdocs-compatible directory tree.

Usage:
    python3 scripts/split_for_mkdocs.py [--src text.md] [--out docs]

The script:
  1. Parses the YAML front-matter from text.md.
  2. Splits the content at Part / Appendix boundaries (level-1 headings) and
     Chapter boundaries (level-2 headings).
  3. Strips LaTeX-specific markup that mkdocs cannot render.
  4. Writes each chapter as its own Markdown file inside a per-part directory.
  5. Writes a mkdocs.yml nav structure alongside the docs/ tree.
"""

import argparse
import os
import re
import sys
import textwrap
import yaml


# ---------------------------------------------------------------------------
# LaTeX stripping helpers
# ---------------------------------------------------------------------------

def strip_index_commands(text: str) -> str:
    r"""Remove \index{...} commands, including nested braces."""
    result = []
    i = 0
    while i < len(text):
        if text[i:i+7] == r'\index{':
            # skip to matching closing brace; j starts at the opening '{'
            depth = 0
            j = i + 6  # index of the opening '{' in '\index{'
            while j < len(text):
                if text[j] == '{':
                    depth += 1
                elif text[j] == '}':
                    depth -= 1
                    if depth == 0:
                        j += 1
                        break
                j += 1
            i = j  # skip over \index{...}
        else:
            result.append(text[i])
            i += 1
    return ''.join(result)


def strip_latex_code_spans(line: str) -> str:
    r"""Remove lines that are entirely a raw-latex code span: `\cmd{...}`{=latex}"""
    stripped = line.strip()
    if stripped.endswith('{=latex}') and stripped.startswith('`') and stripped.count('`') >= 2:
        # e.g. `\chaptermark{Canonical Identity}`{=latex}
        return ''
    return line


def latex_table_to_markdown(block_content: str) -> str:
    r"""
    Convert a simple LaTeX tabularx block to a GFM markdown table.
    Returns an empty string if conversion is not possible.
    """
    lines = block_content.splitlines()
    rows = []
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        # skip environment commands and hline
        if raw.startswith(r'\begin') or raw.startswith(r'\end') or raw == r'\hline':
            continue
        # rows end with \\
        if raw.endswith(r'\\'):
            raw = raw[:-2].strip()
        cells = [c.strip() for c in raw.split('&')]
        # strip \texttt{} from cells
        cells = [re.sub(r'\\texttt\{([^}]*)\}', r'`\1`', c) for c in cells]
        cells = [c.replace(r'\_', '_') for c in cells]
        rows.append(cells)

    if not rows:
        return ''

    # Normalise column count
    ncols = max(len(r) for r in rows)
    rows = [r + [''] * (ncols - len(r)) for r in rows]

    header = rows[0]
    body = rows[1:]
    sep = ['---'] * ncols

    md_lines = []
    md_lines.append('| ' + ' | '.join(header) + ' |')
    md_lines.append('| ' + ' | '.join(sep) + ' |')
    for row in body:
        md_lines.append('| ' + ' | '.join(row) + ' |')
    return '\n'.join(md_lines)


def strip_raw_latex_blocks(text: str) -> str:
    """Replace ```{=latex} ... ``` blocks with markdown equivalents."""
    pattern = re.compile(r'```\{=latex\}\n(.*?)```', re.DOTALL)

    def replace(m: re.Match) -> str:
        content = m.group(1)
        if r'\begin{tabularx}' in content or r'\begin{tabular}' in content:
            md_table = latex_table_to_markdown(content)
            if md_table:
                return md_table
        # Fallback: drop the block entirely
        return ''

    return pattern.sub(replace, text)


def strip_latex(text: str) -> str:
    """Apply all LaTeX-stripping transformations."""
    # 1. Remove raw latex fenced blocks (must come before line-by-line processing)
    text = strip_raw_latex_blocks(text)

    # 2. Process line by line
    out_lines = []
    for line in text.splitlines():
        line = strip_latex_code_spans(line)
        line = strip_index_commands(line)
        # \texttt{foo} -> `foo`
        line = re.sub(r'\\texttt\{([^}]*)\}', r'`\1`', line)
        # \textbf{foo} -> **foo**
        line = re.sub(r'\\textbf\{([^}]*)\}', r'**\1**', line)
        # \emph{foo} -> *foo*
        line = re.sub(r'\\emph\{([^}]*)\}', r'*\1*', line)
        # \_  ->  _
        line = line.replace(r'\_', '_')
        out_lines.append(line)

    # 3. Collapse runs of more than two blank lines into two
    text = '\n'.join(out_lines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


# ---------------------------------------------------------------------------
# Slugification
# ---------------------------------------------------------------------------

def slugify(title: str) -> str:
    """Turn a heading title into a filesystem-safe slug."""
    s = title.lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s).strip('-')
    return s


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def parse_frontmatter(src: str):
    """Return (metadata_dict, body_text) splitting YAML front-matter.

    Accepts both '---' and '...' as the closing delimiter.
    """
    if src.startswith('---'):
        m = re.search(r'\n(---|\.\.\.)\n', src[3:])
        if m:
            yaml_str = src[3: m.start() + 3].strip()
            meta = yaml.safe_load(yaml_str)
            body = src[m.start() + 3 + len(m.group(0)):].lstrip('\n')
            return meta, body
    return {}, src


class Section:
    """One logical section of the book (Part, Chapter, Appendix, or Preface)."""

    def __init__(self, level: int, title: str, content: str):
        self.level = level      # 1 = Part / Appendix, 2 = Chapter
        self.title = title
        self.content = content  # everything between this heading and the next same-or-higher level
        self.children: list['Section'] = []


def parse_sections(body: str) -> list[Section]:
    """
    Split body into a flat list of Sections at level-1 (# ...) and
    level-2 (## ...) headings.  Level-3+ headings stay inside the content.
    """
    # Preface content before the first level-1 heading
    preface_match = re.match(r'^(.*?)(?=^# )', body, re.DOTALL | re.MULTILINE)
    preface_content = preface_match.group(1).strip() if preface_match else body.strip()

    sections: list[Section] = []
    if preface_content:
        # The preface starts with ## Preface heading
        pref_title_m = re.match(r'^##\s+(.+)', preface_content)
        if pref_title_m:
            preface_content = preface_content[pref_title_m.end():].strip()
            preface_title = pref_title_m.group(1).strip()
        else:
            preface_title = 'Preface'
        sections.append(Section(0, preface_title, preface_content))

    # Find all level-1 and level-2 headings with their positions
    pattern = re.compile(r'^(#{1,2})\s+(.+)$', re.MULTILINE)
    matches = list(pattern.finditer(body))

    for idx, m in enumerate(matches):
        level = len(m.group(1))
        title = m.group(2).strip()
        start = m.end() + 1  # skip the newline
        # content runs to the next heading at same or higher level
        end = len(body)
        for next_m in matches[idx + 1:]:
            if len(next_m.group(1)) <= level:
                end = next_m.start()
                break
        content = body[start:end].strip()
        sections.append(Section(level, title, content))

    return sections


def nest_sections(flat: list[Section]) -> list[Section]:
    """
    Nest level-2 sections under their parent level-1 section.
    Level-0 (preface) stays at the top level.
    """
    top: list[Section] = []
    current_part: Section | None = None

    for sec in flat:
        if sec.level == 0:
            top.append(sec)
        elif sec.level == 1:
            top.append(sec)
            current_part = sec
        elif sec.level == 2:
            if current_part is not None:
                current_part.children.append(sec)
            else:
                top.append(sec)
    return top


# ---------------------------------------------------------------------------
# Filename / path helpers
# ---------------------------------------------------------------------------

def part_dirname(title: str) -> str:
    """'Part I: The Problem of Identity' → 'part-i'"""
    # Match "Part <roman>" prefix
    m = re.match(r'Part\s+([IVXLCDM]+)', title, re.IGNORECASE)
    if m:
        return 'part-' + m.group(1).lower()
    # Appendix A → appendix-a, Appendix B → appendix-b, etc.
    m = re.match(r'Appendix\s+([A-Z])', title, re.IGNORECASE)
    if m:
        return 'appendix-' + m.group(1).lower()
    return slugify(title)


def chapter_filename(title: str) -> str:
    """'Chapter 3: The Epistemic Commons' → 'chapter03.md'"""
    m = re.match(r'Chapter\s+(\d+)', title, re.IGNORECASE)
    if m:
        return f'chapter{int(m.group(1)):02d}.md'
    m = re.match(r'Appendix\s+([A-Z])', title, re.IGNORECASE)
    if m:
        return f'appendix-{m.group(1).lower()}.md'
    return slugify(title) + '.md'


# ---------------------------------------------------------------------------
# Writing
# ---------------------------------------------------------------------------

def write_section(path: str, title: str, content: str, heading_level: int = 1) -> None:
    """Write a Markdown file with the given heading and stripped content."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    hashes = '#' * heading_level
    body = strip_latex(content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f'{hashes} {title}\n\n')
        if body:
            f.write(body)
            f.write('\n')


def build_docs(sections: list[Section], out_dir: str) -> list[dict]:
    """
    Write all docs files and return the mkdocs nav list.
    """
    nav = []

    for sec in sections:
        if sec.level == 0:
            # Preface → docs/index.md
            path = os.path.join(out_dir, 'index.md')
            write_section(path, sec.title, sec.content, heading_level=1)
            nav.append({'Preface': 'index.md'})

        elif sec.level == 1:
            dir_name = part_dirname(sec.title)
            part_dir = os.path.join(out_dir, dir_name)

            if not sec.children:
                # Standalone part-level section (e.g. a standalone Appendix)
                fname = chapter_filename(sec.title)
                path = os.path.join(part_dir, fname)
                write_section(path, sec.title, sec.content, heading_level=1)
                nav.append({sec.title: os.path.join(dir_name, fname)})
            else:
                # Part with chapters
                part_nav = []

                # If the part itself has intro content, write an index.md
                intro = sec.content.strip()
                if intro:
                    idx_path = os.path.join(part_dir, 'index.md')
                    write_section(idx_path, sec.title, intro, heading_level=1)
                    part_nav.append({'Overview': os.path.join(dir_name, 'index.md')})

                for child in sec.children:
                    fname = chapter_filename(child.title)
                    path = os.path.join(part_dir, fname)
                    write_section(path, child.title, child.content, heading_level=2)
                    part_nav.append({child.title: os.path.join(dir_name, fname)})

                nav.append({sec.title: part_nav})

    return nav


# ---------------------------------------------------------------------------
# mkdocs.yml generation
# ---------------------------------------------------------------------------

MKDOCS_TEMPLATE = textwrap.dedent("""\
    site_name: "{site_name}"
    site_author: "{site_author}"
    docs_dir: docs
    theme:
      name: material
      features:
        - navigation.sections
        - navigation.expand
        - search.suggest
        - search.highlight
    plugins:
      - search
    nav:
    """)


def write_mkdocs_yml(meta: dict, nav: list[dict], dest: str) -> None:
    """Write mkdocs.yml next to the docs/ directory."""
    site_name = meta.get('title', 'Book')
    site_author = meta.get('author', '')

    header = MKDOCS_TEMPLATE.format(site_name=site_name, site_author=site_author)

    nav_yaml = yaml.dump(nav, default_flow_style=False, allow_unicode=True)
    # Indent nav under the 'nav:' key
    nav_indented = textwrap.indent(nav_yaml, '  ')

    with open(dest, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write(nav_indented)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--src', default='text.md', help='Source markdown file')
    parser.add_argument('--out', default='docs', help='Output docs directory')
    parser.add_argument('--mkdocs-yml', default='mkdocs.yml', help='Output mkdocs.yml path')
    args = parser.parse_args()

    src_path = args.src
    out_dir = args.out
    mkdocs_yml_path = args.mkdocs_yml

    if not os.path.isfile(src_path):
        sys.exit(f'Error: source file not found: {src_path}')

    with open(src_path, encoding='utf-8') as f:
        raw = f.read()

    meta, body = parse_frontmatter(raw)
    flat_sections = parse_sections(body)
    nested_sections = nest_sections(flat_sections)
    nav = build_docs(nested_sections, out_dir)
    write_mkdocs_yml(meta, nav, mkdocs_yml_path)

    print(f'Wrote docs to {out_dir}/ and {mkdocs_yml_path}')


if __name__ == '__main__':
    main()
