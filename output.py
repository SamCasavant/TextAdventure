def visOutput(player, eventLocations, output):
    for location in eventLocations:
        if location in player.location.visibleLocations:
            print(output)
            return
def audOutput(player, actor, output):
    if actor.location in player.location.audibleLocations:
        print(output)

def listToNatural(pyList):
    output = ""
    if len(pyList) == 1:
        return pyList[0]
    tempList = []
    for item in pyList: #Count duplicates
        try:
            index = [each[0] for each in tempList].index(item)
            tempList[index][1] += 1
        except ValueError:
            tempList.append([item, 1])
    if len(tempList) == 1:
        return f"{item[1]} {item[0]}s."

    for item in tempList:
        if item == tempList[-1]:#When we reach the end of the list
            if item == tempList[1]:#If the list only had two items
                output = output[:-2]+" "#drop the oxford comma
            output += "and "
        if item[1] == 1:
            output += f"{item[0]}, "
        else:
            output += f"{item[1]} {item[0]}s, "
    return output[:-2] #delete trailing comma and space