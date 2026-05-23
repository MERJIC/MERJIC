#!/usr/bin/env python3
"""
统一概念页中学者名的中英对照 v5。

规则：每个学者在该页首次出现为「中文名（英文原名）」，后续只用「中文名」。

策略：一轮扫描，收集所有出现位置，然后统一替换。
"""

import os
import re

CONCEPT_DIR = "/Users/myke/Documents/MERJIC/概念库/概念页"

# 统一键（小写）→ (中文名, 英文原名)
SCHOLARS = {
    "agamben": ("阿甘本", "Agamben"),
    "althusser": ("阿尔都塞", "Althusser"),
    "arendt": ("阿伦特", "Arendt"),
    "badiou": ("巴迪欧", "Badiou"),
    "bakhtin": ("巴赫金", "Bakhtin"),
    "baudrillard": ("鲍德里亚", "Baudrillard"),
    "bauman": ("鲍曼", "Bauman"),
    "beauvoir": ("波伏娃", "Beauvoir"),
    "benjamin": ("本雅明", "Benjamin"),
    "berger": ("伯格", "Berger"),
    "bourdieu": ("布迪厄", "Bourdieu"),
    "butler": ("巴特勒", "Butler"),
    "camus": ("加缪", "Camus"),
    "carl schmitt": ("卡尔·施密特", "Carl Schmitt"),
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
    "hume": ("休谟", "Hume"),
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
    "lukacs": ("卢卡奇", "Lukács"),
    "lyotard": ("利奥塔", "Lyotard"),
    "macintyre": ("麦金太尔", "MacIntyre"),
    "malinowski": ("马林诺夫斯基", "Malinowski"),
    "marcuse": ("马尔库塞", "Marcuse"),
    "marx": ("马克思", "Marx"),
    "mauss": ("莫斯", "Mauss"),
    "merleau-ponty": ("梅洛-庞蒂", "Merleau-Ponty"),
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
    "ranciere": ("朗西埃", "Rancière"),
    "rawls": ("罗尔斯", "Rawls"),
    "ricoeur": ("利科", "Ricoeur"),
    "rogers": ("罗杰斯", "Rogers"),
    "rosa": ("罗萨", "Rosa"),
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
    "zizek": ("齐泽克", "Žižek"),
    "montesquieu": ("孟德斯鸠", "Montesquieu"),
    "machiavelli": ("马基雅维利", "Machiavelli"),
    "chomsky": ("乔姆斯基", "Chomsky"),
    "skinner": ("斯金纳", "Skinner"),
    "lakatos": ("拉卡托斯", "Lakatos"),
    "dewey": ("杜威", "Dewey"),
    "russell": ("罗素", "Russell"),
    "darwin": ("达尔文", "Darwin"),
}


def split_fm(content):
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            return content[:end+3], content[end+3:]
    return "", content


