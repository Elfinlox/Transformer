import random, sys

papers = open("./../data/paperlinks.txt", "rt", encoding = "utf8")
lines = papers.read().split("\n")

m = int(len(lines) / 2)
print("Number of papers:", m)

if sys.argv[1] == 'all':
	n = m
else:
	n = int(sys.argv[1])

selected_indices = random.sample(list(range(m)), n)

selected_papers = open("./../data/selected_papers.txt", "wt", encoding = "utf8")

for i in selected_indices:
    selected_papers.write(lines[2*i] + "\n")
    selected_papers.write(lines[2*i+1] + "\n")

papers.close()
selected_papers.close()