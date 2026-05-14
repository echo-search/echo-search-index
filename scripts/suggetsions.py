import json
import hashlib
import itertools
from pathlib import Path

OUTPUT_FILE = "echosearch_suggestions.json"

# TARGET
TARGET_COUNT = 8_000_000_000

# PERFORMANCE
FLUSH_INTERVAL = 100_000
BUFFER_SIZE = 1024 * 1024  # 1MB buffer

topics = [
    "translate","meaning","basics","tutorial","guide","how to","examples",
    "definition","calculator","converter","weather","news","lyrics","movies",
    "games","coding","python","javascript","typescript","java","csharp","cpp",
    "golang","rust","swift","kotlin","html","css","react","vue","angular",
    "science","math","history","geography","sports","football","basketball",
    "cricket","tennis","recipes","cooking","baking","health","fitness","gym",
    "nutrition","ai","machine learning","deep learning","space","music",
    "school","revision","biology","chemistry","physics","english","literature",
    "business","finance","stocks","crypto","economics","shopping","reviews",
    "comparison","near me","restaurants","cafes","maps","travel","hotels",
    "jobs","careers","ebooks","streaming","anime","manga","cars",
    "motorcycles","phones","laptops","fashion","design","photography",
    "video editing","photo editing","gaming","esports","cybersecurity",
    "privacy","vpn","cloud computing","docker","kubernetes","linux","windows",
    "macos","android","iphone","startup","marketing","seo","social media",
    "content creation","youtube","tiktok","instagram","study tips",
    "exam prep","college","university","homework","productivity",
    "time management","meditation","gardening","pets","dogs",
    "cats","memes","fun facts","life hacks","automation","robotics",
    "data science","statistics","algebra","geometry","trigonometry",
    "calculus","philosophy","psychology","astronomy","astrophysics",
    "architecture","3d modeling","ui design","ux design","drawing",
    "painting","podcasts","audiobooks","streamers","web development",
    "app development","game development","blockchain","open source",
    "freelancing","remote work","resume","interview","public speaking",
    "debating","language learning","french","spanish","german","arabic",
    "urdu","hindi","japanese","korean","chinese","documentaries",
    "true crime","science experiments","physics equations",
    "chemistry formulas","biology notes","travel hacks","cheap flights",
    "luxury hotels","budget travel","meal prep","weight loss",
    "muscle building","running","cycling","swimming","yoga","pilates",
    "self improvement","motivation","daily routines","minimalism",
    "smart home","electric cars","tesla","apple","samsung","google",
    "microsoft","openai"
]

subjects = [
    "english to spanish","english to french","english to german",
    "english to arabic","english to urdu","english to hindi",
    "english to japanese","english to korean","english to chinese",
    "algebra","geometry","trigonometry","calculus","linear algebra",
    "statistics","probability","web development","frontend development",
    "backend development","full stack development","app development",
    "ios development","android development","linux","windows","macos",
    "ubuntu","debian","gaming pc","custom pc","iphone","android phone",
    "gpu","cpu","machine learning","deep learning",
    "artificial intelligence","data science","football scores",
    "basketball highlights","cricket live scores","tennis rankings",
    "space facts","black holes","galaxies","biology basics",
    "chemistry equations","physics formulas","travel destinations",
    "cheap flights","luxury hotels","budget travel","healthy meals",
    "meal prep","weight training","home workouts","startup ideas",
    "small business","financial literacy","investing","stocks",
    "cryptocurrency","coding interview","data structures","algorithms",
    "cybersecurity","ethical hacking","privacy","vpn","music theory",
    "guitar lessons","piano tutorials","drum lessons",
    "anime recommendations","movie reviews","book summaries",
    "essay writing","resume building","graphic design","logo creation",
    "video editing","photo editing","science experiments","mental maths",
    "public speaking","study tips","exam revision","geography facts",
    "history timeline","world war 2","roman empire","greek mythology",
    "psychology theories","philosophy basics","robotics projects",
    "arduino","raspberry pi","3d printing","smart home setup",
    "electric vehicles","tesla model 3","iphone tips",
    "android tricks","social media growth","youtube channel ideas",
    "tiktok strategy","instagram reels","seo optimization",
    "digital marketing","affiliate marketing","passive income",
    "freelancing guide","remote jobs","interview questions",
    "career advice","college applications","university ranking",
    "scholarships","language learning","french grammar",
    "spanish vocabulary","japanese hiragana","korean hangul",
    "chinese characters","anime streaming","manga websites",
    "gaming setup","minecraft builds","fortnite settings",
    "roblox scripts","valorant aim","cs2 settings","streaming setup"
]

