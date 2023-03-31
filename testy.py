text = '''
Section 1:
Sarah and Jack were two teenagers who lived in the same neighborhood. Jack was tall with black hair and blue eyes, while Sarah was short with curly brown hair and green eyes. They had known each other their whole lives, but something changed between them one summer when they were both sixteen. 

Section 2:
It was a hot day, and they had spent the whole afternoon swimming in the lake together. As they dried off in the sun, Sarah and Jack began to talk about their hopes and dreams for the future. Before they knew it, the sun was beginning to set, and they had to say goodbye for the night. 

Section 3:
Over the next few weeks, Sarah and Jack couldn't stop thinking about each other. They started texting and calling each other every day, and soon they were spending all of their free time together. They went on long walks, watched movies, and even tried cooking together (with mixed results). As they got to know each other better, they realized they had fallen in love. 

Section 4:
Now, years later, Sarah and Jack are still together. They've gone through ups and downs like any couple, but they always come back to the love they share. They've supported each other through graduations, job changes, and even the loss of loved ones. They know that as long as they have each other, they can get through anything.
'''

def parse(shard):
    return shard[4:]

shards = text.split("Section")
del shards[0]
print(len(shards))

for shard in shards:
    s = parse(shard)
    print(s)

