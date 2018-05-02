## Author: Victor Dibia

""" A set of functions to help us keep track of objects found in each frame
and assign them to groups based on computed Euclidean distance.
"""

import numpy as np
import datetime


 
def get_euclidean_distance(point_1, point_2):
    """Compute Euclidian distance between two points point_1 and point_2
    
    Arguments:
        point_1 {[type]} -- [tuple containing point_1 cordinates]
        point_2 {[type]} -- [tuple containing point_2 cordinates]
    
    Returns:
        [type] -- [returns what is probably a float of the euclidean distance]
    """

    point_1 = np.array(point_1)
    point_2 = np.array(point_2)
    return np.linalg.norm(point_1-point_2)

def get_min_euclidean_distance(focal_item, seen_object_list): 

    first_available_key = list(seen_object_list.keys())[0]

    box_center = focal_item["box_center"]
    min_dist = get_euclidean_distance(box_center,seen_object_list[first_available_key]["box_center"])
    min_item = seen_object_list[first_available_key]
    min_key = first_available_key

    for key in seen_object_list:
        current_item = seen_object_list[key]

        # we only compare euc distances for objects of same class
        # E.g we should not beb assigning a cell phone to the last known position of a cup etc.
        if (focal_item["class"] == current_item["class"]):
            current_dist = get_euclidean_distance(box_center,current_item["box_center"])
            if ( current_dist < min_dist):
                min_dist = current_dist
                min_item = current_item
                min_key = key
    
    # for the item that is closes to this box center, we set its box center value to this
    # print( "min key", min_key)
    return min_key, min_item

def next_available_group(assigned_list, full_list):
    for group in full_list:
        if group not in assigned_list:
            return group

    return None

def refresh_seen_object_list(seen_object_list, refresh_time_out):
    """Remove objects from seen_object_list that have not been seen for a while
    
    Arguments:
        seen_object_list {[type]} -- [description]
        refresh_time_out {[type]} -- [description]
    """
    expired_groups = []
    for key in seen_object_list:
        current_item = seen_object_list[key]
        time_elapsed = (datetime.datetime.now() -  current_item["last_seen_timestamep"]).total_seconds() 
        if ( time_elapsed > refresh_time_out):
            print("deleting key [ ", key, "] that has not been seen for ", refresh_time_out ,"seconds")
            expired_groups.append(key)
           
    for key in expired_groups:
        if key in seen_object_list:
             del seen_object_list[key]


def get_largest_key(seen_object_list):
    first_available_key = list(seen_object_list.keys())[0]
    max_id = seen_object_list[first_available_key]["id"]
    for key in seen_object_list:
        current_item = seen_object_list[key]
        if (current_item["id"] > max_id):
            max_id = current_item["id"]
    
    return (max_id + 1)




def get_id(tags, seen_object_list):
    # if we havent seen anything yet, we assign the current boxes and tag as our first reference point
    assigned_group_keys = []  # keep a list of groups that have been assigned .. 0,1,2,33
   
    if (len(seen_object_list) == 0):
        for i in range(len(tags)):
            object_data = {
                    "id": i, "last_seen_timestamep": datetime.datetime.now(),
                     "direction": "", "class": tags[i]["class"], "box_center": tags[i]["box_center"]
                    }
            seen_object_list[str(i)]=(object_data)
            tags[i]["id_label"] = str(i)
         
    else:
        
        for i in range(len(tags)):
            if(i >= len(seen_object_list)):

                next_group_index = get_largest_key(seen_object_list)
                print("Adding new group", next_group_index )

                object_data = {
                    "id": next_group_index, "last_seen_timestamep": datetime.datetime.now(),
                     "direction": "", "class": tags[i]["class"], "box_center": tags[i]["box_center"]
                    }
                
                seen_object_list[str(next_group_index)]=(object_data)
                tags[i]["id_label"] = str(next_group_index)
            else:
                # if this is a box we have see previously, we find the last object with the closes euclidean distance
                min_key, item = get_min_euclidean_distance(tags[i],seen_object_list)

                # assign the box cordinate of the current box as the last seen box center for this object.
                if (min_key in assigned_group_keys):
                    min_key = next_available_group(assigned_group_keys, list(seen_object_list.keys()) )
                    print(" >>............Noo! Assigning next available group", min_key)
                
                # assign the box cordinate of the current box as the last seen box center for this object.
                seen_object_list[min_key]["box_center"] = tags[i]["box_center"]
                seen_object_list[min_key]["last_seen_timestamep"] = datetime.datetime.now()
                

                assigned_group_keys.append(min_key)
                tags[i]["id_label"] = item["id"]
                 
 
 