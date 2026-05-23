#!/usr/bin/env python3
"""
统一概念页中的学者名为「中文名（英文名）」，仅首次出现时标注英文。

策略：两趟扫描。
1. 先扫描每个文件，找到所有需要替换的英文人名及其位置
2. 按位置从后往前替换，避免位置偏移
3. 每个学者首次出现用「中文名（英文原名）」，后续只用「中文名」
4. 如果正文中文名已经出现在英文名之前，则只替换英文→中文，不加标注
"""

import os
import re

CONCEPT_DIR = "/Users/myke/Documents/MERJIC/概念库/概念页"

# 全名映射（长名优先匹配）
FULL_NAMES = {
    "carl schmitt": ("卡尔·施密特", "Carl Schmitt"),
    "michel foucault": ("福柯", "Michel Foucault"),
    "giorgio agamben": ("阿甘本", "Giorgio Agamben"),
    "byung-chul han": ("韩炳哲", "Byung-Chul Han"),
    "byung-chul han": ("韩炳哲", "Byung-chul Han"),
    "merleau-ponty": ("梅洛-庞蒂", "Merleau-Ponty"),
    "lévi-strauss": ("列维-施特劳斯", "Lévi-Strauss"),
    "evans-pritchard": ("埃文斯-普里查德", "Evans-Pritchard"),
    "simone de beauvoir": ("波伏娃", "Simone de Beauvoir"),
    "guy debord": ("德波", "Guy Debord"),
    "herbert simon": ("赫伯特·西蒙", "Herbert Simon"),
    "amartya sen": ("阿马蒂亚·森", "Amartya Sen"),
    "adam smith": ("亚当·斯密", "Adam Smith"),
    "victor turner": ("维克多·特纳", "Victor Turner"),
    "david hume": ("休谟", "David Hume"),
    "immanuel kant": ("康德", "Immanuel Kant"),
    "friedrich nietzsche": ("尼采", "Friedrich Nietzsche"),
    "martin heidegger": ("海德格尔", "Martin Heidegger"),
    "karl marx": ("马克思", "Karl Marx"),
    "max weber": ("韦伯", "Max Weber"),
    "émile durkheim": ("涂尔干", "Émile Durkheim"),
    "jürgen habermas": ("哈贝马斯", "Jürgen Habermas"),
    "hannah arendt": ("阿伦特", "Hannah Arendt"),
    "walter benjamin": ("本雅明", "Walter Benjamin"),
    "theodor adorno": ("阿多诺", "Theodor Adorno"),
    "jacques derrida": ("德里达", "Jacques Derrida"),
    "gilles deleuze": ("德勒兹", "Gilles Deleuze"),
    "félix guattari": ("加塔利", "Félix Guattari"),
    "jacques lacan": ("拉康", "Jacques Lacan"),
    "edmund husserl": ("胡塞尔", "Edmund Husserl"),
    "jean-paul sartre": ("萨特", "Jean-Paul Sartre"),
    "albert camus": ("加缪", "Albert Camus"),
    "mikhail bakhtin": ("巴赫金", "Mikhail Bakhtin"),
    "julia kristeva": ("克里斯蒂娃", "Julia Kristeva"),
    "pierre bourdieu": ("布迪厄", "Pierre Bourdieu"),
    "erving goffman": ("戈夫曼", "Erving Goffman"),
    "antonio gramsci": ("葛兰西", "Antonio Gramsci"),
    "john rawls": ("罗尔斯", "John Rawls"),
    "john locke": ("洛克", "John Locke"),
    "thomas hobbes": ("霍布斯", "Thomas Hobbes"),
    "jean-jacques rousseau": ("卢梭", "Jean-Jacques Rousseau"),
    "ludwig wittgenstein": ("维特根斯坦", "Ludwig Wittgenstein"),
    "sigmund freud": ("弗洛伊德", "Sigmund Freud"),
    "daniel kahneman": ("卡尼曼", "Daniel Kahneman"),
    "amos tversky": ("特沃斯基", "Amos Tversky"),
    "thomas kuhn": ("库恩", "Thomas Kuhn"),
    "niklas luhmann": ("卢曼", "Niklas Luhmann"),
    "peter sloterdijk": ("斯洛特戴克", "Peter Sloterdijk"),
    "roberto esposito": ("埃斯波西托", "Roberto Esposito"),
    "slavoj žižek": ("齐泽克", "Slavoj Žižek"),
    "slavoj zizek": ("齐泽克", "Slavoj Zizek"),
    "alain badiou": ("巴迪欧", "Alain Badiou"),
    "jacques rancière": ("朗西埃", "Jacques Rancière"),
    "jacques ranciere": ("朗西埃", "Jacques Ranciere"),
    "hartmut rosa": ("罗萨", "Hartmut Rosa"),
    "william james": ("威廉·詹姆斯", "William James"),
    "john dewey": ("杜威", "John Dewey"),
    "bertrand russell": ("罗素", "Bertrand Russell"),
    "imre lakatos": ("拉卡托斯", "Imre Lakatos"),
    "michael polanyi": ("波兰尼", "Michael Polanyi"),
    "thorstein veblen": ("凡勃伦", "Thorstein Veblen"),
    "john maynard keynes": ("凯恩斯", "John Maynard Keynes"),
    "friedrich hayek": ("哈耶克", "Friedrich Hayek"),
    "joseph schumpeter": ("熊彼特", "Joseph Schumpeter"),
    "ronald coase": ("科斯", "Ronald Coase"),
    "oliver williamson": ("威廉姆森", "Oliver Williamson"),
    "douglass north": ("道格拉斯·诺斯", "Douglass North"),
    "nassim nicholas taleb": ("塔勒布", "Nassim Nicholas Taleb"),
    "georg simmel": ("齐美尔", "Georg Simmel"),
    "talcott parsons": ("帕森斯", "Talcott Parsons"),
    "robert k. merton": ("默顿", "Robert K. Merton"),
    "norbert elias": ("埃利亚斯", "Norbert Elias"),
    "clifford geertz": ("格尔茨", "Clifford Geertz"),
    "bronisław malinowski": ("马林诺夫斯基", "Bronisław Malinowski"),
    "marcel mauss": ("莫斯", "Marcel Mauss"),
    "jean baudrillard": ("鲍德里亚", "Jean Baudrillard"),
    "jean-françois lyotard": ("利奥塔", "Jean-François Lyotard"),
    "bruno latour": ("拉图尔", "Bruno Latour"),
    "donna haraway": ("哈拉维", "Donna Haraway"),
    "maurice merleau-ponty": ("梅洛-庞蒂", "Maurice Merleau-Ponty"),
    "emmanuel levinas": ("列维纳斯", "Emmanuel Levinas"),
    "hans-georg gadamer": ("伽达默尔", "Hans-Georg Gadamer"),
    "søren kierkegaard": ("克尔凯郭尔", "Søren Kierkegaard"),
    "karl jaspers": ("雅斯贝尔斯", "Karl Jaspers"),
    "martin buber": ("布伯", "Martin Buber"),
    "max horkheimer": ("霍克海默", "Max Horkheimer"),
    "herbert marcuse": ("马尔库塞", "Herbert Marcuse"),
    "louis althusser": ("阿尔都塞", "Louis Althusser"),
    "györgy lukács": ("卢卡奇", "György Lukács"),
    "edward said": ("萨义德", "Edward Said"),
    "gayatri spivak": ("斯皮瓦克", "Gayatri Spivak"),
    "frantz fanon": ("法农", "Frantz Fanon"),
    "judith butler": ("巴特勒", "Judith Butler"),
    "michael walzer": ("沃尔泽", "Michael Walzer"),
    "alasdair macintyre": ("麦金太尔", "Alasdair MacIntyre"),
    "michael sandel": ("桑德尔", "Michael Sandel"),
    "charles taylor": ("泰勒", "Charles Taylor"),
    "isaiah berlin": ("伯林", "Isaiah Berlin"),
    "martha nussbaum": ("努斯鲍姆", "Martha Nussbaum"),
    "hilary putnam": ("普特南", "Hilary Putnam"),
    "niccolò machiavelli": ("马基雅维利", "Niccolò Machiavelli"),
    "alexis de tocqueville": ("托克维尔", "Alexis de Tocqueville"),
    "antoine de saint-exupéry": ("圣埃克苏佩里", "Antoine de Saint-Exupéry"),
    "carl schmitt": ("卡尔·施密特", "Carl Schmitt"),
    "leo strauss": ("施特劳斯", "Leo Strauss"),
    "mary douglas": ("道格拉斯", "Mary Douglas"),
}

