import json
import time


def get_ambulance_total(mission):
    requirements = mission.get("requirements", {})
    additional = mission.get("additional", {})
    ambulance = requirements.get("ambulances", requirements.get("ambulance", 0))
    possible_patient = additional.get("possible_patient", 0)
    if not isinstance(ambulance, int):
        ambulance = 0
    if not isinstance(possible_patient, int):
        possible_patient = 0
    return ambulance + possible_patient

print("start")

file = open('api.json')
data = json.load(file)

# get al the expansion possibilities
for i in data:
    print(f"collecting expansions for mission {i['id']}")
    expansions = []
    expansions.append(i['base_mission_id'])
    if("expansion_missions_ids" in i["additional"]):
        for e in i["additional"]["expansion_missions_ids"]:
            if not(e in expansions):
                expansions.append(e)
           
    i["exp"] = expansions
    missions = [d for d in data if d["base_mission_id"] in expansions]

    for k in missions:
        if("expansion_missions_ids" in k["additional"]):
            for ex in k["additional"]["expansion_missions_ids"]:
                if not(ex in expansions):
                    expansions.append(ex)
                    added = [j for j in data if j["base_mission_id"] in [ex]]
                    for x in added:
                        missions.append(x)
    i["exp"] = expansions

time.sleep(3)
# compare missions and update to biggest version.        
for i in data:
    print(f"Processing mission {i['id']}")
    if(len(i["exp"]) > 0):
        possiblemissions = [d for d in data if d["base_mission_id"] in i["exp"]]
        for k in possiblemissions:
            for j in k["requirements"]:
                if(isinstance(k["requirements"][j], int)):
                    if(j == "ambulances" or j == "ambulance"):
                        source_total = get_ambulance_total(k)
                        target_total = get_ambulance_total(i)
                        if(source_total > target_total):
                            i["requirements"][j] = source_total
                        continue
                    if(j in i["requirements"]):
                        if(k["requirements"][j] > i["requirements"][j]):
                            i["requirements"][j] = k["requirements"][j]
                    else:
                        i["requirements"][j] = k["requirements"][j]
                elif (j == "personnel_educations"):
                    for m in k["requirements"]["personnel_educations"]:
                        if not("personnel_educations" in i["requirements"]):
                            i["requirements"]["personnel_educations"] = {}
                        if(isinstance(k["requirements"]["personnel_educations"][m], int)):
                            if(m in i["requirements"]["personnel_educations"]):
                                if(k["requirements"]["personnel_educations"][m] > i["requirements"]["personnel_educations"][m]):
                                    i["requirements"]["personnel_educations"][m] = k["requirements"]["personnel_educations"][m]
                            else:
                                i["requirements"]["personnel_educations"][m] = k["requirements"]["personnel_educations"][m]
            for l in k["additional"]:
                if(isinstance(k["additional"][l], int)):
                    if(l in i["additional"]):
                        if(k["additional"][l] > i["additional"][l]):
                            i["additional"][l] = k["additional"][l]
                    else:
                        i["additional"][l] = k["additional"][l]
                elif (l == "personnel_educations"):
                    for m in k["additional"]["personnel_educations"]:
                        if not("personnel_educations" in i["additional"]):
                            i["additional"]["personnel_educations"] = {}
                        if(isinstance(k["additional"]["personnel_educations"][m], int)):
                            if(m in i["additional"]["personnel_educations"]):
                                if(k["additional"]["personnel_educations"][m] > i["additional"]["personnel_educations"][m]):
                                    i["additional"]["personnel_educations"][m] = k["additional"]["personnel_educations"][m]
                            else:
                                i["additional"]["personnel_educations"][m] = k["additional"]["personnel_educations"][m]
                    




with open('max.json', 'w') as outfile:
    json.dump(data, outfile)


file.close()

print("finished")

