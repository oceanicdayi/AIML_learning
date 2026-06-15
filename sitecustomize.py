"""Runtime compatibility shims for Hugging Face Spaces.

Python imports sitecustomize automatically during startup if this file is on
sys.path. We use it to restore the deprecated huggingface_hub.HfFolder symbol
that some Gradio builds still import.
"""

import huggingface_hub as _hf_hub

if not hasattr(_hf_hub, "HfFolder"):
    class HfFolder:
        @staticmethod
        def get_token():
            getter = getattr(_hf_hub, "get_token", None)
            return getter() if getter else None

        @staticmethod
        def save_token(token):
            login = getattr(_hf_hub, "login", None)
            if login is None:
                return None
            try:
                return login(token=token, add_to_git_credential=False)
            except TypeError:
                return login(token=token)

        @staticmethod
        def delete_token():
            logout = getattr(_hf_hub, "logout", None)
            return logout() if logout else None

    _hf_hub.HfFolder = HfFolder
