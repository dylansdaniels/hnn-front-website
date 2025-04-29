# %%
import os
import json
import requests
import datetime

# go up one level in the directory
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

with open('persons.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# get current date only in YYYY-MM-DD
date = datetime.datetime.now().strftime("%Y-%m-%d")

page_contents=f"""
            <div id="content-wrapper">
                <div id="content">
                    <!--
                    # Title: Developers
                    # Updated: {date}
                    -->
"""

# %%
# --------------------------------------------------
# Build active developers section

active_developers = {
    k:v for k,v in data.items() if v["status"] == "active"
}

active_html = ""

active_head = """
                    <br>
                    <h2 style="text-align: center;">
                        Active Development Team
                    </h2>

                    <div class="dev-grid">
"""

active_template="""
                        <a class="grid-link" href="{website_link}">
                            <div class="dev-card">
                                <img data-github="{username}" />
                                <div class="name">{name}</div>
                                <div class="position">{position}</div>
                            </div>
                        </a>
"""

active_tail="""
                    </div>
"""

active_html += active_head

for name, v in active_developers.items():

    username = v["github"]
    position = v["position"]
    website = v["website"]

    if website is None or website == "":
        website_link = f"https://github.com/{username}"
    else:
        website_link = website

    active_html += active_template.format(
        name=name,
        username=username,
        position=position,
        website_link=website_link
    )

active_html += active_tail

# print(active_html)

# %%
# --------------------------------------------------
# Build all developers section

inactive_developers = {
    k:v for k,v in data.items() if v["status"] == "inactive"
}

inactive_html = ""

inactive_head = """
                    <br>
                    <h2 style="text-align: center;">
                        All Developers
                    </h2>

                    <div class="dev-grid inactive">
"""

inactive_template="""
                        <a class="grid-link" href="{website_link}">
                            <div class="dev-card">
                                <img data-github="{username}" />
                                <div class="name">{name}</div>
                            </div>
                        </a>
"""

inactive_tail="""
                    </div>
"""

inactive_html += inactive_head

for name, v in inactive_developers.items():

    username = v["github"]
    website = v["website"]

    if website is None or website == "":
        website_link = f"https://github.com/{username}"
    else:
        website_link = website

    inactive_html += inactive_template.format(
        name=name,
        username=username,
        website_link=website_link
    )

inactive_html += inactive_tail

# print(inactive_html)

# %% 
# --------------------------------------------------
# Build additional contributors section

# get main developer gh usernames from json
developer_usernames = {
    info["github"] for info in data.values()
    if (info["github"] and (info["status"] != "contributor"))
}

# get contributor gh usernames from json
contributor_usernames = {
    info['github'] for info in data.values()
    if (info["github"] and (info["status"] == "contributor"))
}

# repos to check
repo_urls = [
    "https://api.github.com/repos/jonescompneurolab/hnn-core/contributors",
    "https://api.github.com/repos/jonescompneurolab/hnn/contributors"
]

# get all contributors
all_contributors = set()

for url in repo_urls:
    response = requests.get(url)
    fetched_contributors = response.json()
    for user in fetched_contributors:
        all_contributors.add(user['login'])

all_contributors = all_contributors.union(contributor_usernames)

# get contributors not listed in active/inactive developers sections
other_contributors = sorted(
    user for user in all_contributors if user not in developer_usernames
)

# get names of contributors if listed
contributors_with_names = {}
for username in other_contributors:
    user_url = f"https://api.github.com/users/{username}"
    user_response = requests.get(user_url)
    user_data = user_response.json()

    full_name = user_data.get("name", username)
    if full_name is None:
        full_name = username

    contributors_with_names[username] = full_name

# generate html
contributor_html = ""

contributor_head = """
                    <br>
                    <h2 style="text-align: center;">
                        Additional Contributors
                    </h2>

                    <div class="dev-grid additional">
"""

contributor_template = """
                        <div class="dev-card">
                            <a href="https://github.com/{username}" alt="{name}">
                                <img data-github="{username}" alt="{name}" />
                            </a>
                        </div>
"""

contributor_tail = """
                    </div>
"""

contributor_html += contributor_head

for username, name in contributors_with_names.items():
    contributor_html += contributor_template.format(username=username, name=name)

contributor_html += contributor_tail

# print(contributor_html)

# %%
# --------------------------------------------------
# Aggregate all html

head_path = os.path.join(
    os.getcwd(),
    "templates",
    "head.html",
)
tail_path = os.path.join(
    os.getcwd(),
    "templates",
    "tail.html",
)

with open(head_path, "r") as f:
    head_html = f.read()

with open(tail_path, "r") as f:
    tail_html = f.read()

collaborators_html = """
                    <br>
                    <h2 style="text-align: center;">
                        Collaborators
                    </h2>
                    <div class="collaborators">
                        <ul>
                            <li>Matti Hamalainen (co-PI), MGH</li>
                            <li>Michael Hines (co-PI), Yale</li>
                            <li>Noam Peled, MGH</li>
                            <li>Ted Carnevale, Yale</li>
                            <li>Robert McDougal, Yale</li>
                            <li>Christopher Moore, Brown</li>
                            <li>Amitava Majumdar, SDSC</li>
                            <li>Kenneth Yoshimoto, SDSC</li>
                            <li>Subhashini Sivagnanam, SDSC</li>
                            <li>Salvador Dura-Bernal, SUNY Downstate</li>
                            <li>Matteo Cantarelli, Metacell</li>
                        </ul>
                    </div>
"""

page_contents_close = """
                    <br><br>
                </div> <!-- close content -->
            </div> <!-- close content wrapper -->
"""

html_out = head_html + page_contents + active_html + inactive_html + contributor_html + collaborators_html + page_contents_close + tail_html

# print(html_out)
# %%
with open("developers.html", "w") as f:
    f.write(html_out)