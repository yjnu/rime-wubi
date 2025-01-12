local function wubi_provisional_english(input, seg)
    if string.find(input, "^ze") ~= nil then
        local result = string.sub(input, 3)
        -- if string.find(input, "^//") ~= nil then
        --     return
        -- end
        if #result == 0 then
            can = Candidate("en", seg.start, seg._end, result, "临时英文模式")
            can.quality = 100
            yield(can)
            return
        end
        
        
        local result2 = string.upper(result:sub(1, 1)) .. result:sub(2)
        local Uresult = string.upper(result)
        can1 = Candidate("en", seg.start, seg._end, result2, "首字大写")
        can2 = Candidate("en", seg.start, seg._end, Uresult, "大写英文")
        can1.quality = 100
        can2.quality = 100

        if #result == 1 then
            yield(can2)
        else
            yield(can1)
            yield(can2)
        end
    end
end

return wubi_provisional_english