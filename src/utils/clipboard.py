import win32clipboard
import logging
import base64
import re

def set_clipboard_html(html_content):
    if not html_content or not isinstance(html_content, str):
        raise ValueError("HTML content must be non-empty string")
    try:
        CF_HTML = win32clipboard.RegisterClipboardFormat("HTML Format")
        html_header = (
            "Version:0.9\r\n"
            "StartHTML:0000000105\r\n"
            "EndHTML:{:010d}\r\n"
            "StartFragment:0000000141\r\n"
            "EndFragment:{:010d}\r\n"
            "<html><body>\r\n"
            "<!--StartFragment-->{}<!--EndFragment-->\r\n"
            "</body></html>"
        )
        fragment = html_content
        full_html = html_header.format(
            len(html_header) + len(fragment),
            len(html_header) + len(fragment) - len("<!--EndFragment-->\r\n</body></html>"),
            fragment
        )
        win32clipboard.OpenClipboard()
        try:
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(CF_HTML, full_html.encode('utf-8'))
            logging.info("Set HTML to clipboard")
        finally:
            win32clipboard.CloseClipboard()
    except Exception as e:
        logging.error(f"Failed to set clipboard HTML: {e}")
        raise

def get_clipboard_text():
    try:
        win32clipboard.OpenClipboard()
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
            text = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
            logging.info("Retrieved clipboard text")
            return text
        return None
    except Exception as e:
        logging.error(f"Failed to get clipboard text: {e}")
        return None
    finally:
        win32clipboard.CloseClipboard()

def validate_base64(data):
    try:
        if not re.match(r'^[A-Za-z0-9+/=]+$', data):
            return False
        base64.b64decode(data, validate=True)
        return True
    except Exception as e:
        logging.error(f"Base64 validation failed: {e}")
        return False