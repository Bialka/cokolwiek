
l = ["Zimmer", "Newman", "Kilar", "Newman", "", "", "Sherlock", "Sherlock"]
# l = ['', ""]

cos = {}
selected = [0, "whoever"]
for x in l:
    if x == "":
        continue
    if x not in cos:
        cos[x] = 0
    cos[x] += 1
    if selected[0] < cos[x]:
        selected = [cos[x], x]
    elif selected[0] == cos[x]:
        selected += [x]
print(selected)
print(selected[1:] if selected[0] else None)