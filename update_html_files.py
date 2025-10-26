#!/usr/bin/env python3
"""
Script to update student-version.html and teacher-version.html with new vocabulary data
"""

import json
import re


def load_vocabulary():
    """Load vocabulary from vocab_data.json"""
    with open('vocab_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_vocab_js_array(vocab_data):
    """Generate JavaScript array format for vocabulary"""
    lines = []
    for entry in vocab_data:
        # Escape quotes and special characters in the meaning
        meaning = entry['meaning'].replace('"', '\\"').replace("'", "\\'")
        word = entry['word'].replace('"', '\\"')
        number = entry['number']

        line = f'{{"number": "{number}", "word": "{word}", "meaning": "{meaning}"}}'
        lines.append(line)

    return ",\n".join(lines)


def update_html_file(filename, vocab_data):
    """Update an HTML file with new vocabulary data"""

    print(f"\nUpdating {filename}...")

    # Read the HTML file
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generate new vocabulary JavaScript array
    new_vocab_js = generate_vocab_js_array(vocab_data)

    # Find and replace the vocabData array
    # Pattern: const vocabData = [...];
    pattern = r'(const vocabData = \[)(.*?)(\s*\];)'

    def replace_vocab(match):
        return f"{match.group(1)}\n{new_vocab_js}\n        {match.group(3)}"

    new_content = re.sub(pattern, replace_vocab, content, flags=re.DOTALL)

    if new_content == content:
        print(f"  ⚠️  Warning: No changes made to {filename}")
        return False

    # Write the updated content back
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  ✓ Updated {filename}")
    return True


def main():
    print("Loading vocabulary data...")
    vocab_data = load_vocabulary()
    print(f"Loaded {len(vocab_data)} words")

    # Verify all words have meanings
    empty_meanings = [entry['word'] for entry in vocab_data if not entry.get('meaning', '').strip()]
    if empty_meanings:
        print(f"\n⚠️  Warning: {len(empty_meanings)} words still have empty meanings!")
        print("First 10:", empty_meanings[:10])
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return
    else:
        print("✓ All words have meanings")

    # Update both HTML files
    files_updated = []

    if update_html_file('student-version.html', vocab_data):
        files_updated.append('student-version.html')

    if update_html_file('teacher-version.html', vocab_data):
        files_updated.append('teacher-version.html')

    print(f"\n✅ Successfully updated {len(files_updated)} HTML file(s):")
    for filename in files_updated:
        print(f"  - {filename}")

    print("\n🎉 All vocabulary now has meanings and HTML files are updated!")


if __name__ == '__main__':
    main()
