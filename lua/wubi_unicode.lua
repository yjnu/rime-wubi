-- Unicode
-- 示例：输入 zu62fc 得到「拼」
-- 额外功能: 输入 zi 提示 Symbols

local function yieldCandidate(seg, text, desc)
    yield(Candidate("unicode", seg.start, seg._end, text, desc))
end

local function unicode(input, seg, env)
    local composition = env.engine.context.composition
    if (composition:empty()) then return end
    local segment = composition:back()

    -- 与本功能无关, 给 Symbos 输入加入提示
    if string.find(input, '^zi') ~= nil then
        segment.prompt = "〔".. "Symbols".. "〕"
        local symbols = string.sub(input, 3)
        if #symbols == 0 then
            yieldCandidate(seg, "Symbols 输入", "")
        end
        return
    end

    if string.find(input, '^zu') ~= nil then
        segment.prompt = "〔".. "Unicode".. "〕"
        local ucodestr = string.sub(input, 3)

        -- 检查是否只包含十六进制字符
        for i = 1, #ucodestr do
            local char = string.sub(ucodestr, i, i)
            if not (char >= '0' and char <= '9') and not (char >= 'a' and char <= 'f') then
                yieldCandidate(seg, "Unicode Error", "Only 0-9 or a-f")
                return
            end
        end

        if #ucodestr > 0 and #ucodestr < 7 then
            if #ucodestr < 4 then
                yieldCandidate(seg, #ucodestr .. " 个Unicode", "输入中~~~")
                return
            end
            
            local code = tonumber(ucodestr, 16)   -- 十六进制转十进制
            if code > 0x10FFFF then
                yieldCandidate(seg, "Unicode Error", "无效, 大于 0x10FFFF")
                return
            end

            for i = 1, 16 do
                ------              十进制数转为字符    注释显示十六进制数     -----
                yieldCandidate(seg, utf8.char(code), string.format("%x", code))
                code = code + 1
            end
        elseif #ucodestr == 0 then
            yieldCandidate(seg, "[0-9a-f]{4,6}", "Unicode输入")
        else 
            yieldCandidate(seg, "Unicode Error", "最多输入六位")
        end
    end
end

return unicode