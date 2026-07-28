import re
from collections import Counter

def simple_summarizer(text, ratio=0.3):
    # Step 1: Clean and split text into sentences
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
    if not sentences:
        return "Error: No valid sentences found."
        
    # Step 2: Extract individual lowercase words
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return "Error: No words found."
        
    # Step 3: Filter out basic English filler words
    stop_words = {'the', 'is', 'and', 'a', 'in', 'to', 'of', 'it', 'that', 'this', 'for', 'with', 'on'}
    meaningful_words = [w for w in words if w not in stop_words]
    
    # Step 4: Count word frequencies and score sentences
    word_counts = Counter(meaningful_words)
    max_frequency = max(word_counts.values()) if word_counts else 1
    
    sentence_scores = {}
    for sentence in sentences:
        sentence_words = re.findall(r'\b\w+\b', sentence.lower())
        # Total the importance of each word in the sentence
        score = sum(word_counts.get(w, 0) / max_frequency for w in sentence_words)
        sentence_scores[sentence] = score

    # Step 5: Keep the top-scoring sentences based on the requested ratio
    num_to_keep = max(1, int(len(sentences) * ratio))
    # Sort sentences by their original appearance order, picking the ones with highest scores
    sorted_by_score = sorted(sentences, key=lambda s: sentence_scores.get(s, 0), reverse=True)
    best_sentences = sorted_by_score[:num_to_keep]
    
    # Re-sort back to original narrative order
    final_summary = [s for s in sentences if s in best_sentences]
    return " ".join(final_summary)

if __name__ == "__main__":
    print("\n" + "="*40)
    print("      NLP TEXT SUMMARIZER STARTING      ")
    print("="*40)
    
    # Forces a visible prompt in the terminal panel
    print("\n--> STEP 1: Please type or paste your article below.")
    print("--> NOTE: When finished, press ENTER once.\n")
    
    user_text = input("PASTE TEXT HERE: ").strip()
    
    if not user_text:
        print("\n[!] You did not enter any text. Program closing.")
    else:
        print("\n--> STEP 2: Choose summary size.")
        user_ratio = input("ENTER PERCENTAGE (e.g., 30 for 30%): ").strip()
        
        try:
            ratio_float = float(user_ratio) / 100.0
            if not (0.0 < ratio_float <= 1.0):
                raise ValueError
        except ValueError:
            print("[!] Invalid input. Using default size of 30%.")
            ratio_float = 0.3
            
        print("\n" + "-"*40)
        print("             GENERATING SUMMARY             ")
        print("-"*40)
        
        result = simple_summarizer(user_text, ratio_float)
        print(f"\n{result}\n")
        print("="*40)