from bs4 import BeautifulSoup
import requests

# Feed URL
feed_url = "https://feeds.feedburner.com/Net-empregos"  # Replace with the actual FeedBurner or RSS URL

# Fetch the feed content from the URL
response = requests.get(feed_url)

# Check if the request was successful
if response.status_code == 200:
    feed_content = response.text  # Retrieve the feed content as text
    soup = BeautifulSoup(feed_content, "html.parser")  # Parse the feed content with BeautifulSoup

    # Split by potential delimiters to process entries
    entries = feed_content.split("https://www.net-empregos.com/")

    # Loop through entries to extract details
    for entry in entries[1:]:  # Skip the first as it is the header
        parts = entry.split()
        job_link = "https://www.net-empregos.com/" + parts[0]
        job_title = " ".join(parts[1:-3])  # Extract title (customize logic based on actual structure)
        post_date = parts[-3] + " " + parts[-2] if len(parts) > 2 else "Unknown"
        
        print("Job Title:", job_title)
        print("Job Link:", job_link)
        print("Post Date:", post_date)
        print("-" * 50)
else:
    print(f"Failed to fetch feed. HTTP Status Code: {response.status_code}")