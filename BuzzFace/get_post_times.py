import glob
import json
from collections import defaultdict
import os

###############################################################################
# This script will create a dict with keys being thread IDs and values
# being the time the post was made on Facebook, for use with the API.
###############################################################################

def main():
    """Get the post times and write them to disk in a dict."""
    post_times_dict = defaultdict(str)
    # Use `os.path.join` for platform-independent file paths
    files = glob.glob(os.path.join(".", "dataset", "*", "*", "posts.json"))
    for filename in files:
        try:
            with open(filename, 'r') as f:  # Open the post JSON
                postJSON = json.load(f)
            post_time = ""
            if postJSON:
                post_time = postJSON.get('created_time', "")
            # Split up the filepath by os.sep to get the thread ID
            threadID = os.path.basename(os.path.dirname(filename))
            post_times_dict[threadID] = post_time
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error processing file {filename}: {e}")

    # Write the output to POST_TIMES.json
    try:
        with open("POST_TIMES.json", "w") as f2:
            json.dump(post_times_dict, f2, indent=4, sort_keys=True)
        print("POST_TIMES.json has been created successfully.")
    except Exception as e:
        print(f"Error writing POST_TIMES.json: {e}")


if __name__ == '__main__':
    main()
