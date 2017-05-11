import json
import numpy as np
import copy
from random import shuffle
import math
def getusers():
	users=[]
	with open('../yelp/yelp_academic_dataset_user.json') as f:
		for line in f:
			users.append(json.loads(line))

	print("got raw users")
	#filter users
	a=set()
	users2 = []
	for user in users:
		if (len(user['friends']) > 500):
			a.add(user['user_id'])
			users2.append(copy.deepcopy(user))

	for user in users2:
		user['friends'] = [x for x in user['friends'] if x in a]
	return users2

def create_knows(users2):
	#creating knows_obs file
	knows=set()
	for user in users2:
		for friend in user['friends']:
			knows.add((user['user_id'], friend, 1))
			knows.add((friend, user['user_id'], 1))
	for i in range(0, len(users2)):
		for j in range(i+1, len(users2)):
			if((users2[i]['user_id'], users2[j]['user_id'], 1) not in knows):
				knows.add((users2[i]['user_id'], users2[j]['user_id'], 0))
			if((users2[j]['user_id'], users2[i]['user_id'], 1) not in knows):
				knows.add((users2[j]['user_id'], users2[i]['user_id'], 0))
			
	print("knows created")
	#print data to file
	knows_obs = set()
	knows_tru = set()
	knows = list(knows)
	shuffle(knows)
	for i in range(0, len(knows)):
		#choice = np.random.choice([0,1,2], 1, p=[0.2, 0.7, 0.1])[0]
		if(i < len(knows)*.9):
			choice=0
		else:
			choice = 1
		elem = knows[i]
		if(choice == 0 and elem[2]==1):
			knows_obs.add(elem)
		else:
			knows_tru.add(elem)
	knows_tru = list(knows_tru)
	knows_tru = knows_tru[0:int(math.floor(.01*len(knows_tru)))]
	knows_tru = set(knows_tru)
	return knows_obs, knows_tru
	
def saveKnows(knows_obs, knows_tru):
	with open('knows_obs.txt', 'a') as f:
		for elem in knows_obs:
			f.write(elem[0] + "\t" + elem[1] + "\n")
	print("save")
	with open('knows_truth.txt', 'a') as f:
		for elem in knows_tru:
			f.write(elem[0] + "\t" + elem[1] + "\t" + str(elem[2]) + "\n")
	print("save")
	with open('knows_targets.txt', 'a') as f:
		for elem in knows_tru:
			f.write(elem[0] + "\t" + elem[1] + "\n")

print("started")
users = getusers()
print("obtained users")
knows_obs, knows_tru = create_knows(users)
print("obtained knows")
saveKnows(knows_obs, knows_tru)
print("saved knows")
"""
reviews=[]
userset = {}
for user in users2:
	user['lived'] = []
	userset[user['user_id']] = user

businesses = {}
with open('../yelp/yelp_academic_dataset_business.json') as f:
	for line in f:
		business = json.loads(line)
		businesses[business['business_id']] = business['city']

with open('../yelp/yelp_academic_dataset_review.json') as f:
	for line in f:
		review = json.loads(line)
		if(review['user_id'] in userset):
			userset[review['user_id']]['lived'].append(businesses[review['business_id']])
"""
