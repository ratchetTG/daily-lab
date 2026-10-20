import random, json, re, sys
from collections import Counter

WORD_CLUES = {
    "SPARE": "Extra tyre in the boot", "SHARE": "Split a secret — or a pizza",
    "SHARP": "Razor-edged — or on the dot", "SHARK": "Loan _____ / Great White",
    "SPARK": "Bright flash / Electrician", "STARK": "Bleak and bare",
    "START": "Jump-_____ / Begin", "SMART": "Street-wise / Sharp-dressed",
    "CHART": "Top 40 list / Sea map", "CHAIR": "Salon seat / Boardroom head",
    "CHAIN": "Bicycle link / Daisy _____", "TRAIN": "Morning rail from Rush",
    "BRAIN": "Grey matter / Mastermind", "GRAIN": "Against the _____ / Wood texture",
    "DRAIN": "Down the _____ / Empty out", "DRAWN": "Pulled — or sketched",
    "DROWN": "Swallow out with noise", "CROWN": "Triple _____ / Royal headpiece",
    "CLOWN": "Class _____ / Circus jester", "CLEAN": "Squeaky _____ / Spotless",
    "CLEAR": "Crystal _____ / Out of the way", "CLEAT": "Football boot stud",
    "CHEAT": "Card shark / Cut corners", "CHEAP": "Dirt _____ / Ryanair seat sale",
    "PEACH": "Stone fruit / Absolute beauty", "REACH": "Out of _____ / Arm's length",
    "REACT": "Respond / Double-take", "HEART": "Change of _____ / Core",
    "HEARD": "Word on the street / Listened", "BEARD": "Five o'clock shadow / Chin hair",
    "BOARD": "Above _____ / Surf plank", "BOAST": "Brag at the bar",
    "COAST": "East _____ / Freewheel", "ROAST": "Sunday carvery / Comedy ribbing",
    "TOAST": "Raise a glass / Burnt bread", "CRANE": "Dublin skyline lifting machine",
    "CRATE": "Wooden packing box", "SLATE": "Clean _____ / Roof tile",
    "STATE": "Mindset / Declare", "STAGE": "West End boards / Phase",
    "STARE": "Blank look / Unblinking gaze", "STORE": "Department shop / Keep safe",
    "STONE": "Blarney rock / 14 pounds", "SHONE": "Glowed brightly",
    "PHONE": "Mobile handset", "PRONE": "Lying face-down / Likely to",
    "PROSE": "Plain writing, not poetry", "POISE": "Cool composure under pressure",
    "NOISE": "White _____ / Racket", "SNORE": "Saw logs at night",
    "SNORT": "Derisive laugh through the nose", "SPORT": "GAA or rugby / Good _____",
    "SHORT": "_____ sight / Brief", "SHIRT": "Collar and cuffs / Stuffed _____",
    "SHIFT": "Night _____ / Gear change", "SIGHT": "Out of _____ / Vision",
    "NIGHT": "Late evening / Owl's shift", "LIGHT": "Green _____ / Weightless",
    "MIGHT": "Pure strength / Maybe", "FIGHT": "Title bout / Scrap",
    "FAITH": "Blind _____ / Trust", "FIFTH": "Plead the _____ / 20%",
    "PITCH": "GAA field / Sales talk", "WITCH": "Halloween broom flyer",
    "WATCH": "Wrist timepiece / Keep an eye on", "CATCH": "_____ 22 / Snag",
    "MATCH": "Game, set and _____ / Swan Vesta", "MARCH": "Spring month / Parade step",
    "PARKS": "Phoenix & St Stephen's", "PARTS": "Spare _____ / Roles",
    "PARTY": "Stag or hen / Celebration", "PAINT": "Wet _____ / Gloss coat",
    "FAINT": "Pass out / Dim", "SAINT": "Patron _____ / Halo wearer",
    "STAIN": "Coffee ring / Wood dye", "SATIN": "Glossy gown fabric",
    "PLANT": "Power station — or fern", "PLANK": "Core floor exercise / Timber",
    "PLANE": "Ryanair jet / Flat surface", "PLATE": "Dinner dish / Car reg",
    "LATER": "See you _____ / Afterwards", "WATER": "Still or sparkling",
    "CATER": "Provide food for an event", "CAPER": "Heist — or pickled bud",
    "PAPER": "Daily news / Rock, _____, scissors", "TAPER": "Fade gradually / Barber's neckline",
    "TIGER": "Celtic _____ / Striped cat", "TIMER": "Egg clock / Stopwatch",
    "TIRED": "Ready for bed after 11 PM", "TRIED": "Put to the test",
    "TRADE": "Swap / Craft", "TREAD": "Tyre grip / Walk softly",
    "TREAT": "Guilty pleasure / Pick up the bill", "GREAT": "Top-notch / Alexander the _____",
    "GRATE": "Cheese shredder / Fireplace iron", "GRACE": "Saving _____ / Elegance",
    "TRACE": "Vanish without a _____", "TRACK": "Sound _____ / Running lane",
    "TRICK": "Magic illusion / Hat-_____", "THICK": "Through _____ and thin",
    "THINK": "Use your head / Ponder", "THANK": "Show gratitude",
    "SHANK": "Lamb cut / Golf mishit"
}

WORDS = [w for w in WORD_CLUES.keys() if len(w) == 5]

def is_strict_4_overlap(w1, w2):
    if w1 == w2: return False
    c1, c2 = Counter(w1), Counter(w2)
    return sum((c1 & c2).values()) == 4

ADJ = {w: [n for n in WORDS if is_strict_4_overlap(w, n)] for w in WORDS}

def generate_vault(vault_id):
    for _ in range(2000):
        path = [random.choice(WORDS)]
        for _ in range(4):
            candidates = [
                n for n in ADJ[path[-1]]
                if n not in path and all(Counter(n) != Counter(prev) for prev in path)
            ]
            if not candidates: break
            path.append(random.choice(candidates))
        if len(path) == 5:
            rungs = [
                {"word": w, "clue": f"{'Rung 1 (Anchor):' if i==0 else f'Rung {i+1}:'} {WORD_CLUES[w]}"}
                for i, w in enumerate(path)
            ]
            return {"id": vault_id, "rungs": rungs}
    raise RuntimeError("Could not find a 5-rung path.")

count = int(sys.argv[1]) if len(sys.argv[1:]) else 30
vaults = [generate_vault(i + 1) for i in range(count)]

with open("vault.html", "r", encoding="utf-8") as f: html = f.read()
new_vaults_js = f"/* VAULTS_START */\nconst VAULTS = {json.dumps(vaults, indent=2)};\n/* VAULTS_END */"
html_updated = re.sub(r"/\* VAULTS_START \*/.*?/\* VAULTS_END \*/", lambda m: new_vaults_js, html, flags=re.DOTALL)
with open("vault.html", "w", encoding="utf-8") as f: f.write(html_updated)
print(f"✅ Injected {count} strict (Keep 4, Drop 1, Add 1) Vaults into vault.html!")
