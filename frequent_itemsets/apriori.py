import pdb

def items_and_basket():
	"""
	General purpose function which  reads the transactions from a file and
	also create a list of all the items in the inventory.

	Returns
	_______

	market_basket - 2D array 
	all_items - list of all items
	"""

	with open("market_basket", "r") as handle:
		
		market_basket = []
		all_items = []

		for transaction in handle:
			row = []

			for item in transaction.split(','):
				row.append(item.strip())
				if item.strip() not in all_items:
					all_items.append(item.strip())

			market_basket.append(row)

	return market_basket, all_items
			
def support_counting(market_basket, itemset):
	"""
	Calculates the support count of "itemset" in "market_basket"
	"""
	
	return len([1 for transaction in market_basket if itemset.issubset(set(transaction))])

def candidate_generation(previous):
	"""
	Generates candidate k-itemsets from frequent (k-1)-itemset ("previos")

	Returns
	_______

	candidate_itemsets: List of all the candidate k-itemsets (unpruned)
	"""
	
	candidate_itemsets = []	
	
	i = 0
	
	while i < len(previous):
		j = i + 1
		
		while j < len(previous):

			#For each pair of itemset, if all but the last element are equal then the pair is merged into a candidate 
			if (previous[i] != previous[j]) and (previous[i][:-1] == previous[j][:-1]):
				candidate_itemsets.append(sorted(set(previous[i]).union(set(previous[j]))))
			j += 1

		i += 1

	return candidate_itemsets

def candidate_pruning(market_basket, candidate_itemsets, previous):
	"""
	For each candidate k-itemset, if all it's (k-1) subsets are not frequent (with lesser support count)
	then the candidate itemset is removed. Such pruned set of candidate k-itemset is returned.

	Returns
	_______

	pruned_itemsets: List of all the candidate k-itemsets after pruning.
	"""

	pruned_itemsets = []
	
	for itemset in candidate_itemsets:

		index = 0

		#Checks if each of (k-1) subsets are frequent
		for item in itemset:
			if sorted((set(itemset) - {item})) not in previous:
				break
			index += 1
		
		if index == len(itemset):
			pruned_itemsets.append(itemset)

	return pruned_itemsets
			

def apriori_gen(market_basket, previous):
	"""
	An interface for the above methods of candidate_generation() and candidate_pruning()
	"""

	candidate_itemsets = candidate_generation(previous)
	candidate_itemsets = candidate_pruning(market_basket, candidate_itemsets, previous)
	
	return candidate_itemsets

def generate_frequent_itemset(market_basket, all_items, minsup):
	"""
	Major algorithm which generates the frequent itemsets for a market basket. In this implementation,
	the candidate itemsets are generated by {F_(k-1) x F_(k-1)} method. These generated itemsets are then checked for
	their support count, ones with more than the threshold (minsup) are retained as frequent itemsets.

	Returns
	_______

	frequent_itemsets: List of all the frequent itemsets of a market basket
	"""

	k = 1
	flag = True

	#find the frequent 1-itemsets, the list is sorted for future convenience
	frequent_itemsets = []
	previous = sorted([[item] for item in all_items if support_counting(market_basket, {item}) >= (len(market_basket) * minsup)])
	frequent_itemsets.append(previous)

	while flag:

		k += 1
		candidate_itemsets = apriori_gen(market_basket, previous)
		current = [itemset for itemset in candidate_itemsets if support_counting(market_basket, set(itemset)) >= (len(market_basket) * minsup)]
	
		if not current:
			flag = False
		else:
			frequent_itemsets.append(current)
			previous = current
	
	return frequent_itemsets	

if __name__ == "__main__":
	
	market_basket, all_items = items_and_basket()
	frequent_itemsets = generate_frequent_itemset(market_basket, all_items, 0.6)

	for itemset in frequent_itemsets:
		print(itemset)