# 姓氏映射（仅在不是全名匹配时使用）
LAST_NAMES = {
    "agamben": ("阿甘本", "Agamben"),
    "althusser": ("阿尔都塞", "Althusser"),
    "arendt": ("阿伦特", "Arendt"),
    "badiou": ("巴迪欧", "Badiou"),
    "bakhtin": ("巴赫金", "Bakhtin"),
    "baudrillard": ("鲍德里亚", "Baudrillard"),
    "bauman": ("鲍曼", "Bauman"),
    "benjamin": ("本雅明", "Benjamin"),
    "berger": ("伯格", "Berger"),
    "bourdieu": ("布迪厄", "Bourdieu"),
    "butler": ("巴特勒", "Butler"),
    "camus": ("加缪", "Camus"),
    "coase": ("科斯", "Coase"),
    "debord": ("德波", "Debord"),
    "deleuze": ("德勒兹", "Deleuze"),
    "derrida": ("德里达", "Derrida"),
    "durkheim": ("涂尔干", "Durkheim"),
    "elias": ("埃利亚斯", "Elias"),
    "esposito": ("埃斯波西托", "Esposito"),
    "fanon": ("法农", "Fanon"),
    "foucault": ("福柯", "Foucault"),
    "freud": ("弗洛伊德", "Freud"),
    "gadamer": ("伽达默尔", "Gadamer"),
    "geertz": ("格尔茨", "Geertz"),
    "giddens": ("吉登斯", "Giddens"),
    "goffman": ("戈夫曼", "Goffman"),
    "gramsci": ("葛兰西", "Gramsci"),
    "guattari": ("加塔利", "Guattari"),
    "habermas": ("哈贝马斯", "Habermas"),
    "haraway": ("哈拉维", "Haraway"),
    "hayek": ("哈耶克", "Hayek"),
    "hegel": ("黑格尔", "Hegel"),
    "heidegger": ("海德格尔", "Heidegger"),
    "hobbes": ("霍布斯", "Hobbes"),
    "horkheimer": ("霍克海默", "Horkheimer"),
    "husserl": ("胡塞尔", "Husserl"),
    "jaspers": ("雅斯贝尔斯", "Jaspers"),
    "kahneman": ("卡尼曼", "Kahneman"),
    "kant": ("康德", "Kant"),
    "kierkegaard": ("克尔凯郭尔", "Kierkegaard"),
    "kristeva": ("克里斯蒂娃", "Kristeva"),
    "kuhn": ("库恩", "Kuhn"),
    "lacan": ("拉康", "Lacan"),
    "laclau": ("拉克劳", "Laclau"),
    "latour": ("拉图尔", "Latour"),
    "levinas": ("列维纳斯", "Levinas"),
    "locke": ("洛克", "Locke"),
    "luhmann": ("卢曼", "Luhmann"),
    "lukács": ("卢卡奇", "Lukács"),
    "lukacs": ("卢卡奇", "Lukacs"),
    "lyotard": ("利奥塔", "Lyotard"),
    "macintyre": ("麦金太尔", "MacIntyre"),
    "malinowski": ("马林诺夫斯基", "Malinowski"),
    "marcuse": ("马尔库塞", "Marcuse"),
    "marx": ("马克思", "Marx"),
    "mauss": ("莫斯", "Mauss"),
    "merton": ("默顿", "Merton"),
    "mouffe": ("墨菲", "Mouffe"),
    "negri": ("奈格里", "Negri"),
    "nietzsche": ("尼采", "Nietzsche"),
    "nussbaum": ("努斯鲍姆", "Nussbaum"),
    "parsons": ("帕森斯", "Parsons"),
    "piaget": ("皮亚杰", "Piaget"),
    "plato": ("柏拉图", "Plato"),
    "polanyi": ("波兰尼", "Polanyi"),
    "popper": ("波普尔", "Popper"),
    "putnam": ("普特南", "Putnam"),
    "quine": ("蒯因", "Quine"),
    "rawls": ("罗尔斯", "Rawls"),
    "ricoeur": ("利科", "Ricoeur"),
    "rogers": ("罗杰斯", "Rogers"),
    "rousseau": ("卢梭", "Rousseau"),
    "said": ("萨义德", "Said"),
    "sandel": ("桑德尔", "Sandel"),
    "schmitt": ("施密特", "Schmitt"),
    "schumpeter": ("熊彼特", "Schumpeter"),
    "searle": ("塞尔", "Searle"),
    "simmel": ("齐美尔", "Simmel"),
    "sloterdijk": ("斯洛特戴克", "Sloterdijk"),
    "spivak": ("斯皮瓦克", "Spivak"),
    "taleb": ("塔勒布", "Taleb"),
    "thaler": ("泰勒", "Thaler"),
    "tocqueville": ("托克维尔", "Tocqueville"),
    "tversky": ("特沃斯基", "Tversky"),
    "veblen": ("凡勃伦", "Veblen"),
    "vygotsky": ("维果茨基", "Vygotsky"),
    "walzer": ("沃尔泽", "Walzer"),
    "weber": ("韦伯", "Weber"),
    "williamson": ("威廉姆森", "Williamson"),
    "wittgenstein": ("维特根斯坦", "Wittgenstein"),
    "žižek": ("齐泽克", "Žižek"),
    "zizek": ("齐泽克", "Zizek"),
    # Second-tier
    "montesquieu": ("孟德斯鸠", "Montesquieu"),
    "machiavelli": ("马基雅维利", "Machiavelli"),
    "chomsky": ("乔姆斯基", "Chomsky"),
    "skinner": ("斯金纳", "Skinner"),
    "lakatos": ("拉卡托斯", "Lakatos"),
    "dewey": ("杜威", "Dewey"),
    "russell": ("罗素", "Russell"),
    "lukacs": ("卢卡奇", "Lukacs"),
}


