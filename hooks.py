"""MkDocs hooks: generate sitemap.xml after build."""

import os
from datetime import datetime, timezone
def on_post_build(config, **kwargs):
    """Generate sitemap.xml in the site directory after build."""
    site_dir = config["site_dir"]
    site_url = config["site_url"].rstrip("/")
    sitemap_path = os.path.join(site_dir, "sitemap.xml")

    urls = []
    for root, _dirs, files in os.walk(site_dir):
        for name in files:
            if name == "index.html":
                path = os.path.relpath(root, site_dir)
                if path == ".":
                    loc = f"{site_url}/"
                else:
                    loc = f"{site_url}/{path}/"
                urls.append(loc)
            elif name.endswith(".html") and name != "404.html":
                path = os.path.relpath(os.path.join(root, name), site_dir)
                path = path.replace("\\", "/")
                loc = f"{site_url}/{path}"
                urls.append(loc)

    lastmod = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc in sorted(urls):
        escaped = loc  # URLs in sitemap should be escaped per spec
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{escaped}</loc>")
        xml_lines.append(f"    <lastmod>{lastmod}</lastmod>")
        xml_lines.append("  </url>")
    xml_lines.append("</urlset>")

    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(xml_lines))
