-- help 快捷键使用说明
-- 示例：输入 zhelp 显示可用的快捷键及功能
-- 示例：输入 zinfo 显示 rime 信息

local function docRime(input, seg, env)
    local composition = env.engine.context.composition
    if (composition:empty()) then return end
    local segment = composition:back()

    if string.find(input, "^help") ~= nil then
        segment.prompt = "〔" .. "快捷键说明" .. "〕"

        local wubi_helpSet = {
            { '<CS> F4', '方案选择' },
            { '<CS> F5', '最近两个方案切换' },
            { '<CS> F6', 'emoji开关' },
            { '<CS> F7', '切换到五笔单字方案' },
            { '<CS> F8', '候选词数量限制' },
            { '<CS> F9', '清空注释' },
            { '<CS> |', '常用字过滤' },
            { 'ZV', '数字大写' },
            { 'ZU', 'Unicode编码转字符' },
            { 'R_Shift', '中英切换' },
            { '<C> .', '中英标点切换' },
            { '<CS> Space', '半角全角切换' },
            { '<C> \\', '简繁切换' },
            { '<C> H', '删除前一个字符' },
            { '<C> J', '光标下移' },
            { '<C> K', '光标上移' },
            { '<C> L', '注释上屏'},
            { '<C> Enter', '清码' },
            { 'time', '时间' },
            { 'date', '日期' },
            { 'dati', '日期时间' },
            { 'week', '星期' },
            { 'mont', '月份' },
            { 'luna', '农历' },
            { 'help', '使用说明'},
            { 'info', 'rime 信息' }
        }
        
        if env.engine.schema.schema_id == 'wubi' then
            for _, pair in ipairs(wubi_helpSet) do yield(Candidate("helper", seg.start, seg._end, pair[1], pair[2])) end
        else
            yield(Candidate("helper", seg.start, seg._end, "此方案没有帮助", ""))
        end
    elseif string.find(input, "^info") ~= nil then
        segment.prompt = "〔" .. "软件信息" .. "〕"
        local rimeName = rime_api.get_distribution_code_name() .. ' ' .. rime_api.get_distribution_name()
        local rimeDir = string.sub(rime_api.get_shared_data_dir(), 1, -6)
        local luaVer = string.sub(_VERSION, 5)
        yield(Candidate("helper", seg.start, seg._end, rimeName, '输入法名字'))
        yield(Candidate("helper", seg.start, seg._end, rime_api.get_distribution_version(), '输入法版本'))
        yield(Candidate("helper", seg.start, seg._end, rime_api.get_rime_version(), 'librime 版本'))
        yield(Candidate("helper", seg.start, seg._end, luaVer, 'lua 版本'))
        yield(Candidate("helper", seg.start, seg._end, rimeDir, '程序数据目录'))
        yield(Candidate("helper", seg.start, seg._end, rime_api.get_user_data_dir(), '用户数据目录'))
        yield(Candidate("helper", seg.start, seg._end, env.engine.schema.schema_name, '目前使用方案'))
    end
end

return docRime
