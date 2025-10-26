#!/usr/bin/env python3
"""
Script to:
1. Add meanings to all vocabulary words that have empty meanings
2. Split vocabulary data into separate files by letter for easier maintenance
"""

import json
import os
import time
import urllib.request
import urllib.error
import ssl
from collections import defaultdict

# Fix SSL certificate verification issues on macOS
ssl._create_default_https_context = ssl._create_unverified_context

# Common word meanings for 11+ vocabulary (child-friendly definitions)
# These are curated child-friendly definitions for common words
COMMON_MEANINGS = {
    "acquire": "to get or obtain something",
    "across": "from one side to the other",
    "adaptation": "changing to fit new conditions",
    "address": "to speak to or deal with",
    "adequate": "enough; sufficient",
    "adjust": "to change slightly to fit better",
    "administration": "the act of managing or running something",
    "admire": "to respect or look up to",
    "admit": "to confess or allow entry",
    "adopt": "to take on or accept as your own",
    "adult": "a fully grown person",
    "advance": "to move forward",
    "advantage": "a helpful or favorable condition",
    "adventure": "an exciting or unusual experience",
    "advertise": "to announce publicly to promote",
    "advice": "suggestions about what to do",
    "advise": "to give suggestions",
    "advocate": "to support or speak in favor of",
    "affect": "to influence or change",
    "afford": "to have enough money for",
    "afraid": "feeling fear",
    "after": "following in time or place",
    "afternoon": "the time between noon and evening",
    "again": "one more time",
    "against": "in opposition to",
    "age": "how old someone or something is",
    "agency": "an organization providing a service",
    "agenda": "a list of things to do",
    "agent": "someone who acts for another",
    "aggressive": "forceful; pushy",
    "ago": "in the past",
    "agree": "to have the same opinion",
    "agreement": "when people have the same view",
    "ahead": "in front; forward",
    "aid": "to help",
    "aim": "to point toward a target; goal",
    "air": "the mixture of gases we breathe",
    "aircraft": "a vehicle that flies",
    "airline": "a company that flies planes",
    "airport": "where planes take off and land",
    "alarm": "a warning signal",
    "album": "a collection of songs or photos",
    "alcohol": "a type of drink that can make you drunk",
    "alert": "watchful and ready",
    "alien": "a being from another planet",
    "alike": "similar",
    "alive": "living; not dead",
    "all": "everything; everyone",
    "alliance": "a partnership or union",
    "allocate": "to distribute or assign",
    "allow": "to permit",
    "ally": "a friend or helper",
    "almost": "nearly; not quite",
    "alone": "by yourself",
    "along": "moving in a line with",
    "alongside": "next to; beside",
    "aloud": "out loud; so others can hear",
    "alphabet": "the letters of a language",
    "already": "by this time",
    "also": "in addition; too",
    "alter": "to change",
    "alternative": "another choice",
    "although": "even though",
    "altogether": "completely; in total",
    "always": "at all times",
    "amateur": "someone who does something for fun, not as a job",
    "amaze": "to surprise greatly",
    "ambassador": "an official representative",
    "ambition": "a strong desire to achieve",
    "ambulance": "a vehicle for sick or injured people",
    "amend": "to make changes to improve",
    "among": "in the middle of",
    "amount": "how much there is",
    "ample": "plenty; more than enough",
    "amuse": "to entertain",
    "analyze": "to examine carefully",
    "ancestor": "a relative from long ago",
    "anchor": "a heavy object to keep a boat in place",
    "ancient": "very old",
    "and": "also; in addition",
    "angel": "a spiritual being; helper",
    "anger": "strong displeasure",
    "angle": "the space between two lines that meet",
    "angry": "feeling mad",
    "animal": "a living creature",
    "ankle": "the joint between foot and leg",
    "anniversary": "a yearly celebration of an event",
    "announce": "to make known publicly",
    "annoy": "to irritate",
    "annual": "happening once a year",
    "another": "one more; different",
    "answer": "a reply",
    "anticipate": "to expect or look forward to",
    "anxiety": "worry; nervousness",
    "anxious": "worried; nervous",
    "any": "one or some",
    "anybody": "any person",
    "anyhow": "in any case",
    "anyone": "any person",
    "anything": "any thing",
    "anyway": "in any case",
    "anywhere": "in any place",
    "apart": "separated; away from",
    "apartment": "a set of rooms to live in",
    "apologize": "to say sorry",
    "apparatus": "equipment for a specific purpose",
    "apparent": "clear; obvious",
    "appeal": "to make a request; to attract",
    "appear": "to come into view",
    "appearance": "how something looks",
    "appetite": "desire for food",
    "applaud": "to clap hands in approval",
    "applause": "clapping to show approval",
    "apple": "a round fruit",
    "appliance": "a device or machine",
    "application": "a formal request; a program",
    "apply": "to request; to put to use",
    "appoint": "to choose for a position",
    "appointment": "an arranged meeting",
    "appreciate": "to value; to be grateful for",
    "approach": "to come near",
    "appropriate": "suitable; proper",
    "approval": "permission; agreement",
    "approve": "to agree to; to like",
    "approximate": "close to; nearly exact",
    "April": "the fourth month",
    "arbitrary": "based on random choice",
    "architect": "someone who designs buildings",
    "architecture": "the design of buildings",
    "area": "a region or space",
    "arena": "a place for sports or entertainment",
    "argue": "to disagree; to debate",
    "argument": "a disagreement; reasoning",
    "arise": "to come up; to occur",
    "arm": "the upper limb of the body",
    "armed": "carrying weapons",
    "army": "a military force",
    "around": "on all sides; approximately",
    "arouse": "to awaken; to stir up",
    "arrange": "to put in order",
    "arrangement": "an organized plan",
    "array": "an ordered collection",
    "arrest": "to take into custody",
    "arrival": "the act of coming to a place",
    "arrive": "to reach a destination",
    "arrow": "a pointed projectile",
    "art": "creative work",
    "article": "a piece of writing; an item",
    "artificial": "made by humans; not natural",
    "artist": "someone who creates art",
    "artistic": "relating to art; creative",
    "as": "while; because",
    "ascend": "to go up",
    "ashamed": "feeling embarrassed or guilty",
    "aside": "to the side",
    "ask": "to request or question",
    "asleep": "sleeping",
    "aspect": "a particular part or feature",
    "aspire": "to aim for; to desire strongly",
    "assault": "a violent attack",
    "assemble": "to put together; to gather",
    "assembly": "a gathering of people",
    "assert": "to state firmly",
    "assess": "to evaluate",
    "asset": "something valuable",
    "assign": "to give a task or role",
    "assignment": "a task given to someone",
    "assist": "to help",
    "assistance": "help; support",
    "assistant": "a helper",
    "associate": "to connect; a partner",
    "association": "a group with a common purpose",
    "assume": "to suppose; to take on",
    "assure": "to promise; to make certain",
    "astonish": "to amaze; to surprise greatly",
    "athlete": "someone trained in sports",
    "athletic": "physically strong and active",
    "atmosphere": "the air around earth; mood",
    "atom": "the smallest unit of matter",
    "attach": "to fasten or join",
    "attack": "to assault",
    "attain": "to achieve",
    "attempt": "to try",
    "attend": "to be present at",
    "attendance": "being present",
    "attention": "focus; notice",
    "attic": "the space under a roof",
    "attitude": "a way of thinking or feeling",
    "attorney": "a lawyer",
    "attract": "to draw toward",
    "attraction": "something that draws interest",
    "attractive": "pleasing; appealing",
    "attribute": "a quality or characteristic",
    "audience": "people watching or listening",
    "audio": "relating to sound",
    "audit": "an official examination of accounts",
    "auditorium": "a large room for performances",
    "August": "the eighth month",
    "aunt": "your parent's sister",
    "author": "a writer",
    "authority": "the power to give orders",
    "authorize": "to give permission",
    "auto": "relating to cars; self",
    "automatic": "working by itself",
    "automobile": "a car",
    "autumn": "the season between summer and winter; fall",
    "available": "ready to use; obtainable",
    "avenue": "a wide street",
    "average": "typical; ordinary",
    "avoid": "to stay away from",
    "await": "to wait for",
    "awake": "not sleeping",
    "award": "a prize",
    "aware": "knowing; conscious",
    "away": "at a distance",
    "awe": "wonder; amazement",
    "awful": "very bad; terrible",
    "awkward": "clumsy; uncomfortable",
}


