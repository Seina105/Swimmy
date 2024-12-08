def result_voting(mobs):
    votes = {}
    for mob in mobs:
        if mob.name not in votes:
            votes[mob.name] = 0
        if mob.target not in votes:
            votes[mob.target] = 1
            continue
        
        votes[mob.target] += 1