# Track Changes Guide for main_englishv09.tex

## Overview
The `main_englishv09.tex` file is configured with the `changes` package to track all modifications for the revision process.

## Quick Start Commands

Use these commands in your LaTeX document to mark changes:

### 1. Add new text (highlighted in yellow)
```latex
\addtext{This is new text about anti-aliasing filters.}
```

### 2. Delete text (shown as strikethrough)
```latex
\deltext{This old explanation is removed.}
```

### 3. Replace text
```latex
\replacetext{new correct text}{old incorrect text}
```

### 4. Highlight existing text (for emphasis)
```latex
\highlighttext{This important section has been modified.}
```

### 5. Add reviewer comments
```latex
\notetext{This addresses Reviewer 2's concern about reproducibility.}
```

## Compilation Modes

### Draft Mode (Show Changes)
In the preamble, use:
```latex
\usepackage[draft]{changes}
```
This shows all changes with yellow highlighting, strikethroughs, etc.

### Final Mode (Hide Changes)
In the preamble, use:
```latex
\usepackage[final]{changes}
```
This produces a clean document with all changes incorporated (no markup).

## Workflow for Submission

1. **Working Phase**: Keep `[draft]` mode while making changes
   - Compile regularly to see what's highlighted
   - PDF will show all tracked changes in yellow

2. **Review Phase**: Send draft PDF to co-authors
   - They can see exactly what changed

3. **Submission Phase**: 
   - Change to `[draft]` mode and compile → `main_englishv09_TRACKED.pdf` (for "Related manuscript file")
   - Change to `[final]` mode and compile → `main_englishv09.pdf` (clean, for "Article file")
   - Submit both:
     - `main_englishv09.tex` (source, will use [final] mode)
     - `main_englishv09_TRACKED.pdf` (marked as "related manuscript file")

## Example Usage

### Original v08 text:
```latex
The dataset includes signals at multiple resolutions.
```

### Modified v09 text with tracking:
```latex
The dataset includes \addtext{2500 }signals at multiple resolutions\addtext{, 
with anti-aliasing filtered subsampling to prevent frequency aliasing as 
recommended by the reviewers}.
```

### Result in draft mode:
The dataset includes **2500** signals at multiple resolutions**, with anti-aliasing filtered subsampling to prevent frequency aliasing as recommended by the reviewers**.
(shown with yellow highlighting)

### Result in final mode:
The dataset includes 2500 signals at multiple resolutions, with anti-aliasing filtered subsampling to prevent frequency aliasing as recommended by the reviewers.
(clean text, no markup)

## Tips

- Use `\addtext{}` for most new additions
- Use `\replacetext{new}{old}` when correcting errors
- Use `\notetext{}` to document which reviewer comment you're addressing
- Don't nest commands (e.g., don't put `\addtext{}` inside `\replacetext{}`)

## Addressing Reviewer Comments

When making changes, add notes like:
```latex
\addtext{The anti-aliasing filter uses a Butterworth design with order 8, 
cutting at 90\% of the target Nyquist frequency.} 
\notetext{Addresses Reviewer's concern about filter documentation.}
```

## Current Status

- ✅ Package installed and configured
- ✅ Commands defined: `\addtext`, `\deltext`, `\replacetext`, `\notetext`, `\highlighttext`
- ✅ Currently in `[draft]` mode (shows all changes)
- 📝 Ready for you to start marking changes

## Next Steps

1. Identify sections that need revision based on ReviewAnalysis.md
2. Make changes using the tracking commands
3. Compile periodically to verify highlighting works
4. Before submission, generate both draft and final PDFs
