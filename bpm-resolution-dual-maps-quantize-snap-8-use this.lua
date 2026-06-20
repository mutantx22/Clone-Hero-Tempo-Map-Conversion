reaper.Undo_BeginBlock()

local num_items = reaper.CountMediaItems(0)
local all_midi_data = {}

-- 1. Store absolute times of all MIDI notes across all items
for i = 0, num_items - 1 do
  local item = reaper.GetMediaItem(0, i)
  if item then
    local take = reaper.GetActiveTake(item)
    if take and reaper.TakeIsMIDI(take) then
      local item_pos = reaper.GetMediaItemInfo_Value(item, "D_POSITION")
      local _, notecnt = reaper.MIDI_CountEvts(take)
      
      local notes = {}
      for n = 0, notecnt - 1 do
        local _, selected, muted, startppqpos, endppqpos, chan, pitch, vel = reaper.MIDI_GetNote(take, n)
        -- Convert PPQ positions to absolute project time (seconds)
        local start_time = reaper.MIDI_GetProjTimeFromPPQPos(take, startppqpos)
        local end_time = reaper.MIDI_GetProjTimeFromPPQPos(take, endppqpos)
        
        table.insert(notes, {
          selected = selected,
          muted = muted,
          chan = chan,
          pitch = pitch,
          vel = vel,
          start_time = start_time,
          end_time = end_time
        })
      end
      all_midi_data[take] = notes
    end
  end
end

-- 2. Delete all tempo markers
local num_tempo_markers = reaper.CountTempoTimeSigMarkers(0)
if num_tempo_markers > 0 then
  for i = num_tempo_markers - 1, 0, -1 do
    reaper.DeleteTempoTimeSigMarker(0, i)
  end
end

-- 3. Clear old notes and rewrite them at their original absolute times
for take, notes in pairs(all_midi_data) do
  -- Clear existing notes to avoid duplicates
  local _, notecnt = reaper.MIDI_CountEvts(take)
  for n = notecnt - 1, 0, -1 do
    reaper.MIDI_DeleteNote(take, n)
  end
  
  -- Insert them back using the new project timeline mapping
  for _, note in ipairs(notes) do
    local new_start_ppq = reaper.MIDI_GetPPQPosFromProjTime(take, note.start_time)
    local new_end_ppq = reaper.MIDI_GetPPQPosFromProjTime(take, note.end_time)
    
    reaper.MIDI_InsertNote(
      take, 
      note.selected, 
      note.muted, 
      new_start_ppq, 
      new_end_ppq, 
      note.chan, 
      note.pitch, 
      note.vel, 
      true
    )
  end
  reaper.MIDI_Sort(take)
end

reaper.UpdateArrange()
reaper.Undo_EndBlock("Delete tempo markers preserving MIDI absolute time", -1)