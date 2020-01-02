def InventoryAllocator(order, dist):
    order_keys = order.keys()
    res_holder = []
    result = []

    for item in order_keys:

        ord_amt = order.get(item) # Amounts of ordered items

        for d in dist:

            invent = d.get('inventory')
            dist_name = d.get('name')

            # If item is in distrubutor inventory
            if item in invent:
                
                inv_amt = invent.get(item) #  Amount of items in inventory

                # Orders are less than or equal to dist inventory
                if ord_amt <= inv_amt: 
                    res_holder.append({dist_name:{item:ord_amt}})

                    # Remove amount shipped out from inventory
                    inv_amt = inv_amt - ord_amt
                    
                    break

                # Orders are more than dist inventory
                else:
                    # Ship whatever is in distrubutor
                    res_holder.append({dist_name:{item:inv_amt}})

                    # Remove amount shipped out from inventory
                    ord_amt = ord_amt - inv_amt
                    inv_amt = 0

    # Appending all items into their respective distrubutor
    for d in dist:
        item_ship = []
        ship = {}
        dist_name = d.get('name')

        for r in res_holder:

            # Check if distrubutor name is in the shipping list
            if dist_name in r.keys():
                item_ship.append(r[dist_name])

            for item in range(1,len(item_ship)):
                item_ship[0].update(item_ship[item])
        
        # Checks if each distrubutor is atleast shipping one thing, if not then don't append
        if item_ship:
            ship[dist_name] = item_ship[0]

            result.append(ship)

    return result


def test_cases():

    # Item less than dist
    test1_ord = {'apple':4}
    test1_dist = [{'name': 'owd', 'inventory':{'apple': 5, 'orange': 10}}, {'name': 'dm', 'inventory':{'apple':10,'banana': 5, 'orange': 10}}]
    
    # Item equals dist
    test2_ord = {'apple':5}
    test2_dist = [{'name': 'owd', 'inventory':{'apple': 5, 'orange': 10}}, {'name': 'dm', 'inventory':{'apple':10,'banana': 5, 'orange': 10}}]

    # Item more than dist
    test3_ord = {'apple':6}
    test3_dist = [{'name': 'owd', 'inventory':{'apple': 5, 'orange': 10}}, {'name': 'dm', 'inventory':{'apple':10,'banana': 5, 'orange': 10}}]

    # 2 items required for shipping with the same rules for second item
    test4_ord = {'apple':5, 'orange':7}
    test4_dist = [{'name': 'owd', 'inventory':{'apple': 5, 'orange': 10}}, {'name': 'dm', 'inventory':{'apple':10,'banana': 5, 'orange': 10}}]

    # 1 item more than dist, 1 less than dist
    test5_ord = {'apple':10, 'orange':7}
    test5_dist =[{'name': 'owd', 'inventory':{'apple': 5, 'orange': 10}}, {'name': 'dm', 'inventory':{'apple':10,'banana': 5, 'orange': 10}}]
 
    # 2 items more than dist
    test6_ord = {'apple':6, 'orange':15}
    test6_dist = [{'name': 'owd', 'inventory':{'apple': 5, 'orange': 10}}, {'name': 'dm', 'inventory':{'apple':10,'banana': 5, 'orange': 10}}]

    # The other dist has item
    test7_ord = {'banana':6}
    test7_dist = [{'name': 'owd', 'inventory':{'apple': 5, 'orange': 10}}, {'name': 'dm', 'inventory':{'apple':10,'banana': 5, 'orange': 10}}]

    # Dist has no items at all
    test8_ord = {'peach':100}
    test8_dist = [{'name': 'owd', 'inventory':{'apple': 5, 'orange': 10}}, {'name': 'dm', 'inventory':{'apple':10,'banana': 5, 'orange': 10}}]


    assert InventoryAllocator(test1_ord,test1_dist) == [{'owd':{'apple':4}}]
    assert InventoryAllocator(test2_ord,test2_dist) == [{'owd':{'apple':5}}]
    assert InventoryAllocator(test3_ord,test3_dist) == [{'owd':{'apple':5}},{'dm':{'apple':1}}]
    assert InventoryAllocator(test4_ord,test4_dist) == [{'owd':{'apple':5,'orange':7}}]
    assert InventoryAllocator(test5_ord,test5_dist) == [{'owd':{'apple':5,'orange':7}},{'dm':{'apple':5}}]
    assert InventoryAllocator(test6_ord,test6_dist) == [{'owd':{'apple':5,'orange':10}},{'dm':{'apple':1,'orange':5}}]
    assert InventoryAllocator(test7_ord,test7_dist) == [{'dm':{'banana':5}}]
    assert InventoryAllocator(test8_ord,test8_dist) == []

print(test_cases()) # Should be none if everything works
