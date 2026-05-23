#!/usr/bin/env python3
"""
统一概念页中的学者名为「中文名（英文名）」，仅首次出现时标注英文。

修复点 v2:
1. 处理 "First Last" 全英文名（如 Carl Schmitt → 卡尔·施密特）
2. 修复替换后多余空格问题
3. 正确判断首次出现：原文中文名已存在时，不重复标注
4. INDEX.md 特殊处理：只处理正文中的英文名，不碰链接格式里的
"""

import os
import re

CONCEPT_DIR = "/Users/myke/Documents/MERJIC/概念库/概念页"

# ── 第一层：全名替换（优先匹配）──
# "First Last" → "中文名"
# 先匹配长的，再匹配短的
FULL_NAME_MAP = [
    # Long-form names (First + Last)
    ("Carl Schmitt", "卡尔·施密特"),
    ("Carl Schmitt", "卡尔·施密特"),
    ("Michel Foucault", "福柯"),
    ("Giorgio Agamben", "阿甘本"),
    ("Byung-Chul Han", "韩炳哲"),
    ("Byung-chul Han", "韩炳哲"),
    ("Merleau-Ponty", "梅洛-庞蒂"),
    ("Lévi-Strauss", "列维-施特劳斯"),
    ("Evans-Pritchard", "埃文斯-普里查德"),
    ("Simone de Beauvoir", "波伏娃"),
    ("Guy Debord", "德波"),
    ("Mary Douglas", "道格拉斯"),
    ("Herbert Simon", "赫伯特·西蒙"),
    ("Amartya Sen", "阿马蒂亚·森"),
    ("Adam Smith", "亚当·斯密"),
    ("Victor Turner", "维克多·特纳"),
    ("David Hume", "休谟"),
    ("Immanuel Kant", "康德"),
    ("Friedrich Nietzsche", "尼采"),
    ("Martin Heidegger", "海德格尔"),
    ("Karl Marx", "马克思"),
    ("Max Weber", "韦伯"),
    ("Émile Durkheim", "涂尔干"),
    ("Jürgen Habermas", "哈贝马斯"),
    ("Hannah Arendt", "阿伦特"),
    ("Walter Benjamin", "本雅明"),
    ("Theodor Adorno", "阿多诺"),
    ("Jacques Derrida", "德里达"),
    ("Gilles Deleuze", "德勒兹"),
    ("Félix Guattari", "加塔利"),
    ("Jacques Lacan", "拉康"),
    ("Edmund Husserl", "胡塞尔"),
    ("Jean-Paul Sartre", "萨特"),
    ("Albert Camus", "加缪"),
    ("Mikhail Bakhtin", "巴赫金"),
    ("Julia Kristeva", "克里斯蒂娃"),
    ("Pierre Bourdieu", "布迪厄"),
    ("Erving Goffman", "戈夫曼"),
    ("Antonio Gramsci", "葛兰西"),
    ("Georg Wilhelm Friedrich Hegel", "黑格尔"),
    ("John Rawls", "罗尔斯"),
    ("John Locke", "洛克"),
    ("Thomas Hobbes", "霍布斯"),
    ("Jean-Jacques Rousseau", "卢梭"),
    ("Noam Chomsky", "乔姆斯基"),
    ("Ludwig Wittgenstein", "维特根斯坦"),
    ("Sigmund Freud", "弗洛伊德"),
    ("Daniel Kahneman", "卡尼曼"),
    ("Amos Tversky", "特沃斯基"),
    ("Karl Popper", "卡尔·波普尔"),
    ("Thomas Kuhn", "库恩"),
    ("Thomas S. Kuhn", "库恩"),
    ("Niklas Luhmann", "卢曼"),
    ("Peter Sloterdijk", "斯洛特戴克"),
    ("Roberto Esposito", "埃斯波西托"),
    ("Antonio Negri", "奈格里"),
    ("Chantal Mouffe", "墨菲"),
    ("Ernesto Laclau", "拉克劳"),
    ("Giorgio Agamben", "阿甘本"),
    ("Slavoj Žižek", "齐泽克"),
    ("Slavoj Zizek", "齐泽克"),
    ("Alain Badiou", "巴迪欧"),
    ("Jacques Rancière", "朗西埃"),
    ("Jacques Ranciere", "朗西埃"),
    ("Hartmut Rosa", "罗萨"),
    ("William James", "威廉·詹姆斯"),
    ("John Dewey", "杜威"),
    ("Charles Sanders Peirce", "皮尔士"),
    ("Bertrand Russell", "罗素"),
    ("W. V. O. Quine", "蒯因"),
    ("Willard Van Orman Quine", "蒯因"),
    ("Saul Kripke", "克里普克"),
    ("J. L. Austin", "奥斯汀"),
    ("John Searle", "塞尔"),
    ("Imre Lakatos", "拉卡托斯"),
    ("Paul Feyerabend", "费耶阿本德"),
    ("Michael Polanyi", "波兰尼"),
    ("Thorstein Veblen", "凡勃伦"),
    ("John Maynard Keynes", "凯恩斯"),
    ("Friedrich Hayek", "哈耶克"),
    ("Joseph Schumpeter", "熊彼特"),
    ("Ronald Coase", "科斯"),
    ("Oliver Williamson", "威廉姆森"),
    ("Douglass North", "道格拉斯·诺斯"),
    ("Herbert Simon", "赫伯特·西蒙"),
    ("Nassim Nicholas Taleb", "塔勒布"),
    ("Georg Simmel", "齐美尔"),
    ("Talcott Parsons", "帕森斯"),
    ("Robert K. Merton", "默顿"),
    ("Norbert Elias", "埃利亚斯"),
    ("Clifford Geertz", "格尔茨"),
    ("Bronisław Malinowski", "马林诺夫斯基"),
    ("Marcel Mauss", "莫斯"),
    ("Jean Baudrillard", "鲍德里亚"),
    ("Jean-François Lyotard", "利奥塔"),
    ("Bruno Latour", "拉图尔"),
    ("Donna Haraway", "哈拉维"),
    ("Michel Foucault", "福柯"),
    ("Martin Heidegger", "海德格尔"),
    ("Max Weber", "韦伯"),
    ("Karl Marx", "马克思"),
    ("Friedrich Nietzsche", "尼采"),
    ("Edmund Husserl", "胡塞尔"),
    ("Maurice Merleau-Ponty", "梅洛-庞蒂"),
    ("Emmanuel Levinas", "列维纳斯"),
    ("Hans-Georg Gadamer", "伽达默尔"),
    ("Paul Ricœur", "利科"),
    ("Søren Kierkegaard", "克尔凯郭尔"),
    ("Karl Jaspers", "雅斯贝尔斯"),
    ("Martin Buber", "布伯"),
    ("Jürgen Habermas", "哈贝马斯"),
    ("Theodor W. Adorno", "阿多诺"),
    ("Max Horkheimer", "霍克海默"),
    ("Herbert Marcuse", "马尔库塞"),
    ("Louis Althusser", "阿尔都塞"),
    ("György Lukács", "卢卡奇"),
    ("Georg Lukács", "卢卡奇"),
    ("Benedict Anderson", "本尼迪克特·安德森"),
    ("Edward Said", "萨义德"),
    ("Gayatri Spivak", "斯皮瓦克"),
    ("Frantz Fanon", "法农"),
    ("Judith Butler", "巴特勒"),
    ("Michael Walzer", "沃尔泽"),
    ("Alasdair MacIntyre", "麦金太尔"),
    ("Michael Sandel", "桑德尔"),
    ("Charles Taylor", "泰勒"),
    ("Isaiah Berlin", "伯林"),
    ("Martha Nussbaum", "努斯鲍姆"),
    ("Amartya Sen", "阿马蒂亚·森"),
    ("Hilary Putnam", "普特南"),
    ("Richard Rorty", "罗蒂"),
    ("Carl Schmitt", "卡尔·施密特"),
    ("Leo Strauss", "施特劳斯"),
    ("Niccolò Machiavelli", "马基雅维利"),
    ("Montesquieu", "孟德斯鸠"),
    ("Alexis de Tocqueville", "托克维尔"),
    ("Ronald Coase", "科斯"),
    ("Oliver Williamson", "威廉姆森"),
    ("Albert O. Hirschman", "赫希曼"),
    ("Mancur Olson", "奥尔森"),
    ("James Buchanan", "布坎南"),
    ("Anthony Giddens", "吉登斯"),
    ("Ulrich Beck", "贝克"),
    ("Zygmunt Bauman", "鲍曼"),
    ("Niklas Luhmann", "卢曼"),
    ("Pierre Bourdieu", "布迪厄"),
    ("Jean Baudrillard", "鲍德里亚"),
    ("Guy Debord", "德波"),
    ("Roland Barthes", "巴特"),
    ("Michel de Certeau", "德·塞尔托"),
    ("Gilles Deleuze", "德勒兹"),
    ("Félix Guattari", "加塔利"),
    ("Jacques Derrida", "德里达"),
    ("Jean-François Lyotard", "利奥塔"),
    ("Slavoj Žižek", "齐泽克"),
    ("Alain Badiou", "巴迪欧"),
    ("Jacques Rancière", "朗西埃"),
    ("Jacques Ranciere", "朗西埃"),
    ("Giorgio Agamben", "阿甘本"),
    ("Roberto Esposito", "埃斯波西托"),
    ("Antonio Negri", "奈格里"),
    ("Michael Hardt", "哈特"),
    ("Chantal Mouffe", "墨菲"),
    ("Ernesto Laclau", "拉克劳"),
    ("Hartmut Rosa", "罗萨"),
    ("Peter Sloterdijk", "斯洛特戴克"),
    ("Byung-Chul Han", "韩炳哲"),
    ("Bakhtin", "巴赫金"),
]