def find_all_matches(body):
    """Find all scholar name occurrences in body text.
    Returns list of (start, end, chn_name, eng_name_original, chn_name_key) sorted by position.
    """
    matches = []

    # 1. Full names (case-insensitive, longer matches first)
    for full_lower, (chn, eng_orig) in sorted(FULL_NAMES.items(), key=lambda x: -len(x[0])):
        # Case-insensitive search in body
        body_lower = body.lower()
        idx = 0
        while True:
            pos = body_lower.find(full_lower, idx)
            if pos == -1:
                break
            # Verify word boundaries
            before_ok = pos == 0 or not body[pos-1].isalpha()
            after_end = pos + len(full_lower)
            after_ok = after_end >= len(body) or not body[after_end].isalpha()
            if before_ok and after_ok:
                # Check it's not inside [[]] link text or frontmatter
                matches.append((pos, after_end, chn, eng_orig, chn))
            idx = pos + 1

    # 2. Last names (only if not already covered by a full name at same position)
    for last_lower, (chn, eng_orig) in sorted(LAST_NAMES.items(), key=lambda x: -len(x[0])):
        body_lower = body.lower()
        idx = 0
        while True:
            pos = body_lower.find(last_lower, idx)
            if pos == -1:
                break
            before_ok = pos == 0 or not body[pos-1].isalpha()
            after_end = pos + len(last_lower)
            after_ok = after_end >= len(body) or not body[after_end].isalpha()
            if before_ok and after_ok:
                # Check not already covered by a full name match
                covered = False
                for ms, me, _, _, _ in matches:
                    if ms <= pos and me >= after_end:
                        covered = True
                        break
                if not covered:
                    matches.append((pos, after_end, chn, eng_orig, chn))
            idx = pos + 1

    # Sort by position, remove overlapping (keep earlier/longer)
    matches.sort(key=lambda x: (x[0], -(x[1] - x[0])))
    filtered = []
    last_end = -1
    for m in matches:
        if m[0] >= last_end:
            filtered.append(m)
            last_end = m[1]

    return filtered


