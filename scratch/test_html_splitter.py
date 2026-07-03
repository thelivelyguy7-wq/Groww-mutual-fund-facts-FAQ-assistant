from langchain_text_splitters import HTMLHeaderTextSplitter

html_string = """
<!DOCTYPE html>
<html>
<body>
    <h1>HDFC Small Cap Fund</h1>
    <p>This is a small cap fund.</p>
    <h2>Exit Load</h2>
    <p>1% if redeemed within 1 year.</p>
    <h2>Expense Ratio</h2>
    <p>Direct Plan: 0.8%</p>
</body>
</html>
"""

headers_to_split_on = [
    ("h1", "Header 1"),
    ("h2", "Header 2"),
]

html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
html_header_splits = html_splitter.split_text(html_string)

for split in html_header_splits:
    print(split.metadata)
    print(split.page_content)
    print("---")