# ── 第二层：姓氏替换（如文件中只有 "Foucault" 没有 "Michel Foucault"）──
LAST_NAME_MAP = [
    ("Agamben", "阿甘本"),
    ("Althusser", "阿尔都塞"),
    ("Arendt", "阿伦特"),
    ("Badiou", "巴迪欧"),
    ("Bakhtin", "巴赫金"),
    ("Barthes", "巴特"),
    ("Baudrillard", "鲍德里亚"),
    ("Bauman", "鲍曼"),
    ("Beauvoir", "波伏娃"),
    ("Benjamin", "本雅明"),
    ("Berger", "伯格"),
    ("Bourdieu", "布迪厄"),
    ("Butler", "巴特勒"),
    ("Camus", "加缪"),
    ("Coase", "科斯"),
    ("Debord", "德波"),
    ("Deleuze", "德勒兹"),
    ("Derrida", "德里达"),
    ("Dilthey", "狄尔泰"),
    ("Durkheim", "涂尔干"),
    ("Elias", "埃利亚斯"),
    ("Esposito", "埃斯波西托"),
    ("Fanon", "法农"),
    ("Foucault", "福柯"),
    ("Freud", "弗洛伊德"),
    ("Gadamer", "伽达默尔"),
    ("Geertz", "格尔茨"),
    ("Giddens", "吉登斯"),
    ("Goffman", "戈夫曼"),
    ("Gramsci", "葛兰西"),
    ("Guattari", "加塔利"),
    ("Habermas", "哈贝马斯"),
    ("Haraway", "哈拉维"),
    ("Hayek", "哈耶克"),
    ("Hegel", "黑格尔"),
    ("Heidegger", "海德格尔"),
    ("Hobbes", "霍布斯"),
    ("Horkheimer", "霍克海默"),
    ("Hume", "休谟"),
    ("Husserl", "胡塞尔"),
    ("Jaspers", "雅斯贝尔斯"),
    ("Jung", "荣格"),
    ("Kahneman", "卡尼曼"),
    ("Kant", "康德"),
    ("Kierkegaard", "克尔凯郭尔"),
    ("Kristeva", "克里斯蒂娃"),
    ("Kripke", "克里普克"),
    ("Kuhn", "库恩"),
    ("Lacan", "拉康"),
    ("Laclau", "拉克劳"),
    ("Latour", "拉图尔"),
    ("Levinas", "列维纳斯"),
    ("Locke", "洛克"),
    ("Luhmann", "卢曼"),
    ("Lukács", "卢卡奇"),
    ("Lukacs", "卢卡奇"),
    ("Lyotard", "利奥塔"),
    ("MacIntyre", "麦金太尔"),
    ("Malinowski", "马林诺夫斯基"),
    ("Marcuse", "马尔库塞"),
    ("Marx", "马克思"),
    ("Mauss", "莫斯"),
    ("Merton", "默顿"),
    ("Mouffe", "墨菲"),
    ("Negri", "奈格里"),
    ("Nietzsche", "尼采"),
    ("Nussbaum", "努斯鲍姆"),
    ("Parsons", "帕森斯"),
    ("Piaget", "皮亚杰"),
    ("Plato", "柏拉图"),
    ("Polanyi", "波兰尼"),
    ("Popper", "波普尔"),
    ("Putnam", "普特南"),
    ("Quine", "蒯因"),
    ("Rancière", "朗西埃"),
    ("Ranciere", "朗西埃"),
    ("Rawls", "罗尔斯"),
    ("Ricoeur", "利科"),
    ("Rogers", "罗杰斯"),
    ("Rousseau", "卢梭"),
    ("Said", "萨义德"),
    ("Sandel", "桑德尔"),
    ("Schmitt", "施密特"),
    ("Schumpeter", "熊彼特"),
    ("Searle", "塞尔"),
    ("Simmel", "齐美尔"),
    ("Sloterdijk", "斯洛特戴克"),
    ("Spivak", "斯皮瓦克"),
    ("Taleb", "塔勒布"),
    ("Thaler", "泰勒"),
    ("Tocqueville", "托克维尔"),
    ("Tversky", "特沃斯基"),
    ("Veblen", "凡勃伦"),
    ("Vygotsky", "维果茨基"),
    ("Walzer", "沃尔泽"),
    ("Weber", "韦伯"),
    ("Williamson", "威廉姆森"),
    ("Wittgenstein", "维特根斯坦"),
    ("Žižek", "齐泽克"),
    ("Zizek", "齐泽克"),
    # Second pass additions
    ("Montesquieu", "孟德斯鸠"),
    ("Chomsky", "乔姆斯基"),
    ("Machiavelli", "马基雅维利"),
    ("Newton", "牛顿"),
    ("Turing", "图灵"),
    ("Skinner", "斯金纳"),
    ("Lakatos", "拉卡托斯"),
    ("Becker", "贝克尔"),
    ("Bandura", "班杜拉"),
    ("Dewey", "杜威"),
    ("Russell", "罗素"),
    ("Gödel", "哥德尔"),
    ("Godel", "哥德尔"),
    ("Peirce", "皮尔士"),
    ("Austin", "奥斯汀"),
    ("Hardt", "哈特"),
    ("Berlin", "伯林"),
    ("Rorty", "罗蒂"),
    ("Hirschman", "赫希曼"),
    ("Olson", "奥尔森"),
    ("Buchanan", "布坎南"),
    ("Beck", "贝克"),
]

