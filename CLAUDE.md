# Claude Code Documentation

This document contains important information about the 11+ Vocabulary Flashcards project structure and data storage.

## Project Overview

Interactive vocabulary flashcard webapp with 1,193 essential words for 11+ exam preparation.

**Live Site:** https://vocabulary-production-58bc.up.railway.app
**GitHub Repo:** https://github.com/sbenodiz/vocabulary

## Vocabulary Data Storage

The vocabulary data is stored in multiple locations:

### 1. Source Data Files

- **`vocab_data.json`** (87KB)
  - Master source file with all 1,193 words
  - JSON format: `[{"number": "1", "word": "abandon", "meaning": "give up; leave behind"}, ...]`
  - This is the canonical data source

- **`vocab_array.js`** (66KB)
  - JavaScript version of the vocabulary
  - Used for generating/updating HTML files
  - Format: `const vocabData = [{...}, {...}];`

### 2. Embedded in HTML Files

The vocabulary is **embedded directly** in these files (self-contained):

- **`student-version.html`** - Full vocab array in JavaScript (lines ~518-1194)
- **`teacher-version.html`** - Full vocab array in JavaScript (lines ~518-1194)
- **`index.html`** - Landing page (no vocab data, just links)

**Why embedded?**
- ✅ Works completely offline
- ✅ No external HTTP requests needed
- ✅ Faster initial load
- ✅ Easier deployment (just static HTML)

### 3. User Progress Data

- **Browser localStorage** - Stores which words the student has marked as "known"
  - Key: `'knownWords'`
  - Value: JSON array of word strings
  - Persists between sessions
  - Unique per browser/device

## File Structure

```
/Users/sbenodiz/Development /falshcard/
├── index.html                    # Landing page
├── student-version.html          # Interactive practice (3 modes)
├── teacher-version.html          # Reference guide with all definitions
├── vocab_data.json              # Master vocabulary data (1,193 words)
├── vocab_array.js               # JavaScript format for updates
├── 11plus_vocabulary_flashcards.docx  # Original source (276 words)
├── README.md                    # User documentation
├── CLAUDE.md                    # This file (developer documentation)
└── .gitignore
```

## Features

### Student Version (3 Modes)

1. **Flashcard Mode**
   - Click to flip cards and see meanings
   - Navigate with arrows or keyboard
   - Mark words as "known" (saved in localStorage)

2. **Quiz Mode**
   - Multiple choice questions
   - Instant feedback
   - Score tracking

3. **Teacher Mode**
   - Shows word only (no meanings)
   - Student must ask teacher for definition
   - Navigation only (no flipping)

### Teacher Version

- Complete searchable table
- All 1,193 words with meanings
- Printable reference guide
- Statistics dashboard

## Updating Vocabulary

To add/update vocabulary words:

1. Edit `vocab_data.json` directly, OR
2. Process a new source document (Word/text file)
3. Run the Python script to regenerate `vocab_array.js`:

```python
# Example script structure (see git history for full script)
import json
with open('vocab_data.json', 'r') as f:
    data = json.load(f)
# Generate JavaScript array format
```

4. Update HTML files with new data:

```python
# Replace vocabData array in HTML files
# Update all "276" references to new count
```

5. Commit and push to GitHub (Railway auto-deploys)

## Technology Stack

- **Frontend:** Pure HTML, CSS, JavaScript (no frameworks)
- **Styling:** Custom CSS with gradient themes
- **Storage:** Browser localStorage for user progress
- **Hosting:** Railway (connected to GitHub for auto-deploy)
- **Version Control:** Git/GitHub

## Deployment

- **GitHub:** https://github.com/sbenodiz/vocabulary
- **Railway:** Auto-deploys from main branch
- **Process:** Push to GitHub → Railway detects changes → Auto-deploys

## Data History

- **Original:** 276 words from `11plus_vocabulary_flashcards.docx`
- **Updated:** 1,193 words from `11plus_vocabulary_with_meanings (1).docx`
- **Format:** Word document → Text extraction → JSON → JavaScript → HTML

## Key Features

- ✅ 1,193 vocabulary words
- ✅ Child-friendly definitions (age 11)
- ✅ Persistent progress tracking (localStorage)
- ✅ Three learning modes
- ✅ Responsive design (mobile-friendly)
- ✅ Offline capable
- ✅ Printable teacher reference
- ✅ Keyboard navigation
- ✅ Search functionality (teacher version)

## Notes

- All vocabulary is embedded in HTML files for performance
- User progress is stored locally (not synced across devices)
- No backend/database needed
- No user authentication required
- Privacy-friendly (no data sent to server)

---

Generated with Claude Code
