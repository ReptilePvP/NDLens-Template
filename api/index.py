from src.main import app

# This is the entry point for Vercel
def handler(request):
    return app(request)
