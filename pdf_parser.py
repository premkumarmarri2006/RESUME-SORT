import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        text = "".join(p.extract_text() or "" for p in reader.pages)
        if text.strip():
            return text
    except ImportError:
        pass
    except Exception as e:
        print(f"pypdf error: {e}")
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(io.BytesIO(file_bytes))
        return "".join(p.extract_text() or "" for p in reader.pages)
    except Exception as e:
        print(f"PyPDF2 error: {e}")
    return ""