# Ambiguous names - skip in last-name-only matching
SKIP_LAST_NAMES = {
    "Han", "Taylor", "James", "Sen", "Smith", "Turner",
    "Douglas", "Simon", "North", "Rosa", "Strauss",
}

# Build deduplicated lookup
def build_lookups():
    """Build (english, chinese) lists, deduplicated, sorted by length desc."""
    # Full names: already in (eng, chn) format
    full = {}
    for eng, chn in FULL_NAME_MAP:
        if isinstance(chn, str):  # skip the broken tuple
            full[eng] = chn

    # Last names: only those not in SKIP
    last = {}
    for eng, chn in LAST_NAME_MAP:
        if eng in SKIP_LAST_NAMES:
            continue
        if eng not in full:  # don't override full names
            last[eng] = chn

    # Sort by length desc for matching priority
    full_sorted = sorted(full.items(), key=lambda x: -len(x[0]))
    last_sorted = sorted(last.items(), key=lambda x: -len(x[0]))

    return full_sorted, last_sorted


def split_frontmatter(content):
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            return content[:end+3], content[end+3:]
    return "", content


def has_chinese_name_in_body(body, chn_name):
    """Check if the Chinese name already exists in the body."""
    return chn_name in body


def clean_spaces_around(text, pos, inserted_len):
    """Remove double spaces around a replacement region."""
    # This is handled inline
    pass


