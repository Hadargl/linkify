matches = ['youtube.com']


closest_match = matches[0]

print("closest match: " + closest_match)

domain_len = len(closest_match)

def build_url_path(link, match, domain_len):
    if "reddit" in match:
        first_slash_loc = link.index("/")
        slash_loc = first_slash_loc + 3
        return link[slash_loc:].strip()
    # elif link[0]=='/':
    #     slash_loc = first_slash_loc
    elif '/' in link:
        first_slash_loc = link.index("/")
        slash_loc = first_slash_loc
        return link[slash_loc:].strip()
    else:
        linklist = [ x for x in link]
        del linklist[:(domain_len)]
        # linklist[int(domain_len) - 1].strip()
        print('first strip')
        print(linklist)
        linklist[0] = '/'
        print("else print: ")
        print(linklist)
        print(type(linklist))
        link = ''.join(linklist)
        print(link)
        return link




# def build_url_path(link, match):
#     first_slash_loc = link.index("/")
#     if "reddit" in match:
#         slash_loc = first_slash_loc + 3
#     else:
#         slash_loc = first_slash_loc
#     return link[slash_loc:].strip()





new_path = build_url_path('youtube.comyhdhhdhhdhdhhdhhdhhd', closest_match, domain_len)

print(new_path)

new_url = str(matches[0]) + str(new_path)

print("new url: " + new_url + " length: " + str(len(new_url)))
