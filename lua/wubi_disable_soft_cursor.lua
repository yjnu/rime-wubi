local function disable_soft_cursor(key, env)
	  local engine = env.engine
	  local context = engine.context
    local soft_cursor = context:get_option("soft_cursor")
    if soft_cursor == nil or soft_cursor == true then
        context:set_option("soft_cursor", false)
    end
    return 2
end

return disable_soft_cursor