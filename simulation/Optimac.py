import random as rd


def get_ordered_actions(motivations,list_actions):
    """
    Return actions orderded by their preferences.
    """
    sorting_key = lambda item: (item[1],rd.random())
    return sorted(motivations.items(),key=sorting_key, reverse=True)

def assign_action(participant,n, list_actions, allocated_actions):
    """
    args:
    -   participant :: dict | object from Participant class in its dict representation
    -   n :: int | counter
    -   list_actions :: dict list | dict of actions : {action_name : {target_proportion: float, current: float, minimum : int}}
    -   participants_allocated_actions :: (int, str, float) list | (value of n, label of the action, motivation of the participant for this action) list


    side-effects:
    -   fills participants_allocated_actions up

    Finds the best action for the given participant (represented by their id_number and motivations).

    Assigns said action to the participant and update the current matching (allocated actions)
    """
    id_number = participant["id"]
    motivations = participant["motivations"]

    ordered_actions = get_ordered_actions(motivations,list_actions)

    for label, value in ordered_actions:

        action = list_actions[label]
        if (n/(n+1))*action['current'] < action['target'] or (n * action['current'] < action['minimum']):
            update_action_proportions(n, list_actions, label)
            allocated_actions.append((id_number, label, value))
            return


def update_action_proportions(n, list_actions, assigned_label):
    """
    Updates the 'current' proportions of all actions after assignment.
    """
    assigned_action = list_actions[assigned_label]
    assigned_action['current'] = (assigned_action['current'] * n + 1) / (n + 1)
    for other in list_actions:
        if other != assigned_label:
            list_actions[other]['current'] = (list_actions[other]['current'] * n) / (n + 1)


def allocate_actions_to_participants(part_df, list_actions):
    """
    Main function to iterate over participants and assign actions.
    Returns the list of allocated actions.
    args:
    -   partdf :: dict panda dataframe | dataframe of Participants objects (in their dict representation)
    -   list_actions :: dict dict | list of actions 
    (represented by a dict {action (:str) :{target (:float), current(:float), minimum (:int) }})
    
    returns : 
    -   participants_allocated_actions :: (int, str, float) list | (value of n, label of the action, motivation of the participant for this action) list
    """
    n = 0
    participants_allocated_actions = []
    for i in range(len(part_df)):
        n = assign_action(part_df.iloc[i], n, list_actions, participants_allocated_actions)
    return participants_allocated_actions

def allocate_actions_to_participants_list(part_list, list_actions):
    """
    Main function to iterate over participants and assign actions.
    Returns the list of allocated actions.
    args:
    -   part_list :: disct list | list of Participants objects (in their dict representation)
    -   list_actions :: dict dict | list of actions 
    (represented by a dict {action (:str) :{target (:float), current(:float), minimum (:int) }})
    
    returns : 

    -   participants_allocated_actions :: (int, str, float) list | (value of n, label of the action, motivation of the participant for this action) list
    """
    n = 0
    participants_allocated_actions = []
    for i in range(len(part_list)):
        assign_action(part_list[i], n, list_actions, participants_allocated_actions)
        n+=1
    return participants_allocated_actions



