"""Finite coverage and pure guard selection model, not Rust execution."""


def enum_match_analysis(variants, arms, values, non_exhaustive=False, outside_crate=False):
    covered = set()
    catch_all = False
    for arm in arms:
        if arm["guard"] is None:
            if arm["pattern"] == "*":
                catch_all = True
            else:
                covered.add(arm["pattern"])
    missing = [tag for tag in variants if not catch_all and tag not in covered]
    future_missing = non_exhaustive and outside_crate and not catch_all
    decisions = []
    for value in values:
        selected = None
        tested = []
        for index, arm in enumerate(arms):
            if arm["pattern"] != "*" and arm["pattern"] != value["tag"]:
                continue
            if arm["guard"] is not None:
                tested.append(index)
                if not value["guards"][arm["guard"]]:
                    continue
            selected = index
            break
        decisions.append({"selected": selected, "tested_guards": tested})
    return {"missing": missing, "future_missing": future_missing,
            "exhaustive": not missing and not future_missing, "decisions": decisions}
