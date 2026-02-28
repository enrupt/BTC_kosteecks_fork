import re

# ===== Допустимые аккорды =====
ALLOWED_CHORDS = [
    'N', 'X',
    'C:min', 'C', 'C:dim', 'C:aug', 'C:min6', 'C:maj6', 'C:min7', 'C:minmaj7', 'C:maj7', 'C:7', 'C:dim7', 'C:hdim7',
    'C:sus2', 'C:sus4',
    'C#:min', 'C#', 'C#:dim', 'C#:aug', 'C#:min6', 'C#:maj6', 'C#:min7', 'C#:minmaj7', 'C#:maj7', 'C#:7', 'C#:dim7',
    'C#:hdim7', 'C#:sus2', 'C#:sus4',
    'D:min', 'D', 'D:dim', 'D:aug', 'D:min6', 'D:maj6', 'D:min7', 'D:minmaj7', 'D:maj7', 'D:7', 'D:dim7', 'D:hdim7',
    'D:sus2', 'D:sus4',
    'D#:min', 'D#', 'D#:dim', 'D#:aug', 'D#:min6', 'D#:maj6', 'D#:min7', 'D#:minmaj7', 'D#:maj7', 'D#:7', 'D#:dim7',
    'D#:hdim7', 'D#:sus2', 'D#:sus4',
    'E:min', 'E', 'E:dim', 'E:aug', 'E:min6', 'E:maj6', 'E:min7', 'E:minmaj7', 'E:maj7', 'E:7', 'E:dim7', 'E:hdim7',
    'E:sus2', 'E:sus4',
    'F:min', 'F', 'F:dim', 'F:aug', 'F:min6', 'F:maj6', 'F:min7', 'F:minmaj7', 'F:maj7', 'F:7', 'F:dim7', 'F:hdim7',
    'F:sus2', 'F:sus4',
    'F#:min', 'F#', 'F#:dim', 'F#:aug', 'F#:min6', 'F#:maj6', 'F#:min7', 'F#:minmaj7', 'F#:maj7', 'F#:7', 'F#:dim7',
    'F#:hdim7', 'F#:sus2', 'F#:sus4',
    'G:min', 'G', 'G:dim', 'G:aug', 'G:min6', 'G:maj6', 'G:min7', 'G:minmaj7', 'G:maj7', 'G:7', 'G:dim7', 'G:hdim7',
    'G:sus2', 'G:sus4',
    'G#:min', 'G#', 'G#:dim', 'G#:aug', 'G#:min6', 'G#:maj6', 'G#:min7', 'G#:minmaj7', 'G#:maj7', 'G#:7', 'G#:dim7',
    'G#:hdim7', 'G#:sus2', 'G#:sus4',
    'A:min', 'A', 'A:dim', 'A:aug', 'A:min6', 'A:maj6', 'A:min7', 'A:minmaj7', 'A:maj7', 'A:7', 'A:dim7', 'A:hdim7',
    'A:sus2', 'A:sus4',
    'A#:min', 'A#', 'A#:dim', 'A#:aug', 'A#:min6', 'A#:maj6', 'A#:min7', 'A#:minmaj7', 'A#:maj7', 'A#:7', 'A#:dim7',
    'A#:hdim7', 'A#:sus2', 'A#:sus4',
    'B:min', 'B', 'B:dim', 'B:aug', 'B:min6', 'B:maj6', 'B:min7', 'B:minmaj7', 'B:maj7', 'B:7', 'B:dim7', 'B:hdim7',
    'B:sus2', 'B:sus4'
]

# ===== Pitch classes =====
NOTE_TO_INT = {
    'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4,
    'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8,
    'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
}

# Интервальные формулы
CHORD_FORMULAS = {
    '': [0, 4, 7],
    'min': [0, 3, 7],
    'dim': [0, 3, 6],
    'aug': [0, 4, 8],
    '7': [0, 4, 7, 10],
    'maj7': [0, 4, 7, 11],
    'min7': [0, 3, 7, 10],
    'dim7': [0, 3, 6, 9],
    'hdim7': [0, 3, 6, 10],
    'minmaj7': [0, 3, 7, 11],
    'sus2': [0, 2, 7],
    'sus4': [0, 5, 7],
    'min6': [0, 3, 7, 9],
    'maj6': [0, 4, 7, 9],
}


# ===== Парсинг =====
def normalize(chord):
    if chord is None:
        return None

    chord = chord.split('/')[0]
    chord = re.sub(r'add\d+', '', chord)

    # если после ноты идёт цифра — добавляем :
    chord = re.sub(r'^([A-G][b#]?)(\d+)', r'\1:\2', chord)

    chord = chord.replace('m7', ':min7')
    chord = chord.replace('m', ':min')
    chord = chord.replace('maj7', ':maj7')
    chord = chord.replace('maj', ':maj')

    return chord


def parse(chord):
    m = re.match(r'^([A-G][b#]?)(?::(.+))?$', chord)
    if not m:
        return None, None
    root = m.group(1)
    quality = m.group(2) if m.group(2) else ''
    return root, quality


def chord_to_pcset(chord):
    root, quality = parse(chord)
    if root not in NOTE_TO_INT:
        return set()

    base = NOTE_TO_INT[root]
    formula = CHORD_FORMULAS.get(quality, CHORD_FORMULAS[''])

    return {(base + interval) % 12 for interval in formula}


def pc_distance(set1, set2):
    return len(set1.symmetric_difference(set2))


def root_distance(r1, r2):
    i1 = NOTE_TO_INT.get(r1)
    i2 = NOTE_TO_INT.get(r2)
    if i1 is None or i2 is None:
        return 12
    diff = abs(i1 - i2)
    return min(diff, 12 - diff)


def find_closest(chord):
    norm = normalize(chord)
    if norm is None:
        return 'N'

    best = None
    best_score = 999

    root1, _ = parse(norm)
    set1 = chord_to_pcset(norm)

    for allowed in ALLOWED_CHORDS:
        if allowed in ['N', 'X']:
            continue

        root2, _ = parse(allowed)
        set2 = chord_to_pcset(allowed)

        score = pc_distance(set1, set2)
        score += root_distance(root1, root2) * 0.3

        if score < best_score:
            best_score = score
            best = allowed

    return best if best else 'N'
