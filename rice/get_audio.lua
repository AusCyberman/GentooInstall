function conky_get_audio()
	local commandpre = "pactl list sinks " 
	local volume = 0
	local handle = io.popen(commandpre)
	local sound = handle:read("*a")
	handle:close()	
	local i = 0
	local mi = 0
	local output = ""
	local muteval = "no"
	local artist
	local album
	local track
	handle = io.popen("playerctl -l")
	local media = handle:read("*a")
	handle:close()
	handle = io.popen("pactl list sinks short")
	local audio_id = string.match(handle:read("*a"),"(%d)%s+alsa_output.usb")
	handle:close()	
	if string.find(media,"spotify") ~= nil then
		media = true
		handle = io.popen("playerctl metadata")
		local metadata = handle:read("*a")
		handle:close()
		for line in string.gmatch(metadata,"[^\r\n]+") do
			local buf
			buf = string.match(line,":artist[%s]+([^\n]+)")
			if buf ~= nil then
				artist = buf
			end
                        buf = string.match(line,":album[%s]+([^\n]+)")
                        if buf ~= nil then
				album = buf
                        end
			buf = string.match(line,":title[%s]+([^\n]+)")
                        if buf ~= nil then
				title = buf
                        end
		end
	else
		media = false
	end
	if audio_id ~=nil then
		for line in string.gmatch(sound, "[^\r\n]+") do
			v,s = string.match(line,"^%s+Volume:(.+)")
			if v ~= nil then
				if i == tonumber(audio_id) then
					m = string.match(v,"%d+[^%d]+(%d+)")
					volume=m	
				end
				i=i+1
			end
			m = string.match(line,"^%s+Mute: (.+)")	
			if m ~= nil then
				if mi == tonumber(audio_id) then
					mute = m
				end
				mi=mi+1	
			end
		end
	end
	if media == true then
		output = output .. ":1:c:2:DBD89e:1:"
		handle = io.popen("playerctl status")
		local playstatus = handle:read("*a")
		if playstatus == "Paused\n" then
			output = output .. "  "
		elseif playstatus == "Playing\n" then
			output = output .. "  "
		end
		output = output .. title .. " - " .. artist  
	end
	if audio_id ~= nil then
		output = output .. ":1:c:2:9ecbdb:1:"
		if mute == "yes" then
			output = output .. "  "
		else 
			volume = tonumber(volume)
			if volume < 10 then
				output = output ..  "  "
			elseif volume > 60 then
				output = output .. "  "
			elseif volume > 10 then
				output = output .. "  "
			end
		end

		output = output .. volume .. "%"
	end
	if media == true or audio_id ~= nil then
		output =  output .. " ::"
	end
	return output
end
conky_get_audio()
