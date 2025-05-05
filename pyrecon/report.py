import json

def generate_report(entries: list, output_file: str):
    html = """<!DOCTYPE html>
<html lang='en'>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<script src='https://cdn.tailwindcss.com'></script>
<title>PyRecon Report</title>
</head>
<body class='bg-gray-100 p-6'>
<div class='max-w-5xl mx-auto bg-white shadow rounded-lg p-6'>
<h1 class='text-3xl font-bold mb-6'>PyRecon Report</h1>
"""
    for entry in entries:
        html += f"""<div class='mb-8'>
<h2 class='text-xl font-semibold'>{entry['host']} ({entry['ip']})</h2>
<p><a href='{entry['url']}' class='text-blue-600 underline' target='_blank'>{entry['url']}</a></p>
<img src='{entry['screenshot']}' class='mt-4 border rounded'>
</div>
"""
    html += """</div>
</body>
</html>"""
    with open(output_file, 'w') as f:
        f.write(html)
