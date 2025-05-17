-- 创建时间: 2025-04-14 02:25
-- 三个功能 ① 只显示三个候选项, 当输入编码数大于三个时, 取消限制  ② 清空 comment  ③ 适配多行词组
-- 功能说明: 
-- ① 最终重码太多时, 只显示三个候选项, 要翻页不方便
-- ② 反查和输入 symbol 时取消限制
-- ③ comment 全部清空, 候选多时保留, 系统自带的没那么灵活
-- ④ 注意: 只显示三个候选项后, 翻页功能失效, 无法显示之后的候选项, 但 Rime 可以在输入的时候切换开关
-- ⑤ 增加多行词组

-- 获取字符串的长度（任何单个字符长度都为1）
-- 注: 由于编码格式的原因，【#字符串】 的方式获取中文时是字节数量，所以按照视觉效果来说会觉得返回有误
function getStringLength(inputstr)
    if not inputstr or type(inputstr) ~= "string" or #inputstr <= 0 then  --inputstr不为nil、类型为字符串、且长度不为0
        return nil
    end
    local length = 0  -- 字符的个数
    local i = 1       --累计的每个字符的字节数，如果 i = 0，那么跳出while条件就是  i >= #intutstr 或 i == #inputstr
    while true do     --这里我们是通过获取一个字符的头字节来判断是几字节的，如汉字的头字节ASCII是大于223的，所以直接跳过后面2个字节的判断，byteCount = 3
        local curByte = string.byte(inputstr, i)  --获取单个字节的ASCII码
        local byteCount = 1                       --单个字符的字节数，根据ASCII判断字节数
        if curByte > 239 then
            byteCount = 4  -- 4字节字符
        elseif curByte > 223 then
            byteCount = 3  -- 汉字，3字节
        elseif curByte > 128 then
            byteCount = 2  -- 双字节字符
        else
            byteCount = 1  -- 单字节字符
        end
        -- local char = string.sub(inputstr, i, i + byteCount - 1)
        -- print(char)  -- 打印单个字符
        i = i + byteCount
        length = length + 1
        if i > #inputstr then
            break
        end
    end
    return length
end

local function only_three_candidates(input, env)
    local context = env.engine.context
    local code = env.engine.context.input        -- 输入的编码
    local code_size = #code                      -- 编码长度
    local notpreset_str = true                   -- code 是否是预设列表中的编码, 默认不是
    local count = 0 

    -- z 开头的编码, 不做限制, 但只有一个 z 时, 只显示上一次输入的词
    if code:sub(1, 1) == "z" then 
        if code_size > 1 then
            for cand in input:iter() do yield(cand) end
        else
            for cand in input:iter() do
                if cand.type == "table" then
                    cand.comment = "Last Input" 
                    yield(cand)
                    -- 如果是单字，可重复二次和三次，减少输入强度
                    if getStringLength(cand.text) == 1 then
                        yield(Candidate("last_input", cand.start, cand._end, cand.text .. cand.text , "梅开二度"))
                        yield(Candidate("last_input", cand.start, cand._end, cand.text.. cand.text.. cand.text, "帽子戏法"))
                    end
                    -- log.warning( cand.text .. " " .. #cand.text )
                else
                    yield(Candidate("z", 0, 1, "Z", "echo"))  
                end
                break
            end
        end
        return
    end

    -- 为之后兼容多个编码而准备的例外预设列表, 只匹配开头, 放在这就只用计算一次
    -- if code_size > 1 then
    --     local preset = {
    --         "^ob",
    --     }
    --     for i = 1, #preset do
    --         if string.find(code, preset[i]) ~= nil then
    --             notpreset_str = false
    --             break
    --         end
    --     end
    -- end
    
    -- 如果只有一个例外, 就用一行代码 
    if code_size > 1 and code:sub(1, 2) == "ob" then notpreset_str = false end

    -- 过滤
    for cand in input:iter() do
        -- 输入的编码小于 4 才限制候选数量和清空 comment, notpreset_str 为例外情况, 即直接显示
        if notpreset_str and code_size < 4 then 
            if env.engine.context:get_option("only_three_candidates") then
                count = count + 1
                if count > 3 then break end
            end
            -- 如果不是 zhuyin 类型 或 开启了清空 comment, 则清空 comment
            if context:get_option("clear_comment") then 
                if cand.type ~= "zhuyin" then 
                    cand.comment = "" 
                end
            end
        end
        
        -- 添加换行符, 适配多行词组
        newCand = cand.text      -- filter 里要更改 cand.text 只能用新变量，并生成一个新的 cand
        if string.match(newCand, "\\n") then
            -- newCand = string.gsub(newCand, "$20", " ")
            newCand = string.gsub(newCand, "\\n", "\n")
            yield(Candidate("lf", cand.start, cand._end, newCand, "多行词组"))
        else
            yield(cand)
        end
    end
end

return only_three_candidates
