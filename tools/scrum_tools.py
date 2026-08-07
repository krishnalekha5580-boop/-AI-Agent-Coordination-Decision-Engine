def check_sprint_progress(tasks: list) -> str:
    """
    Given a list of tasks (with id, progress_pct, planned_end), summarize sprint health:
    how many tasks are done, in progress, or not started, and flag any at risk.
    """
    try:
        if not tasks:
            return "No tasks in sprint to evaluate"

        total = len(tasks)
        done = sum(1 for t in tasks if t.get("progress_pct", 0) >= 100)
        not_started = sum(1 for t in tasks if t.get("progress_pct", 0) == 0)
        in_progress = total - done - not_started

        return (f"Sprint has {total} tasks: {done} done, {in_progress} in progress, "
                f"{not_started} not started")
    except Exception as e:
        return f"Error checking sprint progress: {str(e)}"


def flag_impediments(tasks: list) -> str:
    """
    Flag tasks that look stuck: 0% progress but very close to their deadline.
    This is a proxy for 'blocked' since we don't track a separate blocked-status field.
    """
    try:
        from datetime import datetime
        impediments = []
        for t in tasks:
            progress = t.get("progress_pct", 0)
            planned_end = t.get("planned_end")
            if not planned_end or progress > 0:
                continue
            try:
                end = datetime.strptime(planned_end, "%Y-%m-%d")
                days_left = (end - datetime.now()).days
                if days_left <= 3:
                    impediments.append(f"{t.get('id', 'unknown')} (0% done, {days_left} days left)")
            except ValueError:
                continue

        if impediments:
            return "Impediments found: " + "; ".join(impediments)
        return "No impediments detected"
    except Exception as e:
        return f"Error flagging impediments: {str(e)}"