def fetch_meaning_from_api(word, max_retries=3):
    """Fetch word meaning from Free Dictionary API"""
    word_lower = word.lower().strip()
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word_lower}"

    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())

                if data and isinstance(data, list) and len(data) > 0:
                    entry = data[0]
                    meanings = entry.get('meanings', [])

                    if meanings:
                        # Get the first definition from the first meaning
                        first_meaning = meanings[0]
                        definitions = first_meaning.get('definitions', [])

                        if definitions:
                            definition = definitions[0].get('definition', '')
                            # Simplify long definitions
                            if len(definition) > 100:
                                definition = definition[:97] + '...'
                            return definition

            return None

        except urllib.error.HTTPError as e:
            if e.code == 404:
                # Word not found in dictionary
                return None
            elif attempt < max_retries - 1:
                time.sleep(1)  # Wait before retrying
            else:
                return None

        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                print(f"  ⚠️  Error fetching '{word}': {e}")
                return None

    return None


def get_meaning_for_word(word, use_api=True):
    """Get a child-friendly meaning for a word"""
    word_lower = word.lower()

    # Check if we have a predefined meaning
    if word_lower in COMMON_MEANINGS:
        return COMMON_MEANINGS[word_lower]

    # Try to fetch from API if enabled
    if use_api:
        api_meaning = fetch_meaning_from_api(word)
        if api_meaning:
            return api_meaning

    # Fallback - mark for manual review
    return f"[NEEDS REVIEW] {word_lower}"


