"""Pure fixed-membership Raft direct-commit counting rule."""
def advance_commit(current_term, log_terms, match_indexes, commit_index):
    integer = lambda x: type(x) is int
    if not integer(current_term) or current_term < 1:
        raise ValueError("current_term")
    if type(log_terms) is not list or len(log_terms) > 64:
        raise ValueError("log_terms")
    if any(not integer(x) or not 1 <= x <= current_term for x in log_terms):
        raise ValueError("entry term")
    if any(a > b for a,b in zip(log_terms,log_terms[1:])):
        raise ValueError("term order")
    length=len(log_terms)
    if type(match_indexes) is not list or not 1 <= len(match_indexes) <= 31:
        raise ValueError("membership")
    if any(not integer(x) or not 0 <= x <= length for x in match_indexes):
        raise ValueError("match index")
    if match_indexes[0] != length:
        raise ValueError("leader match")
    if not integer(commit_index) or not 0 <= commit_index <= length:
        raise ValueError("commit index")
    quorum=len(match_indexes)//2+1
    eligible=[]
    for index in range(commit_index+1,length+1):
        if log_terms[index-1] == current_term and sum(m >= index for m in match_indexes) >= quorum:
            eligible.append(index)
    new_commit=eligible[-1] if eligible else commit_index
    return {"new_commit":new_commit,
            "newly_committed":list(range(commit_index+1,new_commit+1)),
            "eligible_current_term":list(eligible)}
