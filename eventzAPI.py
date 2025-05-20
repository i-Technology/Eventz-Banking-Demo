import uuid
import datetime

# In-memory immutable archive
Y = []

def publish(event_type, data):
    data['uuid'] = str(uuid.uuid4())
    data['event_type'] = event_type
    data['timestamp'] = data.get('timestamp', datetime.datetime.now().isoformat())
    Y.append(data)
    print(f"Published: {data}")

def read_latest(event_type, filter_dict):
    for y in reversed(Y):
        if y.get("event_type") == event_type and all(y.get(k) == v for k, v in filter_dict.items()):
            return y
    return None

def decline(event, reason):
    publish('TransactionDeclined', {
        'reason': reason,
        'original_event_uuid': event.get('uuid')
    })
def export_tsv(filename="Y_archive.tsv"):
    if not Y:
        print("Nothing to export.")
        return

    # Get all unique keys across all tuples
    all_keys = sorted(set().union(*(y.keys() for y in Y)))

    with open(filename, "w") as f:
        # Header
        f.write("\t".join(all_keys) + "\n")

        # Rows
        for y in Y:
            row = [str(y.get(k, "")) for k in all_keys]
            f.write("\t".join(row) + "\n")

    print(f"Exported {len(Y)} records to {filename}")
def export_markdown(filename="Y_report.md"):
    if not Y:
        print("No data to export.")
        return

    all_keys = sorted(set().union(*(y.keys() for y in Y)))

    with open(filename, "w") as f:
        f.write("# Eventz Immutable Archive Report\n\n")
        f.write("```\n")  # Begin monospaced block

        header = "\t".join(all_keys)
        f.write(header + "\n")
        f.write("-" * len(header) + "\n")

        for y in Y:
            row = [str(y.get(k, "")) for k in all_keys]
            f.write("\t".join(row) + "\n")

        f.write("```\n")  # End block

    print(f"Clean markdown TSV report written to {filename}")

