-- 日期转换(文件最后有 lua 时间格式化使用说明)
-- 以下输入可以转换为时间
-- dati
-- date
-- time
-- week 
-- mont

-- 封装候选, 简化
local function yield_cand(seg, text, comment)
    local cand = Candidate("date", seg.start, seg._end, text, comment)
    cand.quality = 100
    yield(cand)
end

-- 判断是否是闰年
local function isLeap(y)
    local year = tonumber(y)
    if math.fmod(year, 400) ~= 0 and math.fmod(year, 4) == 0 or math.fmod(year, 400) == 0 then
        return 366
    else
        return 365
    end
end

-- 返回百分比字符串, 输入 0-100 的数字
local function draw_percentage(num)
    -- 这种方式不好看
    -- local passed = math.ceil(num / 10)
    -- local passed_str = string.rep("▮", 5)
    -- local remaining_str = string.rep("▯", 10 - passed)
    -- return passed_str .. remaining_str
    local full_block_num = math.floor(num/20)
    local half_block_num = math.fmod(num,20)
    if half_block == 0 then
        half_block = "▓"
    elseif half_block_num < 9 then
        half_block = "▕"
    elseif  half_block_num < 15 then
        half_block = "▐"
    else
        half_block = "█"
    end
    return  half_block .. string.rep("█", full_block_num) .. string.rep("▓", 4 - full_block_num)
end

function wubi_date_translator(input, seg, env)
    local composition = env.engine.context.composition
    if (composition:empty()) then return end
    local segment = composition:back()
    
    if #input < 4 then return end

    local istime = false
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
        segment.prompt =  "〔" .. "日期时间" .. "〕"
        yield_cand(seg, os.date("%Y-%m-%d %H:%M"), "日时分")
        yield_cand(seg, os.date("%Y/%m/%d %H:%M:%S"), "日时分秒")
        yield_cand(seg, os.date("%Y%m%d%H%M"), "纯数字")
        yield_cand(seg, os.date("%Y-%m-%dT%H:%M:%S+08:00"), "东八区标准格式")
        istime = true

    -- date
    elseif (input == "date") then
        segment.prompt =  "〔" .. "日期" .. "〕"
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
        -- yield_cand(seg, os.date("%m-%d-%Y"), "年在后")
        istime = true

    -- time and timestamp
    elseif (input == "time") then
        segment.prompt =  "〔" .. "时间" .. "〕"
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
        istime = true

    -- week
    elseif (input == "week") then
        segment.prompt =  "〔".. "星期".. "〕"
        local weekTab = {'日', '一', '二', '三', '四', '五', '六'}
        local weekCount = yearWeekTab[tonumber(os.date("%W"))]
        yield_cand(seg, "周"..weekTab[tonumber(os.date("%w")+1)], "第"..weekCount.."周")
        yield_cand(seg, "星期"..weekTab[tonumber(os.date("%w")+1)], "第"..os.date("%W").."周")
        yield_cand(seg, os.date("%A"), "英文")   
        yield_cand(seg, os.date("%a"), "缩写")
        yield_cand(seg, weekCount, "大写周数")
        yield_cand(seg, os.date("%W"), "今年第 "..os.date("%W").." 周")
        istime = true

    -- month
    elseif (input == "mont" or input == "month") then
        segment.prompt =  "〔".. "月份".. "〕"
        yield_cand(seg, os.date("%B"), "英文")
        yield_cand(seg, os.date("%b"), "缩写")
        istime = true
    end

    if istime then
        -- math.ceil 向上取整    math.floor 向下取整
        local yearDay = isLeap(tonumber(os.date("%Y")))
        local passed_day = tonumber(os.date("%j"))
        local remaining_day = yearDay - passed_day
        local progress = string.format("%.2f", passed_day/yearDay*100)
        local floor_progress = math.floor(passed_day/yearDay*100)
        yield_cand(seg, passed_day, "今年第 "..passed_day.." 天")
        yield_cand(seg, remaining_day, "今年余 "..remaining_day.." 天")
        yield_cand(seg, draw_percentage(floor_progress), "今年进度 ".. progress .." %")
    end
end

return wubi_date_translator


-- 日期格式化说明：
-- %a	abbreviated weekday name (e.g., Wed)
-- %A	full weekday name (e.g., Wednesday)
-- %b	abbreviated month name (e.g., Sep)
-- %B	full month name (e.g., September)
-- %c	date and time (e.g., 09/16/98 23:48:10)
-- %d	day of the month (16) [01-31]
-- %H	hour, using a 24-hour clock (23) [00-23]
-- %I	hour, using a 12-hour clock (11) [01-12]
-- %j	day of the year (252) [001-366]
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
-- %%	a literal '%' character (e.g., %)
-- *t	date as a table (e.g., {wday=3, yday=252, hour=23, min=48, sec=10, year=1998, month=9, day=16})
