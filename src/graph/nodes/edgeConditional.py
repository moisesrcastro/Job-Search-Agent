def route_after_chat(state):

    if state["extract_preference"]:
        return "savePreferences"

    if state["should_search_jobs"]:
        return "searchJobs"

    if state["needs_summarization"]:
        return "summarize"

    return "end"

def route_after_save_preferences(state):

    if state["should_search_jobs"]:
        return "searchJobs"

    if state["needs_summarization"]:
        return "summarize"

    return "end"