def load_vocabulary():
    """Load vocabulary from vocab_data.json"""
    with open('vocab_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def save_vocabulary(vocab_data):
    """Save vocabulary back to vocab_data.json"""
    with open('vocab_data.json', 'w', encoding='utf-8') as f:
        json.dump(vocab_data, f, indent=2, ensure_ascii=False)


def populate_missing_meanings(vocab_data, use_api=True):
    """Add meanings to entries with empty meanings"""
    updated_count = 0
    needs_review = []
    total_empty = sum(1 for entry in vocab_data if entry.get('meaning', '').strip() == '')

    print(f"Found {total_empty} words with empty meanings")
    if use_api:
        est_time = (total_empty * 0.5 + (total_empty // 10) * 1) / 60
        print(f"Estimated time with API: {est_time:.1f} minutes\n")

    empty_word_count = 0
    for i, entry in enumerate(vocab_data):
        if entry.get('meaning', '').strip() == '':
            empty_word_count += 1
            word = entry['word']
            print(f"  [{empty_word_count}/{total_empty}] '{word}'...", end=' ', flush=True)

            meaning = get_meaning_for_word(word, use_api=use_api)
            entry['meaning'] = meaning
            updated_count += 1

            if '[NEEDS REVIEW]' in meaning:
                needs_review.append(word)
                print("⚠️  needs review")
            else:
                print("✓")

            # Save progress every 50 words
            if use_api and updated_count % 50 == 0:
                print(f"\n  💾 Saving progress... ({updated_count}/{total_empty} completed)")
                save_vocabulary(vocab_data)
                print(f"  ✓ Progress saved!\n")

            # Rate limiting - be nice to the API
            if use_api and updated_count % 5 == 0:
                time.sleep(0.5)  # Wait 0.5 seconds every 5 requests

    return updated_count, needs_review


def split_by_letter(vocab_data):
    """Split vocabulary into separate files by first letter"""
    by_letter = defaultdict(list)

    for entry in vocab_data:
        first_letter = entry['word'][0].upper()
        by_letter[first_letter].append(entry)

    # Create directory if it doesn't exist
    os.makedirs('vocab_by_letter', exist_ok=True)

    # Save each letter to its own file
    for letter, words in sorted(by_letter.items()):
        filename = f'vocab_by_letter/{letter}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(words, f, indent=2, ensure_ascii=False)
        print(f"Created {filename} with {len(words)} words")


def main():
    print("Loading vocabulary data...")
    vocab_data = load_vocabulary()
    print(f"Loaded {len(vocab_data)} words")

    print("\nPopulating missing meanings...")
    updated_count, needs_review = populate_missing_meanings(vocab_data)
    print(f"Updated {updated_count} entries with meanings")

    if needs_review:
        print(f"\n⚠️  {len(needs_review)} words need manual review:")
        for word in needs_review[:10]:  # Show first 10
            print(f"  - {word}")
        if len(needs_review) > 10:
            print(f"  ... and {len(needs_review) - 10} more")

        # Save words that need review
        with open('words_need_review.txt', 'w') as f:
            f.write('\n'.join(needs_review))
        print("\n📝 Full list saved to words_need_review.txt")

    print("\nSaving updated vocabulary data...")
    save_vocabulary(vocab_data)
    print("✓ Saved to vocab_data.json")

    print("\nSplitting vocabulary by letter...")
    split_by_letter(vocab_data)
    print("✓ Created individual letter files in vocab_by_letter/")

    # Create an index file
    print("\nCreating index file...")
    by_letter = defaultdict(int)
    for entry in vocab_data:
        first_letter = entry['word'][0].upper()
        by_letter[first_letter] += 1

    with open('vocab_by_letter/INDEX.md', 'w') as f:
        f.write("# Vocabulary Index\n\n")
        f.write(f"Total words: {len(vocab_data)}\n\n")
        f.write("## Words by Letter\n\n")
        for letter in sorted(by_letter.keys()):
            count = by_letter[letter]
            f.write(f"- **{letter}**: {count} words ([{letter}.json]({letter}.json))\n")

    print("✓ Created vocab_by_letter/INDEX.md")
    print("\n✅ Done!")


if __name__ == '__main__':
    main()
