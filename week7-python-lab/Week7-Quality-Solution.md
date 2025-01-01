# **Week 7 Lab: Code Review – Refactoring – Pair Programming (Python Version) Solution**

## **Activity 1: Code Review**

---

1. **Almost no (or confusing) comments**  
   - You have a brief docstring, but it doesn’t clearly explain how the word count is calculated (e.g., by letters vs. whitespace). It simply says it’s “intentionally verbose,” which doesn’t clarify the core logic.

2. **Unclear how title length is determined**  
   - The docstring mentions scanning letters vs. whitespace, but it’s not explicitly stated whether you’re measuring *words* or *characters*. A reader might wonder why `.isalpha()` is used in some places but not in others.

3. **Method is large and not subdivided**  
   - You have two substantial loops in a single method. Each loop duplicates complex logic for scanning titles, instead of breaking it out into a helper function (e.g., `count_words_in_title`).

4. **Serious code duplication**  
   - You repeat very similar logic to count words in the first pass (finding the longest) and in the second pass (counting how many match). This is the same duplication issue noted in the Java snippet.

5. **Reusing variables**  
   - Variables like `count` are repurposed in multiple loops. `charcount` is assigned for debugging but then overwritten (and only printed). It’s not used in the final calculation.

6. **Unused or leftover variables**  
   - `selectedBooks` is declared but never used—clearly a leftover.  
   - `charcount` is assigned and printed but never actually contributes to the logic.

7. **Unclear variable names**  
   - Names like `count1`, `found`, and `eol` make the logic harder to read.  
   - “`found`” only indicates you’re currently in the middle of a “word,” but it’s not immediately apparent without closely reading the loop.

8. **Confusing logic for word count**  
   - The manual scanning of `.isalpha()` vs. “not alpha” is more complicated than using a straightforward approach like `len(title.split())`.  
   - The mismatch between the first pass (just scanning) and the second pass (nearly identical scanning) can confuse maintainers, especially if punctuation or trailing spaces appear in real titles.

---

## **Activity 2: Code Refactor**
---

## **Refactored `count_longest_book_titles`**

Below is a **refactored Python solution** using a **helper method** for word counting—mirroring the Java snippet’s character-by-character approach—but **without** duplicating the entire logic twice. It includes explanations on how each **smell** was removed. 

Additionally, we’ll address the **TypeError** (`Takes 1 positional argument but 2 were given`) by making `_count_words_in_title` a proper *instance method* (i.e., it includes `self` as the first parameter). 

---

## **Refactored Code with a Helper Method**

```python
    def _count_words_in_title(self, title: str) -> int:
        """
        Counts words by scanning letters vs. non-letters,
        similar to the Java snippet logic.
        - We consider a 'word' any run of characters for which .isalpha() is True.
        - When we hit a non-alpha or the end of the string, we finalize one 'word'.

        This method is intentionally verbose if you need 
        to mimic the original Java approach exactly. If you want simpler code, 
        you could just do: return len(title.split()) 
        """
        count = 0
        found = False
        eol = len(title) - 1

        for i, ch in enumerate(title):
            if ch.isalpha() and i != eol:
                found = True
            elif not ch.isalpha() and found:
                count += 1
                found = False
            elif ch.isalpha() and i == eol:
                count += 1

        return count

    def count_longest_book_titles(self) -> int:
        """
        Determine how many books share the maximum word count in their titles,
        using a single-pass approach with the _count_words_in_title helper.

        Refactoring:
        - Removed duplicated loops
        - Removed leftover variables/debug prints
        - Clarified naming
        - Extracted word-count logic into a helper method
        """
        all_books = self.db.query(Book).all()
        if not all_books:
            return 0

        # 1) Build an array of word counts for each book
        word_counts = [self._count_words_in_title(book.title) for book in all_books]

        # 2) Determine the maximum word count
        max_word_count = max(word_counts)

        # 3) Count how many match that max
        return sum(1 for wc in word_counts if wc == max_word_count)
```

---

## **Summary of the Refactoring**

- **Smelly** aspects (duplication, leftover variables, unclear docstrings) are **removed**.  
- We **maintain** the original logic for word detection (character scanning), so tests expecting that approach still pass.  
- The final method is concise, maintainable, and clear on how we’re counting “words.”  

---
## **Activity 3: Pair Programming**

```python
    def get_most_common_words_in_titles(self, top_k: int) -> Dict[str, int]:
        """
        Example:
          - If there are two books: 
               "I'm a Book", "This book is great"
          - Then get_most_common_words_in_titles(2) might return:
               {"book": 2, "a": 1}
          - get_most_common_words_in_titles(3) might return:
               {"book": 2, "a": 1, "is": 1}

        :param top_k: how many words to return (0 => return empty dict).
        :return: a dictionary of at most top_k words -> count, 
                 sorted by frequency desc, then alphabetically asc.
        """

        # 1) If top_k <= 0, return an empty dict immediately
        if top_k <= 0:
            return {}

        # 2) Fetch all books
        all_books = self.db.query(Book).all()

        # 3) Build a frequency map of all words, ignoring case
        #    We'll use a Counter from the collections module
        word_counter = Counter()

        for book in all_books:
            # Split on whitespace, convert each word to lowercase
            # You may want to strip punctuation or do more advanced logic as needed
            words = book.title.lower().split()
            word_counter.update(words)

        if not word_counter:
            # If no words found at all
            return {}

        # 4) Sort the words by:
        #    (1) frequency (descending), 
        #    (2) alphabetical (ascending)
        # Counter.most_common() only sorts by frequency desc, so we need a custom sort
        sorted_items = sorted(
            word_counter.items(),
            key=lambda x: (-x[1], x[0])  # -x[1] = descending freq, x[0] = alpha asc
        )

        # 5) Take the top_k items from the sorted list
        top_items = sorted_items[:top_k]

        # 6) Convert to a dict, preserving sorted order (use OrderedDict if needed)
        returned_dict = OrderedDict(top_items)

        return dict(returned_dict)
```

---

