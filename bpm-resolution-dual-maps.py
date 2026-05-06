import re
import bisect

OLD_RESOLUTION = 480
NEW_RESOLUTION = 480





def build_time_map(bpm_events, resolution):
    times = []
    total_time = 0.0

    for i, (tick, bpm) in enumerate(bpm_events):
        if i > 0:
            prev_tick, prev_bpm = bpm_events[i - 1]
            delta_ticks = tick - prev_tick
            beats = delta_ticks / resolution
            total_time += beats * (60.0 / prev_bpm)
        times.append(total_time)

    return times


# ----------------------------
# Parse SyncTrack BPM markers
# ----------------------------
def parse_synctrack(sync_text):
    bpm_events = []
    for line in sync_text.splitlines():
        m = re.search(r'(\d+)\s*=\s*B\s*(\d+)', line)
        if m:
            tick = int(m.group(1))
            bpm = int(m.group(2)) / 1000.0
            bpm_events.append((tick, bpm))
    bpm_events.sort()
    return bpm_events

# ---------------------------------------
# Convert ticks -> seconds (old tempo)
# ---------------------------------------
def ticks_to_seconds(ticks, bpm_events, time_map, resolution):
    index = bisect.bisect_right([t for t, _ in bpm_events], ticks) - 1
    index = max(0, index)

    segment_start_tick, bpm = bpm_events[index]
    segment_start_time = time_map[index]

    delta_ticks = ticks - segment_start_tick
    beats = delta_ticks / resolution
    delta_time = beats * (60.0 / bpm)

    return segment_start_time + delta_time
# ---------------------------------------
# Build time map for new tempo map
# ---------------------------------------
def build_new_time_map(bpm_events):
    times = []
    total_time = 0.0

    for i, (tick, bpm) in enumerate(bpm_events):
        if i > 0:
            prev_tick, prev_bpm = bpm_events[i - 1]
            delta_ticks = tick - prev_tick
            beats = delta_ticks / NEW_RESOLUTION
            total_time += beats * (60.0 / prev_bpm)
        times.append(total_time)

    return times

# ---------------------------------------
# Convert seconds -> ticks (new tempo)
# ---------------------------------------
def seconds_to_ticks_new(seconds, bpm_events, time_map):
    # Find which BPM segment this time falls in
    index = bisect.bisect_right(time_map, seconds) - 1
    index = max(0, index)

    segment_start_time = time_map[index]
    segment_start_tick, bpm = bpm_events[index]

    delta_time = seconds - segment_start_time
    beats = delta_time / (60.0 / bpm)
    delta_ticks = beats * NEW_RESOLUTION

    return int(round(segment_start_tick + delta_ticks))

# ---------------------------------------
# Convert ExpertSingle notes
# ---------------------------------------
def convert_notes(notes_text, old_bpm_events, new_bpm_events):
    old_time_map = build_time_map(old_bpm_events, OLD_RESOLUTION)
    new_time_map = build_time_map(new_bpm_events, NEW_RESOLUTION)

    output_lines = []

    for line in notes_text.splitlines():
        m = re.search(r'(\d+)\s*=\s*N\s*(\d+)\s*(\d+)', line)
        if m:
            tick = int(m.group(1))
            note = m.group(2)
            length = int(m.group(3))

            # Convert start
            start_seconds = ticks_to_seconds(
                tick, old_bpm_events, old_time_map, OLD_RESOLUTION
            )
            new_tick = seconds_to_ticks_new(
                start_seconds, new_bpm_events, new_time_map
            )

            # Convert sustain
            if length > 0:
                end_seconds = ticks_to_seconds(
                    tick + length, old_bpm_events, old_time_map, OLD_RESOLUTION
                )
                new_end_tick = seconds_to_ticks_new(
                    end_seconds, new_bpm_events, new_time_map
                )
                new_length = new_end_tick - new_tick
            else:
                new_length = 0

            output_lines.append(f"  {new_tick} = N {note} {new_length}")
        else:
            output_lines.append(line)

    return "\n".join(output_lines)

# ---------------------------------------
# USAGE
# ---------------------------------------

with open("old_sync.txt", "r") as f:
    old_sync_text = f.read()

with open("new_sync.txt", "r") as f:
    new_sync_text = f.read()

with open("expert.txt", "r") as f:
    notes_text = f.read()

old_bpm_events = parse_synctrack(old_sync_text)
new_bpm_events = parse_synctrack(new_sync_text)

converted_notes = convert_notes(notes_text, old_bpm_events, new_bpm_events)

with open("expert_converted.txt", "w") as f:
    f.write(converted_notes)

print("Conversion complete.")