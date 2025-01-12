--[[
	自动大写英文词汇：
	- 部分规则不做转换
	- 输入首字母大写，候选词转换为首字母大写： Hello → Hello
	- 输入至少前 2 个字母大写，候选词转换为全部大写： HEllo → HELLO
--]]

local function autocap_filter(input, env)
    local code = env.engine.context.input -- 输入码
    local codeLen = #code
    local codeAllUCase = false
    local codeUCase = false
    -- 不转换：
    if codeLen == 1 or       -- 码长为 1
        code:find("^[%p]")   -- 输入码首位为标点
    then
        for cand in input:iter() do
            yield(cand)
        end
        return
    ---- 输入码全大写
    -- elseif code == code:upper() then
    --     codeAllUCase = true
    -- 输入码前 2 - n 位大写
    -- elseif code:find("^%u%u+.*") then
    --     codeAllUCase = true
    -- 输入码首位大写
    --  elseif code:find("^%u.*") then
    --      codeUCase = true
    end

    -- local pureCode = code:gsub("[%s%p]", "")   -- 删除标点和空格的输入码
    for cand in input:iter() do
        local text = cand.text                    -- 候选词
        if
            text:find("^" .. code)                -- 输入码完全匹配候选词
        then
            local textl = text:lower()
            local textfu = text:sub(1, 1):upper() .. text:sub(2)
            local textu = text:upper()
            -- if textl == text then
            yield(cand)
            yield(Candidate(cand.type, 0, codeLen, textfu, cand.comment))
            yield(Candidate(cand.type, 0, codeLen, textu, cand.comment))
            -- elseif text == textfu then
                -- yield(cand)
                -- yield(Candidate(cand.type, 0, codeLen, textu, cand.comment))
            -- elseif text == textu then
                -- yield(cand)
            -- end
        else
            yield(cand)
        end
    end
end

return autocap_filter
