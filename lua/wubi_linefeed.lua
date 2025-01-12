-- linefeed
-- 示例：输入 zo 显示 多行输出 
-- 这是笨方法, 不好用但也能用, 因为多行输入的情况很少

local function linefeed(input, seg, env)
    local composition = env.engine.context.composition
    if (composition:empty()) then return end
    local segment = composition:back()

    if string.find(input, "^zo") ~= nil then
        segment.prompt = "〔" .. "Linefeed" .. "〕"
        local code = string.sub(input, 3)

        -- 列出候选目录
        if #code == 0 then
            can1 = Candidate("lf", seg.start, seg._end, "abcd", "ab")
            yield(can1)
            return
        end

        -- 编写候选
        errorcode = Candidate("lf", seg.start, seg._end, "Code Error", "无多行预存")
        zoab = Candidate("lf", seg.start, seg._end, "a.\nb.\nc.\nd.", "选项")
        zoac = Candidate("lf", seg.start, seg._end, "第一行\n" .. "第二行\n", "多行")
        
        -- 显示候选, 需加两次
        if #code == 2 then        
            if code == "ab" then
                yield(zoab)
            elseif code == "ac" then
                yield(zoac)
            else
                yield(errorcode)
            end
        elseif #code == 1 then
            if code == "a" then
                yield(zoab)
                yield(zoac)
            else
                yield(errorcode)
            end
        else
            yield(errorcode)
        end
    end
end

return linefeed