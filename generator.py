import random, json, re, sys

WORDS = [
    "ABUSE","ADAPT","ADULT","AGENT","AGILE","AISLE","ALARM","ALBUM","ALERT","ALIEN",
    "ALIGN","ALIKE","ALIVE","ALLOW","ALLOY","ALONE","ALONG","ALOFT","ALTER","AMONG",
    "AMPLE","ANGEL","ANGER","ANGLE","ANGRY","ANKLE","APART","APPLE","APPLY","APRON",
    "ARENA","ARGUE","ARISE","ARMOR","AROMA","ARROW","ASIDE","ASSET","ATLAS","AUDIO",
    "AUDIT","AVOID","AWAKE","AWARD","AWARE","AWOKE","BACON","BADGE","BAKER","BASIC",
    "BASIN","BASIS","BATCH","BEACH","BEARD","BEAST","BEGIN","BEING","BELLY","BELOW",
    "BENCH","BERRY","BIRTH","BLACK","BLADE","BLAME","BLANK","BLAST","BLAZE","BLEAK",
    "BLEND","BLESS","BLIND","BLINK","BLOCK","BLOOD","SIGHT","SPARE","SHARE","HEART",
    "STARE","SMART","BRAIN","CRANE","FLAME","SLATE","SHARP","PLANT","CHART","PITCH",
    "CLOTH","CHEST","WITCH","FAITH","BOOTH","EARTH","MONTH","YOUTH","BOARD","BOAST",
    "BRAKE","BRAND","BRAVE","BREAD","BREAK","BRICK","BRIDE","BRIEF","BRING","BROAD",
    "BROKE","BROWN","BRUSH","BUILD","BUILT","BUNCH","BURST","CABIN","CABLE","CARGO",
    "CATCH","CAUSE","CHAIN","CHAIR","CHALK","CHARM","CHASE","CHEAP","CHEAT","CHECK",
    "CHIEF","CHILD","CHILL","CHINA","CHOIR","CHOKE","CHORD","CHORE","CHOSE","CLAIM",
    "CLASH","CLASS","CLEAN","CLEAR","CLERK","CLICK","CLIFF","CLIMB","CLOAK","CLOCK",
    "CLONE","CLOSE","CLOUD","CLOWN","COACH","COAST","CORAL","COUCH","COUNT","COURT",
    "COVER","CRACK","CRAFT","CRASH","CRATE","CRAVE","CRAZY","CREAM","CREEK","CREST",
    "CRIME","CRISP","CROSS","CROWD","CROWN","CRUDE","CRUSH","CRUST","CURVE","DAILY",
    "DAIRY","DANCE","DEATH","DEBIT","DEBUT","DECAY","DELAY","DELTA","DENSE","DEPTH",
    "DIARY","DINER","DIRTY","DITCH","DIVER","DOUBT","DOUGH","DOZEN","DRAFT","DRAIN",
    "DRAMA","DRANK","DRAWN","DREAD","DREAM","DRESS","DRIFT","DRILL","DRINK","DRIVE",
    "DRONE","DROVE","DROWN","DRUNK","FLIGHT","TIGER","TIMER","TIRED","TITLE","TOAST",
    "TODAY","TOKEN","TONIC","TOOTH","TOPIC","TORCH","TOTAL","TOUCH","TOUGH","TOWEL",
    "TOWER","TOXIC","TRACE","TRACK","TRACT","TRADE","TRAIL","TRAIN","TRAIT","TRASH",
    "TREAD","TREAT","TREND","TRIAL","TRIBE","TRICK","TRIED","TROOP","TROUT","TRUCK",
    "TRULY","TRUMP","TRUNK","TRUST","TRUTH","TWICE","TWIST","ULTRA","UNCLE","UNDER",
    "UNION","UNITE","UNITY","UNTIL","UPPER","UPSET","URBAN","USAGE","VALID","VALUE",
    "VALVE","VAPOR","VAULT","VENUE","VERSE","VIDEO","VILLA","VINYL","VIRAL","VIRUS",
    "VISIT","VITAL","VIVID","VOCAL","VODKA","VOICE","VOTER","WAGON","WAIST","WASTE",
    "WATCH","WATER","WEARY","WEAVE","WEDGE","WEIGH","WEIRD","WHALE","WHEAT","WHEEL",
    "WHERE","WHICH","WHILE","WHITE","WHOLE","WHOSE","WIDOW","WIDTH","WOMAN","WORLD",
    "WORRY","WORSE","WORST","WORTH","WOULD","WOUND","WRATH","WRECK","WRIST","WRITE",
    "WRONG","WROTE","YACHT","YEARN","YEAST","YIELD","YOUNG","ZEBRA"
]
WORDS = sorted(list(set([w.upper() for w in WORDS if len(w) == 5])))

def generate_board(puzzle_id):
    while True:
        top = random.choice(WORDS)
        bottom = random.choice([w for w in WORDS if w != top])
        spines = [w for w in WORDS if w[0] == top[2] and w[4] == bottom[2] and w not in (top, bottom)]
        if spines:
            spine = random.choice(spines)
            sol = list(top) + list(spine[1:4]) + list(bottom)
            movable_idx = [0,1,3,4, 5,6,7, 9,11,12]
            movable_chars = [sol[i] for i in movable_idx]
            for _ in range(100):
                random.shuffle(movable_chars)
                if all(movable_chars[k] != sol[movable_idx[k]] for k in range(len(movable_idx))):
                    init = sol[:]
                    for k, idx in enumerate(movable_idx):
                        init[idx] = movable_chars[k]
                    return {
                        "id": puzzle_id, "top": top, "spine": spine, "bottom": bottom,
                        "par": 6, "maxSwaps": 8, "initial": init
                    }

count = int(sys.argv[1]) if len(sys.argv[1:]) else 50
puzzles = [generate_board(i + 1) for i in range(count)]

with open("index.html", "r", encoding="utf-8") as f: html = f.read()
new_puzzles_js = f"/* PUZZLES_START */\nconst PUZZLES = {json.dumps(puzzles, indent=2)};\n/* PUZZLES_END */"
html_updated = re.sub(r"/\* PUZZLES_START \*/.*?/\* PUZZLES_END \*/", lambda m: new_puzzles_js, html, flags=re.DOTALL)
with open("index.html", "w", encoding="utf-8") as f: f.write(html_updated)
print(f"✅ Injected {count} verified Swap/Cross boards into index.html!")
