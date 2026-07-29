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


#result=extract_hashtags("Please extract #python hastags from the #texts")
#print(result) 