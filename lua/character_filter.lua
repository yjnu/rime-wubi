-- 别人使用的其它方法 https://github.com/hchunhui/librime-lua/blob/master/sample/lua/charset.lua
-- 包含二个功能:  ① 非常用字过滤  ② 显示易读错的字的读音
-- 变量名不能更改, 否则 python 脚本会报错

-- 非常用字
local hanzi_set = {    
    ["峤"] = true,
    ["窨"] = true,
    ["啬"] = true,
    ["瓞"] = true,
    ["簷"] = true,
    ["咴"] = true,
    ["硗"] = true,
    ["蓓"] = true,
    [""] = true,
    ["𰻞"] = true,
    ["畝"] = true,
    ["郃"] = true,
    ["珮"] = true,
    ["菟"] = true,
    ["堇"] = true,
    ["柰"] = true,
    ["覀"] = true
}

-- 易读错的拼音
local error_prone_pronunciations = {
    ["豸"] = {comment = "zhì"},
    ["鬯"] = {comment = "chàng"},
    ["肏"] = {comment = "cào"},
    ["亨"] = {comment = "hēng"},
    ["埗"] = {comment = "bù"},
    ["𫖯"] = {comment = "fǔ"},
    ["赢"] = {comment = "yíng"},
    ["戊"] = {comment = "wù"},
    ["戌"] = {comment = "xū"},
    ["龌龊"] = {comment = "wò chuò"},
    ["旮旯"] = {comment = "gā lá"},
    ["妊娠"] = {comment = "rèn shēn"},
    ["耄耋"] = {comment = "mào dié"}
}

-- 更改提示, 如果是输入的 z 开头的编码, 则不更改
local function update_comment(cand)
    local c = error_prone_pronunciations[cand.text]
    if c and cand.type ~= "reverse_lookup" then
        cand.type = "zhuyin"        -- 更改候选类型为 zhuyin, 避免被下一个 filter 过滤掉
        cand.comment = c.comment
        -- log.warning("易读错的字: " .. cand.text .. " 类型：" .. cand.type .. " 注释：".. cand.comment)
    end
    yield(cand)
end

-- 主过滤函数
local function filter_single_candidates(input, env)
    -- 获取输入的第一个字符是不是 z, 也可以用 cand.type 来判断
    -- local inputWord = env.engine.context.input
    -- local first_word = inputWord:sub(1, 1)    
    -- if first_word == "z" then
    --     log.warning("输入的是 z 开头 " .. env.engine.schema.page_size)
    -- end

    for cand in input:iter() do
        local textlen = utf8.len(cand.text)
        if env.engine.context:get_option("character_filter") then
            if textlen == 1 then
                if not hanzi_set[cand.text] then
                    -- 如果不在字符集中，则显示候选字
                    update_comment(cand)
                elseif cand.type == "unicode" or cand.type =="reverse_lookup" then
                    -- 如果是 unicode 类型和反查类型, 一律显示
                    yield(cand)
                -- else
                    -- log.warning("被过滤的不常用字: " .. cand.text)  -- 日志输出,调试可打开
                end
            else
                -- if not env.engine.context:get_option("single_char") then  -- 单字过滤
                update_comment(cand)
            end
        else
            -- 如果没有启用字符过滤, 则将非常用字的 comment 显示为书签 🔖
            if textlen == 1 then
                if hanzi_set[cand.text] then
                    cand.comment = "🔖"
                end
                yield(cand)
            -- 开启了 single_char 选项, 则不显示, 已删除
            -- elseif not env.engine.context:get_option("single_char") then
            else    
                yield(cand)
            end
        end
    end
end

return filter_single_candidates
