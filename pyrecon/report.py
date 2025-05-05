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
        whois_info = entry['whois']
        html += f"""<div class='mb-8'>
<h2 class='text-xl font-semibold'>{entry['host']} ({entry['ip']})</h2>
<p><a href='{entry['url']}' class='text-blue-600 underline' target='_blank'>{entry['url']}</a></p>
<img src='{entry['screenshot']}' class='mt-4 border rounded'>
<h3 class='text-lg font-medium mt-4'>Informazioni WHOIS</h3>
<ul class='list-disc pl-5'>
"""
        if 'error' in whois_info:
            html += f"<li>Errore: {whois_info['error']}</li>"
        else:
            for key, value in whois_info.items():
                if key != 'whois_raw' and value:  # Esclude 'whois_raw' per evitare troppi dettagli
                    html += f"<li>{key}: {value}</li>"
        html += "</ul></div>"
    html += """</div>
</body>
</html>"""
    with open(output_file, 'w') as f:
        f.write(html)
