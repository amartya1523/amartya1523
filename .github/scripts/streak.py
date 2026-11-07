import json, os, sys, urllib.request
from datetime import date, timedelta

user, token, out = sys.argv[1], os.environ["GITHUB_TOKEN"], sys.argv[2]
query = """query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}"""
req = urllib.request.Request(
    "https://api.github.com/graphql",
    json.dumps({"query": query, "variables": {"u": user}}).encode(),
    {"Authorization": f"bearer {token}"},
)
cal = json.load(urllib.request.urlopen(req))["data"]["user"]["contributionsCollection"]["contributionCalendar"]
days = {d["date"]: d["contributionCount"] for w in cal["weeks"] for d in w["contributionDays"]}

best = run = 0
for k in sorted(days):
    run = run + 1 if days[k] else 0
    best = max(best, run)

cur, d = 0, date.today()
if not days.get(d.isoformat()):
    d -= timedelta(days=1)
while days.get(d.isoformat()):
    cur += 1
    d -= timedelta(days=1)

stats = [(cal["totalContributions"], "contributions (last year)"), (cur, "current streak (days)"), (best, "longest streak (days)")]
cells = "".join(
    f'<text x="{100 + i * 200}" y="62" text-anchor="middle" font-size="34" font-weight="700" fill="#ffffff">{v}</text>'
    f'<text x="{100 + i * 200}" y="92" text-anchor="middle" font-size="13" fill="#c9d1d9">{label}</text>'
    for i, (v, label) in enumerate(stats)
)
svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="120" viewBox="0 0 600 120" font-family="Segoe UI,Helvetica,Arial,sans-serif">'
    '<rect width="600" height="120" rx="8" fill="#0d1117"/>'
    '<line x1="200" y1="25" x2="200" y2="95" stroke="#30363d"/><line x1="400" y1="25" x2="400" y2="95" stroke="#30363d"/>'
    f'{cells}</svg>'
)
open(out, "w").write(svg)
