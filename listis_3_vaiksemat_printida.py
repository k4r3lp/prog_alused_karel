args = [9,8,7,1,2,3,4,5,6,7,8]
kalevipoeg = "Soomlased virutasid meilt eepose"

print(len(kalevipoeg))

def threesmallest(args):
    sordi_aretus = sorted(args)
    return sordi_aretus[:3]
print(threesmallest(args))
print(len(args))
print(min(args))
print(max(args))