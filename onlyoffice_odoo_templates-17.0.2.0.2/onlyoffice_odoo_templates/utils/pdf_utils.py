# TODO: add convert docx to pdf

def is_pdf_form(text):
    if not text:
        return False
    
    index_first = text.find(b'%\xCD\xCA\xD2\xA9\x0D')
    if index_first == -1:
        return False
    
    p_first = text[index_first + 6:]

    if not p_first.startswith(b'1 0 obj\x0A<<\x0A'):
        return False
    
    p_first = p_first[11:]

    signature = b'ONLYOFFICEFORM'
    index_stream = p_first.find(b'stream\x0D\x0A')
    index_meta = p_first.find(signature)

    if index_stream == -1 or index_meta == -1 or index_stream < index_meta:
        return False
    
    p_meta = p_first[index_meta:]
    p_meta = p_meta[len(signature) + 3:]

    index_meta_last = p_meta.find(b' ')
    if index_meta_last == -1:
        return False
    
    p_meta = p_meta[index_meta_last + 1:]

    index_meta_last = p_meta.find(b' ')
    if index_meta_last == -1:
        return False
    
    return True