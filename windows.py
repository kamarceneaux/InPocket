def set_dpi_awareness():
    """Configures the window box, to make the screen look more HD
    """
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass