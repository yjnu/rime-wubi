-- 日期转换, 可输入:
-- dati
-- date
-- time
-- week 
-- month


local function yield_cand(seg, text, comment)
    local cand = Candidate("date", seg.start, seg._end, text, comment)
    cand.quality = 100  -- Increase the weight to display it at the top.
    yield(cand)
end

function wubi_date_translator(input, seg, env)
    local composition = env.engine.context.composition
    if (composition:empty()) then return end
    local segment = composition:back()
    
    -- 日期格式化说明：
    -- %a	abbreviated weekday name (e.g., Wed)
    -- %A	full weekday name (e.g., Wednesday)
    -- %b	abbreviated month name (e.g., Sep)
    -- %B	full month name (e.g., September)
    -- %c	date and time (e.g., 09/16/98 23:48:10)
    -- %d	day of the month (16) [01-31]
    -- %H	hour, using a 24-hour clock (23) [00-23]
    -- %I	hour, using a 12-hour clock (11) [01-12]
    -- %M	minute (48) [00-59]
    -- %m	month (09) [01-12]
    -- %p	either "am" or "pm" (pm)
    -- %S	second (10) [00-61]
    -- %w	weekday (3) [0-6 = Sunday-Saturday]
    -- %W	week number in year (48) [01-52]
    -- %x	date (e.g., 09/16/98)
    -- %X	time (e.g., 23:48:10)
    -- %Y	full year (1998)
    -- %y	two-digit year (98) [00-99]
    -- %%	the character `%´
    local yearWeekTab = {
        [0] = '〇', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', 
        '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十', 
        '二十一', '二十二', '二十三', '二十四', '二十五', '二十六', '二十七', '二十八', '二十九', '三十', 
        '三十一', '三十二', '三十三', '三十四', '三十五', '三十六', '三十七', '三十八', '三十九', '四十', 
        '四十一', '四十二', '四十三', '四十四', '四十五', '四十六', '四十七', '四十八', '四十九', '五十', 
        '五十一', '五十二', '五十三', '五十四'
    } -- 默认索引从 1 开始, 但加了 [0]= 后, 索引从 0 开始
    -- date and time
    if (input == "dati") then
        segment.prompt = "日期时间"
        yield_cand(seg, os.date("%Y-%m-%d %H:%M"), "日时分")
        yield_cand(seg, os.date("%Y/%m/%d %H:%M:%S"), "日时分秒")
        yield_cand(seg, os.date("%Y%m%d%H%M"), "纯数字")
        yield_cand(seg, os.date("%Y-%m-%dT%H:%M:%S+08:00"), "东八区标准格式")

    -- date
    elseif (input == "date") then
        segment.prompt = "日期"
        local CapitalYear = ""
        for i = 1, 4 do
            CapitalYear = CapitalYear..yearWeekTab[tonumber(string.sub(os.date("%Y"), i, i))]   -- 索引从 1 开始,需加一
        end
        local CapitalDate = CapitalYear.."年"..yearWeekTab[tonumber(os.date("%m"))].."月"..yearWeekTab[tonumber(os.date("%d"))].."日"
        yield_cand(seg, os.date("%Y/%m/%d"), "//日//")
        yield_cand(seg, os.date("%Y%m%d"), "纯数字")
        yield_cand(seg, CapitalDate, "大写")
        yield_cand(seg, os.date("%Y-%m-%d"), "--日--")
        yield_cand(seg, os.date("%Y年%m月%d日"), "中文")
        yield_cand(seg, os.date("%Y.%m.%d"), "..日..")
        yield_cand(seg, os.date("%m-%d-%Y"), "年在后")

    -- time and timestamp
    elseif (input == "time") then
        segment.prompt = "时间"
        local shichen = {
            { name = "子时", alias = "夜半 | 三更" },   -- 23:00 - 01:00
            { name = "丑时", alias = "鸡鸣 | 四更" },   -- 01:00 - 03:00
            { name = "寅时", alias = "平旦 | 五更" },   -- 03:00 - 05:00
            { name = "卯时", alias = "日出" },         -- 05:00 - 07:00
            { name = "辰时", alias = "食时" },         -- 07:00 - 09:00
            { name = "巳时", alias = "隅中" },         -- 09:00 - 11:00
            { name = "午时", alias = "日中" },         -- 11:00 - 13:00
            { name = "未时", alias = "日昳" },         -- 13:00 - 15:00
            { name = "申时", alias = "晡时" },         -- 15:00 - 17:00
            { name = "酉时", alias = "日入" },         -- 17:00 - 19:00
            { name = "戌时", alias = "黄昏 | 一更" },   -- 19:00 - 21:00
            { name = "亥时", alias = "人定 | 二更" }    -- 21:00 - 23:00
        }
        local hour = math.floor((os.date("%H") + 1) / 2) % 12 + 1
        local ancientTime = shichen[hour].name.."("..shichen[hour].alias..")"
        yield_cand(seg, os.date("%H:%M"), ancientTime)
        yield_cand(seg, os.date("%H:%M:%S"), "时分秒")
        yield_cand(seg, string.format('%d', os.time()), "时间戳")
        yield_cand(seg, ancientTime, "大写")

    -- week
    elseif (input == "week") then
        segment.prompt = "星期"
        local weekTab = {'日', '一', '二', '三', '四', '五', '六'}
        local weekCount = yearWeekTab[tonumber(os.date("%W"))]
        yield_cand(seg, "周"..weekTab[tonumber(os.date("%w")+1)], "第"..weekCount.."周")
        yield_cand(seg, "星期"..weekTab[tonumber(os.date("%w")+1)], "第"..os.date("%W").."周")
        yield_cand(seg, os.date("%A"), "英文")   
        yield_cand(seg, os.date("%a"), "缩写")
        yield_cand(seg, weekCount, "周数")
        yield_cand(seg, os.date("%W"), "数字周")

    -- month
    elseif (input == "month") then
        segment.prompt = "月份"
        yield_cand(seg, os.date("%B"), "英文")
        yield_cand(seg, os.date("%b"), "缩写")
    end
end

return wubi_date_translator
