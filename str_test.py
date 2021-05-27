txt = ["Blablabla", "", None,"ein Text"]

i = -1
for t in txt:
    i+=1
    if t:
        print(f"Text Nr {i} ist: {txt[i]}")
    else:
        print(f"Text Nr {i} ist: FALSE")