def process_file(filepath, full_sorted, last_sorted):
    with open(filepath, 'r') as f:
        content = f.read()

    original = content
    fm, body = split_frontmatter(content)

    # Track which scholars have been introduced (first occurrence annotated)
    # Key: Chinese name, Value: True
    introduced = {}

    # First: check if any 中文名（EngName） patterns already exist
    # This means the scholar was already introduced, so future English names
    # should just become Chinese name
    for _, chn in full_sorted + last_sorted:
        if chn in introduced:
            continue
        # Check for pattern like 福柯（Foucault）or 福柯(Foucault)
        for eng, _ in full_sorted:
            if re.search(re.escape(chn) + r'\s*[（(]\s*' + re.escape(eng) + r'\s*[）)]', body):
                introduced[chn] = True
                break
        if chn not in introduced:
            for eng, _ in last_sorted:
                if re.search(re.escape(chn) + r'\s*[（(]\s*' + re.escape(eng) + r'\s*[）)]', body):
                    introduced[chn] = True
                    break

    # Also check if Chinese name appears before any English name
    # (e.g., if "福柯" appears in body but "Foucault" also appears, the Chinese name
    # came first and no annotation is needed — just replace English → Chinese)
    for eng, chn in full_sorted + last_sorted:
        if chn in introduced:
            continue
        chn_pos = body.find(chn)
        if chn_pos != -1:
            # Chinese name exists, check if English name exists
            eng_pattern = r'(?<![\w])' + re.escape(eng) + r'(?![\w])'
            eng_match = re.search(eng_pattern, body)
            if eng_match:
                # Chinese appears before English, or they're on different lines
                # Just replace English → Chinese, no annotation needed
                introduced[chn] = True

    def do_replacement(body_text, eng_name, chn_name, all_eng_names):
        """Replace one English name in body. Returns (new_body, did_change)."""
        # Skip if inside markdown link syntax like [text](url)
        # Match whole word
        pattern = r'(?<![\w/\[（(])(' + re.escape(eng_name) + r')(?![\w/\]）)])'

        matches = list(re.finditer(pattern, body_text))
        if not matches:
            return body_text, False

        changed = False

        # Process from last to first to preserve positions
        for match in reversed(matches):
            start, end = match.start(), match.end()

            # Skip if inside a markdown link [text](url) — check if surrounded by ](
            line_start = body_text.rfind('\n', 0, start) + 1
            line = body_text[line_start:start] + body_text[start:end] + body_text[end:body_text.find('\n', end) if '\n' in body_text[end:] else len(body_text)]
            if '](' in line and body_text[end:end+1] in (')', '）', '', '\n'):
                # Check if it's in a URL-like context
                context = body_text[max(0, start-30):end+30]
                if '](' in context:
                    continue

            # Skip if already part of 中文名（EngName）pattern
            before = body_text[max(0, start-30):start]
            if re.search(re.escape(chn_name) + r'\s*[（(]\s*$', before):
                continue

            # Determine replacement
            if chn_name in introduced and introduced[chn_name]:
                # Already introduced → just Chinese name
                replacement = chn_name
            else:
                # First occurrence → 中文名（EngName）
                replacement = f"{chn_name}（{eng_name}）"
                introduced[chn_name] = True

            # Do replacement
            body_text = body_text[:start] + replacement + body_text[end:]
            changed = True

            # Clean up double spaces around the replacement
            # Look at char before replacement and char after
            check_start = start
            check_end = start + len(replacement)
            # We don't need to clean if we handle it in the replacement context

        # Post-pass: clean double spaces near scholar names
        # Pattern: space + 中文名 or 中文名 + space where the space is redundant
        for name in set(chn_name for _, chn_name in (full_sorted + last_sorted)):
            if not name:
                continue
            # 中文名 followed by Chinese char with space → remove space
            body_text = re.sub(
                re.escape(name) + r'(?=[一-鿿])',
                name,
                body_text
            )
            # 中文名 preceded by Chinese char with space → remove space
            body_text = re.sub(
                r'(?<=[一-鿿（)])\s+' + re.escape(name),
                name,
                body_text
            )
            # 中文名（Eng）followed by Chinese char with space → remove space
            body_text = re.sub(
                re.escape(name) + r'[（(][^）)]+[）)]\s+(?=[一-鿿])',
                lambda m: re.sub(r'\s+$', '', m.group(0)),
                body_text
            )

        return body_text, changed

    # Process all full names first (longer matches first)
    for eng, chn in full_sorted:
        body, changed = do_replacement(body, eng, chn, full_sorted)

    # Then process last names
    for eng, chn in last_sorted:
        body, changed = do_replacement(body, eng, chn, last_sorted)

    # Final cleanup: remove double spaces
    # But preserve intentional double spaces (unlikely in Chinese text)
    # Only clean spaces adjacent to Chinese characters
    body = re.sub(r'(?<=[一-鿿）)]) +(?=[一-鿿（])', '', body)
    body = re.sub(r'(?<=[一-鿿）)]) +(?=\S)', lambda m: '' if len(m.group(0)) > 1 else m.group(0), body)

    result = fm + body

    if result != original:
        return result, True
    return original, False


def main():
    full_sorted, last_sorted = build_lookups()

    changed_files = []
    skipped_files = []
    error_files = []

    for f in sorted(os.listdir(CONCEPT_DIR)):
        if not f.endswith('.md'):
            continue
        filepath = os.path.join(CONCEPT_DIR, f)

        try:
            result, changed = process_file(filepath, full_sorted, last_sorted)
            if changed:
                with open(filepath, 'w') as fh:
                    fh.write(result)
                changed_files.append(f)
            else:
                skipped_files.append(f)
        except Exception as e:
            error_files.append((f, str(e)))
            import traceback
            traceback.print_exc()

    print(f"=== 完成 ===")
    print(f"已修改: {len(changed_files)} 个文件")
    print(f"未改动: {len(skipped_files)} 个文件")
    if error_files:
        print(f"错误: {len(error_files)} 个文件")
        for f, err in error_files:
            print(f"  {f}: {err}")

    print(f"\n=== 修改的文件 ===")
    for f in changed_files:
        print(f"  {f}")


if __name__ == "__main__":
    main()
