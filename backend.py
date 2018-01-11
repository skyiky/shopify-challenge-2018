
import urllib, json
import sys
url = "https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=1&page=1"
response = urllib.urlopen(url)
data = json.loads(response.read())

per_page = data["pagination"]["per_page"]
total_items = data["pagination"]["total"] 
pages = total_items / per_page
curr_page = 1
curr_depth = 0
output = { "valid_menus": [], "invalid_menus": [] }

hist = []

def createOutput(root_id, child_ids, isInvalid, output):
	keyval = { "root_id": 0, "children":[0] }
	keyval["children"] = child_ids
	keyval["root_id"] = root_id
	if(isInvalid):
		output["invalid_menus"].append(keyval)
	else:
		output["valid_menus"].append(keyval)
	

def traverse_menu(passed_id, curr_page, per_page, data):
	#our page is lower
	had_to_change_page = False
	if (passed_id < (curr_page * per_page - per_page + 1)):
		had_to_change_page = True
		curr_page-=1
		while (passed_id < (curr_page * per_page - per_page)):
			curr_page-=1
	#our page is higher
	if (passed_id > (curr_page * per_page)):
		had_to_change_page = True
		curr_page+=1
		while (passed_id > (curr_page * per_page)):
			curr_page+=1
	#right page
	if had_to_change_page:
		url = "https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=" + str(1) + "&page=" + str(curr_page)
		response = urllib.urlopen(url)			
		data = json.loads(response.read())

	#
	for id in hist:
		if id == passed_id:
			#print("Found cycle with id " + str(passed_id))
			return True

	
	hist.append(passed_id)
	#print("Id " + str(passed_id) + " not found in history, adding")

	#traverse through the children
	for item in data["menus"]:
		if item["id"] == passed_id:
			#print("traversing children of id " + str(passed_id) + " with children: " + str(item["child_ids"]))
			for child_id in item["child_ids"]:
				return traverse_menu(child_id, curr_page, per_page, data)
	
#Looping through the root_ids
for item in data["menus"]:
	isCyclic = False
	if item["id"] not in hist:
		#print("adding id " + str(item["id"]) + " to hist")
		hist.append(item["id"])

		#traverse through the children
		for child_id in item["child_ids"]:
			#print("traversing child with id " + str(child_id) + ". current page: " + str(curr_page))

			if (traverse_menu(child_id, curr_page, per_page, data) == True):
				if not isCyclic:
					#print("ADDING id " + str(item["id"]) + " to INVALID menu")
					createOutput(item["id"], item["child_ids"], True, output);
					#print("root_id: " + str(item["id"]) +  " is cyclic")
					isCyclic = True
					break
			
		if not isCyclic:
			#print("ADDING id " + str(item["id"]) + " to VALID menu")
			createOutput(item["id"], item["child_ids"], False, output);
			#print("root_id: " + str(item["id"]) +  " is NOT cyclic")


#print("execution completed")
jsonOutput = json.dumps(output)
loaded_jsonOutput = json.loads(jsonOutput)

print loaded_jsonOutput
