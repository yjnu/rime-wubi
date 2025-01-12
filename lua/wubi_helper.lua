-- help 快捷键使用说明
-- 示例：输入 zhelp 显示可用的快捷键及功能
-- 示例：输入 zinfo 显示 rime 信息

local function docRime(input, seg, env)
    local composition = env.engine.context.composition
    if (composition:empty()) then return end
    local segment = composition:back()

    local helpSet = {
        { '<CS> F4', '方案选择' },
        { '<CS> F5', '最近两个方案切换' },
        { '<CS> F6', 'emoji开关' },
        { '<CS> F7', '切换到五笔方案' },
        { '<CS> |', '常用字过滤' },
        { 'ZV', '数字大写与计算器' },
        { 'ZU', 'Unicode编码转字符' },
        { 'ZI', 'Symbol符号' },
        { 'ZO', '多行输出,lua中添加词条' },
        { 'time', '时间' },
        { 'date', '日期' },
        { 'dati', '日期时间' },
        { 'week', '星期' },
        { 'month', '月份' },
        { 'luna', '农历' },
        { 'R_Shift', '中英切换' },
        { '<C> .', '中英标点切换' },
        { '<S> Space', '半角全角切换' },
        { '<C> \\', '简繁切换' },
        { '<C> Enter', '清码' },
        { 'zhelp', '你懂的'},
        { 'zinfo', 'rime 信息' }
    }
    
    if string.find(input, "^zhelp") ~= nil then
        segment.prompt = "〔" .. "快捷键说明" .. "〕"
        for _, pair in ipairs(helpSet) do
            yield(Candidate("helper", seg.start, seg._end,pair[1], pair[2]))
        end
    elseif string.find(input, "^zinfo") ~= nil then
        segment.prompt = "〔" .. "软件信息" .. "〕"
        yield(Candidate("helper", seg.start, seg._end, rime_api.get_rime_version(), '〔librime version〕'))
        yield(Candidate("helper", seg.start, seg._end, _VERSION, '[lua version]'))
        yield(Candidate("helper", seg.start, seg._end, rime_api.get_user_data_dir(), '[user data dir]'))
        yield(Candidate("helper", seg.start, seg._end, rime_api.get_shared_data_dir(), '[shared data dir]'))
        yield(Candidate("helper", seg.start, seg._end, rime_api.get_distribution_name(), '[distribution name]'))
        yield(Candidate("helper", seg.start, seg._end, rime_api.get_distribution_code_name(), '[distribution code name]'))
        yield(Candidate("helper", seg.start, seg._end, rime_api.get_distribution_version(), '[distribution version]'))
    end
end

return docRime
