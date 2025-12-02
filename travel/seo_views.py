from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def robots_txt(request):
    """
    Generate robots.txt file dynamically
    Allows all search engines to crawl the site and points to sitemap
    """
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        "# Sitemaps",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


@require_GET
def google_verification(request):
    """
    Placeholder for Google Search Console HTML verification
    Replace the content below with your actual Google verification code
    """
    # TODO: Replace with actual Google Search Console verification meta tag
    html = """<!DOCTYPE html>
<html>
<head>
    <meta name="google-site-verification" content="YOUR_VERIFICATION_CODE_HERE" />
    <title>Google Site Verification</title>
</head>
<body>
    <h1>Google Site Verification</h1>
    <p>This page is for Google Search Console verification.</p>
</body>
</html>"""
    return HttpResponse(html, content_type="text/html")