modifiers = [
    "fast","easy","advanced","simple","best","free","online","2026",
    "for beginners","step by step","explained","full guide","examples",
    "tips","ideas","reference","course","tutorial","masterclass",
    "walkthrough","deep dive","cheat sheet","practice problems",
    "summary","detailed","interactive","visual","high quality",
    "ultimate","updated","latest","complete","expert","professional",
    "efficient","quick start","crash course","beginner friendly",
    "real world","production ready","open source","closed source",
    "minimal","modern","classic","creative","powerful","optimized",
    "secure","private","accurate","lightweight","high performance",
    "low latency","clean design","responsive","mobile friendly",
    "desktop friendly","full stack","frontend","backend","ai powered",
    "smart","daily","weekly","top rated","popular","viral",
    "recommended","community favorite","trending","must know",
    "essential","easy to learn","challenging","fun","educational",
    "academic","practical","hands on","live","streaming",
    "downloadable","printable","customizable","beginner to advanced",
    "zero to hero","minimal setup","fully automated","manual setup",
    "ai generated","human written","industry standard",
    "enterprise grade","professional quality","school friendly",
    "student friendly","teacher approved","family friendly"
]

# MASSIVE EXPANSION
for i in range(1, 5001):

    topics.extend([
        f"topic {i}",
        f"advanced topic {i}",
        f"modern topic {i}",
        f"ultimate topic {i}",
        f"professional topic {i}"
    ])

    subjects.extend([
        f"subject {i}",
        f"advanced subject {i}",
        f"enterprise subject {i}",
        f"professional subject {i}",
        f"beginner subject {i}"
    ])

    modifiers.extend([
        f"modifier {i}",
        f"advanced modifier {i}",
        f"optimized modifier {i}",
        f"production modifier {i}",
        f"enterprise modifier {i}"
    ])

patterns = [
    "{topic} {subject}",
    "{topic} {subject} {modifier}",
    "{subject} tutorial",
    "{subject} guide",
    "{subject} basics",
    "{subject} examples",
    "{subject} explained",
    "{subject} online",
    "{subject} free",
    "{subject} course",
    "{subject} advanced guide",
    "{subject} for beginners",
    "{subject} step by step",
    "{subject} crash course",
    "{subject} quick start",
    "{subject} deep dive",
    "{subject} cheatsheet",
    "{subject} interview questions",
    "{subject} practice problems",
    "{subject} exam prep",
    "{subject} notes",
    "{subject} summary",
    "{subject} explained simply",
    "{subject} explained visually",
    "{subject} complete guide",
    "{subject} production ready",
    "{subject} beginner friendly",
    "{subject} advanced concepts",
    "{subject} zero to hero",
    "{subject} latest updates",
    "{subject} trending",
    "{subject} industry standard",
    "{subject} with source code",
    "{subject} project ideas",
    "{subject} mini projects",
    "{topic} and {subject}",
    "{topic} for {subject}",
    "{subject} roadmap",
    "{subject} complete roadmap",
    "{subject} ai powered",
    "{subject} full tutorial",
    "{subject} walkthrough",
    "{subject} real examples",
    "{subject} with answers",
    "{subject} with diagrams",
    "{subject} in depth"
]

def normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())

def hash_text(text: str) -> str:
    return hashlib.blake2b(
        text.encode("utf-8"),
        digest_size=16
    ).hexdigest()

def suggestion_generator():

    for topic, subject, modifier, pattern in itertools.product(
        topics,
        subjects,
        modifiers,
        patterns
    ):

        yield normalize(
            pattern.format(
                topic=topic,
                subject=subject,
                modifier=modifier
            )
        )

def main():

    print("======================================")
    print(" EchoSearch Massive Suggestion Builder")
    print("======================================\n")

    print(f"Topics:     {len(topics):,}")
    print(f"Subjects:   {len(subjects):,}")
    print(f"Modifiers:  {len(modifiers):,}")
    print(f"Patterns:   {len(patterns):,}")

    total_possible = (
        len(topics)
        * len(subjects)
        * len(modifiers)
        * len(patterns)
    )

    print(f"\nTotal possible combinations: {total_possible:,}")
    print(f"Target suggestions:          {TARGET_COUNT:,}\n")

    Path(OUTPUT_FILE).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    generated = 0
    first = True

    # MEMORY SAFE
    seen_hashes = set()
    MAX_HASHES = 5_000_000

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
        buffering=BUFFER_SIZE
    ) as f:

        f.write("[\n")

        for suggestion in suggestion_generator():

            suggestion_hash = hash_text(suggestion)

            if suggestion_hash in seen_hashes:
                continue

            seen_hashes.add(suggestion_hash)

            if len(seen_hashes) >= MAX_HASHES:
                seen_hashes.clear()

            if not first:
                f.write(",\n")

            json.dump(
                suggestion,
                f,
                ensure_ascii=False
            )

            first = False
            generated += 1

            if generated % FLUSH_INTERVAL == 0:

                f.flush()

                print(
                    f"Generated: {generated:,} / {TARGET_COUNT:,}"
                )

            if generated >= TARGET_COUNT:
                break

        f.write("\n]")

    print("\n======================================")
    print(" Generation Complete")
    print("======================================")
    print(f"Saved to: {OUTPUT_FILE}")
    print(f"Total suggestions: {generated:,}")

if __name__ == "__main__":
    main()
