#!/usr/bin/env python3
"""
Script to replace [NEEDS REVIEW] meanings with proper child-friendly definitions
"""

import json

# Child-friendly meanings for the 112 words that need review
REVIEW_MEANINGS = {
    "Biased": "showing unfair favor to one side",
    "bicycle": "a two-wheeled vehicle you pedal",
    "Biodiversity": "variety of different plants and animals",
    "Blossom": "a flower on a tree or plant",
    "Britain": "an island nation in Europe; UK",
    "communicate": "to share information or feelings",
    "community": "a group of people living together",
    "company": "a business; being with others",
    "completely": "totally; entirely",
    "Delude": "to trick or mislead someone",
    "demolished": "completely destroyed",
    "Demure": "shy and modest",
    "dictionary": "a book of word definitions",
    "digest": "to break down food; to understand",
    "dilapidated": "falling apart; in ruins",
    "divine": "godly; extremely good",
    "divinity": "the state of being a god",
    "domestic": "relating to home or country",
    "Dormant": "sleeping; inactive",
    "dose": "a measured amount of medicine",
    "Facebook": "a social media website",
    "fact": "something that is true",
    "Factor": "something that contributes to a result",
    "Factual": "based on facts; true",
    "Flourish": "to grow well; to thrive",
    "fragment": "a small broken piece",
    "Gallant": "brave and noble",
    "Gargantuan": "extremely large; gigantic",
    "handkerchief": "a cloth for wiping your nose",
    "Haphazardly": "in a random, careless way",
    "Harass": "to bother or annoy repeatedly",
    "Harmonious": "peaceful; working well together",
    "https": "secure web address protocol",
    "Ignominious": "shameful; embarrassing",
    "ignorant": "lacking knowledge",
    "Illustrious": "famous and respected",
    "inedible": "not safe or suitable to eat",
    "Inevitable": "certain to happen; unavoidable",
    "Infamous": "famous for bad reasons",
    "interrupt": "to break in; to stop someone talking",
    "Intervene": "to step in to help or stop something",
    "Intimidate": "to frighten or threaten",
    "liable": "responsible; likely to",
    "liberal": "open-minded; generous",
    "liberty": "freedom",
    "library": "a place with books to borrow",
    "meant": "intended; planned",
    "Meddle": "to interfere in others' business",
    "Melancholy": "deep sadness",
    "Mellow": "calm and gentle",
    "Mutter": "to speak quietly and unclearly",
    "Mutual": "shared by both sides",
    "mysterious": "strange; hard to explain",
    "Naive": "innocent; inexperienced",
    "odour": "a smell",
    "offend": "to hurt someone's feelings",
    "omen": "a sign of future events",
    "online": "connected to the internet",
    "palaeontologist": "a scientist who studies fossils",
    "passive": "inactive; accepting without resistance",
    "pasture": "grassland for animals to graze",
    "Pattern": "a repeated design or arrangement",
    "peak": "the top; highest point",
    "plunder": "to steal goods, especially in war",
    "plunge": "to dive or fall suddenly",
    "Plus": "in addition to; positive",
    "Podcast": "audio show you can download",
    "programme": "a plan; a TV or radio show",
    "prohibit": "to forbid; to ban",
    "prominent": "important; standing out",
    "promote": "to advertise; to advance",
    "Rapid": "very fast; quick",
    "rare": "uncommon; not often found",
    "Ravenous": "extremely hungry",
    "resources": "available supplies or materials",
    "restaurant": "a place where you buy meals",
    "Restlessness": "inability to relax or stay still",
    "restore": "to bring back to original state",
    "sane": "mentally healthy; rational",
    "sanitary": "clean and hygienic",
    "Sarcasm": "mocking humor; saying the opposite",
    "signature": "your written name",
    "Silhouette": "a dark outline or shadow",
    "sincere": "honest and genuine",
    "sincerely": "in an honest way",
    "Spotify": "a music streaming service",
    "stubborn": "refusing to change; determined",
    "Stumble": "to trip or walk unsteadily",
    "sturdy": "strong and solid",
    "subdued": "quiet; controlled",
    "Susceptible": "easily affected or influenced",
    "suspect": "to believe something may be true",
    "suspend": "to hang; to temporarily stop",
    "Sustainable": "able to continue without damage",
    "teamkeen": "eager to work with others",
    "theexamcoach": "an exam preparation tutor",
    "their": "belonging to them",
    "Tireless": "never getting tired; persistent",
    "tomorrow": "the day after today",
    "Tone": "the quality of sound or mood",
    "torment": "to cause severe suffering",
    "uniform": "identical clothing; consistent",
    "union": "a joining together; workers' group",
    "unite": "to join together",
    "Unsteadiness": "lack of balance or stability",
    "visit": "to go to see someone or someplace",
    "Vital": "essential; very important",
    "Vocab": "short for vocabulary; words",
    "vocabulary": "all the words you know",
    "your": "belonging to you",
    "YouTube": "a video sharing website",
    "Zoom": "a video calling app; to move fast",
}


def fix_review_words():
    """Replace [NEEDS REVIEW] meanings with proper definitions"""

    # Load vocabulary
    with open('vocab_data.json', 'r', encoding='utf-8') as f:
        vocab_data = json.load(f)

    fixed_count = 0
    not_found = []

    print(f"Processing {len(vocab_data)} words...")

    for entry in vocab_data:
        word = entry['word']
        meaning = entry.get('meaning', '')

        if '[NEEDS REVIEW]' in meaning:
            if word in REVIEW_MEANINGS:
                entry['meaning'] = REVIEW_MEANINGS[word]
                fixed_count += 1
                print(f"  ✓ Fixed: {word}")
            else:
                not_found.append(word)
                print(f"  ⚠️  Not found in mapping: {word}")

    # Save updated vocabulary
    with open('vocab_data.json', 'w', encoding='utf-8') as f:
        json.dump(vocab_data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Fixed {fixed_count} words")

    if not_found:
        print(f"⚠️  {len(not_found)} words still need manual review:")
        for word in not_found:
            print(f"  - {word}")
    else:
        print("✓ All review words have been fixed!")

    # Verify no more [NEEDS REVIEW] tags
    needs_review = [entry['word'] for entry in vocab_data if '[NEEDS REVIEW]' in entry.get('meaning', '')]
    print(f"\nFinal check: {len(needs_review)} words still need review")


if __name__ == '__main__':
    fix_review_words()