def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original = content

    # Split frontmatter
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            fm = content[:end+3]
            body = content[end+3:]
        else:
            fm = ""
            body = content
    else:
        fm = ""
        body = content

    matches = find_all_matches(body)
    if not matches:
        return original, False

    # Determine which scholars are already introduced
    # A scholar is "already introduced" if their Chinese name appears in the body
    # before their first English match
    first_eng_pos = {}  # chn_name → first English position
    for start, end, chn, eng_orig, key in matches:
        if key not in first_eng_pos or start < first_eng_pos[key]:
            first_eng_pos[key] = start

    already_has_chinese = {}  # chn_name → True if Chinese name exists before English
    for key, eng_pos in first_eng_pos.items():
        chn_pos = body.find(key)
        if chn_pos != -1 and chn_pos < eng_pos:
            already_has_chinese[key] = True
        else:
            already_has_chinese[key] = False

    # Check for existing 中文名（EngName）pattern
    for key in first_eng_pos:
        for _, (chn, eng_orig) in FULL_NAMES.items():
            if chn == key:
                if re.search(re.escape(chn) + r'\s*[（(]\s*' + re.escape(eng_orig) + r'\s*[）)]', body):
                    already_has_chinese[key] = True
                break
        else:
            for last_k, (chn, eng_orig) in LAST_NAMES.items():
                if chn == key:
                    if re.search(re.escape(chn) + r'\s*[（(]\s*' + re.escape(eng_orig) + r'\s*[）)]', body):
                        already_has_chinese[key] = True
                    break

    # Track which scholars we've introduced (first occurrence with annotation)
    introduced = set()

    # Apply replacements from last to first
    for start, end, chn, eng_orig, key in reversed(matches):
        eng_in_text = body[start:end]

        # Check if this match is inside an already-existing 中文名（EngName）pattern
        before = body[max(0, start-30):start]
        if re.search(re.escape(chn) + r'\s*[（(]\s*$', before):
            continue  # Already annotated, skip

        if already_has_chinese.get(key, False) or key in introduced:
            # Just replace English → Chinese
            body = body[:start] + chn + body[end:]
        else:
            # First occurrence: 中文名（EngName）
            body = body[:start] + f"{chn}（{eng_in_text}）" + body[end:]
            introduced.add(key)

    # Clean up double spaces (only around Chinese characters)
    # Pattern: Chinese char + space + Chinese char → remove space
    body = re.sub(r'(?<=[一-鿿）)]) +(?=[一-鿿（【])', '', body)

    result = fm + body
    return result, result != original


def main():
    changed_files = []
    skipped_files = []
    error_files = []

    for f in sorted(os.listdir(CONCEPT_DIR)):
        if not f.endswith('.md'):
            continue
        filepath = os.path.join(CONCEPT_DIR, f)

        try:
            result, changed = process_file(filepath)
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
