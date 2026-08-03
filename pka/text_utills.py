import re 

def extract_hashtags(text:str) -> list[str]:
    """
        Find all hashtags in a note's text and return just the tag names
        (without the '#' symbol).

        Example:
        extract_hashtags("Loving the #python journey, feeling #motivated")
        -> ['python', 'motivated']
    """
    pattern = r"#(\w+)"
    return re.findall(pattern, text)      

def extract_mentions(text: str) -> list[str]:
    """
    Find all @mentions in a note's text and return just the names
    (without the '@' symbol).

    Example:
        extract_mentions("Meeting with @sarah and @raj tomorrow")
        -> ['sarah', 'raj']
    """
    pattern = r"@(\w+)"
    return re.findall(pattern, text)

def clean_whitespace(text: str) -> str:
    """
    Collapse any run of whitespace (multiple spaces, tabs, newlines)
    into a single space, and strip leading/trailing whitespace.

    Example:
        clean_whitespace("Hello   world\n\n  from   Python")
        -> "Hello world from Python"
    """
    pattern = r"\s+"
    cleaned = re.sub(pattern, " ", text)
    return cleaned.strip()

def split_into_sentences(text: str) -> list[str]:
    """
    Split text into a list of sentences, using '.', '!', or '?'
    followed by whitespace as the boundary.

    Example:
        split_into_sentences("Sarah owns backend. Raj owns API. Done by Friday!")
        -> ['Sarah owns backend.', 'Raj owns API.', 'Done by Friday!']
    """
    pattern = r"(?<=[.!?])\s+"
    sentences = re.split(pattern, text.strip())
    return [s for s in sentences if s]

def chunk_text2(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split text into overlapping chunks of a fixed character size.

    Args:
        text: The text to split (should already be cleaned).
        chunk_size: Max number of characters per chunk.
        overlap: Number of characters repeated between consecutive
            chunks, so context isn't lost at chunk boundaries.

    Returns:
        A list of text chunks.

    Raises:
        ValueError: If overlap is >= chunk_size (would cause an
            infinite loop / non-progressing window).
    """
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        # Slice out the window: from 'start' up to 'start + chunk_size'.
        # Python slicing auto-clamps if end goes past the string length,
        # so the last chunk just comes out shorter — no IndexError risk.
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        # Move the window forward, but NOT by the full chunk_size —
        # by (chunk_size - overlap) instead, so the next chunk starts
        # a bit before this one ended. That's what creates the overlap.
        start += chunk_size - overlap

    return chunks

def chunk_text(text: str, max_chunk_size: int = 200, overlap: int = 1) -> list[str]:
    """
    Split text into overlapping chunks of whole sentences, each chunk
    staying under max_chunk_size characters where possible.

    Args:
        text: the full note text to chunk
        max_chunk_size: soft limit on characters per chunk
        overlap: number of sentences to repeat at the start of the next chunk

    Example:
        chunk_text("Sarah owns backend. Raj owns API. Done by Friday!", max_chunk_size=30)
        -> ['Sarah owns backend.', 'Raj owns API.', 'Raj owns API. Done by Friday!']
    """
    sentences = split_into_sentences(text)
    chunks = []
    current_chunk: list[str] = []
    current_length = 0

    for sentence in sentences:
        # Would adding this sentence blow past our size limit?
        if current_length + len(sentence) > max_chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            # Start the next chunk with the last `overlap` sentences from this one
            current_chunk = current_chunk[-overlap:] if overlap > 0 else []
            current_length = sum(len(s) for s in current_chunk)

        current_chunk.append(sentence)
        current_length += len(sentence)

    # Don't forget the last chunk — it won't get appended by the loop above
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

#result=extract_hashtags("Please extract #python hastags from the #texts")
#print(result) 


#text = clean_whitespace("The golden sun slowly descends toward the horizon, painting the evening sky in vibrant shades of red, pink, and deep purple. Gentle waves crash against the sandy shoreline, creating a rhythmic and calm melody that echoes across the quiet beach. A cool, refreshing breeze sweeps in from the vast ocean, carrying the salty scent of the sea. Seagulls glide gracefully above the water, their silhouettes all dark against the fading light. Night approaches, and brings a peaceful end to a long, quiet day.")  # simulate a long note
#chunks = chunk_text2(text, chunk_size=100, overlap=20)

#for i, c in enumerate(chunks):
#    print(f"--- Chunk {i} (len={len(c)}) ---")
#    print(c)

#text = "Sarah owns backend. Raj owns API integration. We ship by Friday. QA starts Monday. Retro is next Wednesday."
#result = chunk_text(text, max_chunk_size=40, overlap=1)
#for i, c in enumerate(result):
#    print(f"Chunk {i}: {c!r}")