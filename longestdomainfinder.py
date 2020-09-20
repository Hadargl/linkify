import csv

with open("top500Domains.csv", "r") as f:
    reader = csv.DictReader(f)

    domains = [row["Root Domain"] for row in reader]

longest_domain = ''

for d in domains:
    if len(d) > len(longest_domain):
        longest_domain = d
    else:
        longest_domain = longest_domain

print(len(longest_domain))