def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original = content
    fm, body = split_fm(content)

    # Collect all scholar occurrences in the body
    # Each occurrence: (abs_start, abs_end, chn_name, eng_name, match_type)
    # match_type: "eng" = pure English, "chn_annotated" = 中文名（Eng）, "chn_bare" = pure 中文名
    occurrences = []

    # Match English names (longer keys first to prefer full names)
    sorted_keys = sorted(SCHOLARS.keys(), key=lambda x: -len(x))

    # Track which body ranges are already covered by a longer match
    covered_ranges = []  # list of (start, end)

    def is_covered(s, e):
        return any(s >= cs and e <= ce for cs, ce in covered_ranges)

    for key in sorted_keys:
        chn, eng = SCHOLARS[key]

        parts = key.split()
        if len(parts) > 1:
            pattern = r'(?<![a-zA-Z\w])(' + r'\s+'.join(re.escape(p) for p in parts) + r')(?![a-zA-Z\w])'
        else:
            pattern = r'(?<![a-zA-Z\w])(' + re.escape(key) + r')(?![a-zA-Z\w])'

        idx = 0
        while True:
            m = re.search(pattern, body[idx:], re.IGNORECASE)
            if not m:
                break
            abs_start = idx + m.start(1)
            abs_end = idx + m.end(1)

            # Skip if position already covered by a longer match
            if is_covered(abs_start, abs_end):
                idx = abs_end
                continue

            # Skip if inside 中文名（EngName）pattern
            before = body[max(0, abs_start-40):abs_start]
            after = body[abs_end:min(len(body), abs_end+20)]
            if re.search(re.escape(chn) + r'\s*[（(]\s*$', before) and re.match(r'\s*[）)]', after):
                covered_ranges.append((abs_start, abs_end))
                idx = abs_end
                continue

            occurrences.append((abs_start, abs_end, chn, eng, "eng"))
            covered_ranges.append((abs_start, abs_end))
            idx = abs_end

    # Match annotated Chinese names: 中文名（EngName）
    for key in sorted_keys:
        chn, eng = SCHOLARS[key]
        # Pattern: 中文名 followed by （ or ( then EngName then ） or )
        pat = re.escape(chn) + r'\s*[（(]\s*' + re.escape(eng) + r'\s*[）)]'
        for m in re.finditer(pat, body):
            # Check not already covered
            abs_start, abs_end = m.start(), m.end()
            if is_covered(abs_start, abs_end):
                continue
            occurrences.append((abs_start, abs_end, chn, eng, "chn_annotated"))
            covered_ranges.append((abs_start, abs_end))

    # Match bare Chinese names: 中文名 without （EngName）following
    for key in sorted_keys:
        chn, eng = SCHOLARS[key]
        # Negative lookahead: not followed by （ or ( with eng name
        # Negative lookbehind: not preceded by a Chinese char (to avoid matching
        # 施密特 inside 卡尔·施密特)
        pat = r'(?<![一-鿿·])' + re.escape(chn) + r'(?!\s*[（(]\s*' + re.escape(eng) + r'\s*[）)])'
        for m in re.finditer(pat, body):
            abs_start, abs_end = m.start(), m.end()
            # Check not already covered by another match
            if is_covered(abs_start, abs_end):
                continue
            occurrences.append((abs_start, abs_end, chn, eng, "chn_bare"))
            covered_ranges.append((abs_start, abs_end))

    # Sort all occurrences by position
    occurrences.sort(key=lambda x: x[0])

    # Group by scholar (chn_name)
    from collections import defaultdict
    by_scholar = defaultdict(list)
    for occ in occurrences:
        by_scholar[occ[2]].append(occ)

    # For each scholar, determine what to do
    replacements = []  # (start, end, replacement_text) — will apply from last to first

    for chn, occs in by_scholar.items():
        eng = occs[0][3]

        # Find the first occurrence
        first = occs[0]

        for i, (start, end, _, _, mtype) in enumerate(occs):
            if i == 0:
                # First occurrence: ensure it's 中文名（EngName）
                if mtype == "chn_annotated":
                    pass  # Already correct
                elif mtype == "chn_bare":
                    replacements.append((start, end, f"{chn}（{eng}）"))
                elif mtype == "eng":
                    replacements.append((start, end, f"{chn}（{eng}）"))
            else:
                # Subsequent: just 中文名, strip any annotation
                if mtype == "chn_annotated":
                    # Strip the （EngName） part
                    m = re.match(r'(.*?' + re.escape(chn) + r')\s*[（(]\s*' + re.escape(eng) + r'\s*[）)]',
                                 body[start:end])
                    if m:
                        replacements.append((start, end, chn))
                    else:
                        # Fallback: replace whole match with chn
                        replacements.append((start, end, chn))
                elif mtype == "chn_bare":
                    pass  # Already just Chinese name
                elif mtype == "eng":
                    replacements.append((start, end, chn))

    if not replacements:
        return original, False

    # Apply replacements from last to first to preserve positions
    replacements.sort(key=lambda x: -x[0])
    for start, end, replacement in replacements:
        body = body[:start] + replacement + body[end:]

    # Cleanup: remove double spaces around Chinese chars
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
