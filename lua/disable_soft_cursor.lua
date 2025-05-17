-- 不显示输入法中右小角的光标
-- 来源于 github 上我问的问题, 开发给我的解答
-- 好像只能在 Windows 中使用

-- 猜测操作系统类型
local function guess_os(env)
    -- 检查路径分隔符（Windows 用 "\"，Unix用 "/"）
    local path_sep = package.config:sub(1,1)
    if path_sep == "\\" then
        return "Windows"
    else
        return "Linux"
    end
end

-- 禁用软光标
local function disable_soft_cursor(key, env)
    -- local OSName = guess_os(env)
    -- if OSName == "Windows" then
        local context = env.engine.context
        local soft_cursor = context:get_option("soft_cursor")
        if soft_cursor == nil or soft_cursor == true then
            context:set_option("soft_cursor", false)
        end
        return 2     -- 表示 kNoop, 声称本函数不响应该输入事件，交给接下来的处理器决定
    -- end
end

return disable_soft_cursor
