#Requires AutoHotkey >=2.0- 64-bit
#SingleInstance force

; 取消注释下面这行, 则不显示托盘图标, 建议开机启动
;#NoTrayIcon

; Ctrl + Alt + ! 打开五笔字典编辑器
^!=::
{
  if (WinExist("Wubi Dict Editor")) {
    WinActivate
    controlFocus "Edit1"
  } else {
    bg_color := "454545"
    myTitle := "Wubi Dict Editor"
    AHKCMDGUI := Gui("-MinimizeBox -MaximizeBox +LastFound", myTitle)

    buildNum := Number(RegRead("HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion", "CurrentBuild"))
    isWin11 := (buildNum >= 22000)

    hwnd := AHKCMDGUI.Hwnd
    AHKCMDGUI.BackColor := bg_color
    
    iconbigsize := 128
    iconsmallsize := 64
    bigIcon := LoadPicture("./img/wubiEditor.ico", "Icon1 w" iconbigsize " h" iconbigsize, &imgtype)
    smallIcon := LoadPicture("./img/wubiEditor.ico", "Icon1 w" iconsmallsize " h" iconsmallsize, &imgtype)
    SendMessage(0x0080, 1, bigIcon, AHKCMDGUI)
    SendMessage(0x0080, 0, smallIcon, AHKCMDGUI)

    if (isWin11) {
      centerX := A_ScreenWidth // 2
      centerY := A_ScreenHeight // 2
      brightness := GetAreaBrightnessFast(centerX, centerY, 15)
      dark := Buffer(4), NumPut("Int", 1, dark)
      DllCall("dwmapi\DwmSetWindowAttribute", "Ptr", hwnd, "Int", 20, "Ptr", dark, "Int", 4)
      bg_type := (brightness < 200) ? 3 : 2
      backdrop := Buffer(4)
      NumPut("Int", bg_type, backdrop)
      DllCall("dwmapi\DwmSetWindowAttribute", "Ptr", hwnd, "Int", 38, "Ptr", backdrop, "Int", 4)
      corner := Buffer(4)
      NumPut("Int", 2, corner) 
      DllCall("dwmapi\DwmSetWindowAttribute", "Ptr", hwnd, "Int", 33, "Ptr", corner, "Int", 4)
    }

    AHKCMDGUI.OnEvent("Close", ExitAHKCMD)

    AHKCMDGUI.SetFont("s20 cF1F1F1 q5", "微软雅黑")
    cmdInput := AHKCMDGUI.Add("Edit", "w500 -E0x200 -VScroll -HScroll +Background" bg_color, "eeadd ")

    AHKCMDGUI.SetFont("s16 cF1F1F1 q5", "微软雅黑")
    resultArea := AHKCMDGUI.Add("Edit", "w500 h300 ReadOnly -E0x200 -VScroll -HScroll +Background" bg_color)

    if (isWin11) {
      WinSetTransColor(bg_color, AHKCMDGUI)
    }

    isTimerRunning := true
    SetTimer TimerExitGUI.Bind(myTitle), 1000

    AHKCMDGUI.Show()

    Sleep 1
    Send "{Right}"

    eemv(*) {
      cmdInput.Value := "eemv "
      send "{End}"
    }
    eere(*) {
      cmdInput.Value := "eere "
      send "{End}"
    }
    eeen(*) {
      cmdInput.Value := "eeen "
      send "{End}"
    }
    eedel(*) {
      cmdInput.Value := "eedel "
      send "{End}"
    }
    eelua(*) {
      cmdInput.Value := "eelua "
      send "{End}"
    }
    eeadd(*) {
      cmdInput.Value := "eeadd "
      send "{End}"
    }
    eeuser(*) {
      cmdInput.Value := "eeuser "
      send "{End}"
    }
    eehelp(*) {
      cmdInput.Value := "eehelp"
      send "{End}"
      ExecuteCommand()
    }
    eedep(*) {
      cmdInput.Value := "eedep"
      send "{End}"
      ExecuteCommand()
    }
    eesync(*) {
      cmdInput.Value := "eesync"
      send "{End}"
      ExecuteCommand()
    }
    eequotes(*) {
      SendText '""'
      Send "{Left}"
    }
    changeAutoTimer(*) {
      if isTimerRunning {
        isTimerRunning := false
        resultArea.Value := "定时器已关闭"
      } else {
        isTimerRunning := true
        SetTimer TimerExitGUI.Bind(myTitle), 1000
        resultArea.Value := "定时器已开启"
      }
    }

    TurnonAHKCMDHotkey(*) {
      HotIfWinActive "ahk_class AutoHotkeyGUI"  
      Hotkey "Esc", ExitAHKCMD, "On"
      Hotkey "^Enter", ExecuteCommand, "On"
      Hotkey "^m", eemv, "On"
      Hotkey "^r", eere, "On"
      Hotkey "^d", eedel, "On"
      Hotkey "^l", eelua, "On"
      Hotkey "^u", eeuser, "On"
      Hotkey "^h", eehelp, "On"
      Hotkey "^p", eedep, "On"
      Hotkey "^s", eesync, "On"
      Hotkey "^k", eeadd, "On"
      Hotkey "^t", changeAutoTimer, "On"
      Hotkey "^e", eeen, "On"
      Hotkey "^`'", eequotes, "On"
    }
    TurnonAHKCMDHotkey()

    closeAHKCMDHotkey(*) {
      Hotkey "Esc", ExitAHKCMD, "Off"
      Hotkey "^Enter", ExecuteCommand, "Off"
      Hotkey "^m", eemv, "Off"
      Hotkey "^r", eere, "Off"
      Hotkey "^d", eedel, "Off"
      Hotkey "^l", eelua, "Off"
      Hotkey "^u", eeuser, "Off"
      Hotkey "^h", eehelp, "Off"
      Hotkey "^p", eedep, "Off"
      Hotkey "^s", eesync, "Off"
      Hotkey "^k", eeadd, "Off"
      Hotkey "^t", changeAutoTimer, "Off"
      Hotkey "^e", eeen, "Off"
      Hotkey "^`'", eequotes, "Off"
    }

    ExitAHKCMD(*) {
      if (AHKCMDGUI) {
        closeAHKCMDHotkey()
        AHKCMDGUI.Destroy()
      } else if (WinExist(myTitle)) {
        closeAHKCMDHotkey()
        WinClose myTitle
      }
    }

    TimerExitGUI(myTitle) {
      if !WinActive(myTitle) {
        Sleep 30
        if !WinActive(myTitle) {
          SetTimer , 0        
          ExitAHKCMD()
        }
      } else if not isTimerRunning {
        SetTimer , 0
      }
    }

    ExecuteCommand(*) {
      try {
        command := cmdInput.Value
        if (command = "") {
          resultArea.Value := "错误：请输入命令"
          return
        }
        resultArea.Value := "运行中，请稍等..."

        result := RunCMD(command)

        if (result = "") {
            resultArea.Value := "命令执行成功，但无输出内容"
        } else {
            resultArea.Value := result
        }

        cmd4 := SubStr(cmdInput.Value, 1, 4)
        cmd5 := SubStr(cmdInput.Value, 1, 5)
        res := resultArea.Value
        if (((InStr("eeadd eeuse", cmd5) || InStr("eere eeen", cmd4)) && SubStr(res, 1, 12) == "Successfully")
          || (cmd5 == "eedel" && SubStr(res, 1, 7) == "Deleted")
          || (cmd4 == "eemv"  && SubStr(res, 1, 2) == "输入")
          || (cmd5 == "eelua" && SubStr(res, 1, 4) == "word")) 
        {
            Run(A_ComSpec " /C eedep", , "Hide")
        }
      }
    }
  }
}


GetAreaBrightnessFast(centerX, centerY, size := 20) {
    offset := size // 2
    x := centerX - offset
    y := centerY - offset
    
    hdcScreen := DllCall("GetDC", "Ptr", 0, "Ptr")
    hdcMem := DllCall("CreateCompatibleDC", "Ptr", hdcScreen, "Ptr")
    hBitmap := DllCall("CreateCompatibleBitmap", "Ptr", hdcScreen, "Int", size, "Int", size, "Ptr")
    objOld := DllCall("SelectObject", "Ptr", hdcMem, "Ptr", hBitmap, "Ptr")
    
    DllCall("BitBlt", "Ptr", hdcMem, "Int", 0, "Int", 0, "Int", size, "Int", size, "Ptr", hdcScreen, "Int", x, "Int", y, "UInt", 0x00CC0020)
    
    bmi := Buffer(40, 0)
    NumPut("UInt", 40, bmi, 0)         
    NumPut("Int", size, bmi, 4)      
    NumPut("Int", -size, bmi, 8)      
    NumPut("UShort", 1, bmi, 12)   
    NumPut("UShort", 32, bmi, 14) 
    
    bufSize := size * size * 4
    pixelBuf := Buffer(bufSize)
    
    DllCall("GetDIBits", "Ptr", hdcMem, "Ptr", hBitmap, "UInt", 0, "UInt", size, "Ptr", pixelBuf, "Ptr", bmi, "UInt", 0)
    
    DllCall("SelectObject", "Ptr", hdcMem, "Ptr", objOld)
    DllCall("DeleteObject", "Ptr", hBitmap)
    DllCall("DeleteDC", "Ptr", hdcMem)
    DllCall("ReleaseDC", "Ptr", 0, "Ptr", hdcScreen)
    
    totalLuminance := 0
    Loop size * size {
        offset := (A_Index - 1) * 4
        b := NumGet(pixelBuf, offset, "UChar")
        g := NumGet(pixelBuf, offset + 1, "UChar")
        r := NumGet(pixelBuf, offset + 2, "UChar")
        
        totalLuminance += (0.299 * r + 0.587 * g + 0.114 * b)
    }
    
    return totalLuminance / (size * size)
}

RunCMD(command) {
    local hRead, hWrite, siBuf, piBuf, result, bytesRead, memBuf, ptrSize, SI_SIZE, PI_SIZE
    
    ptrSize := A_PtrSize
    SI_SIZE := ptrSize = 8 ? 104 : 68
    PI_SIZE := ptrSize = 8 ? 24 : 16
    
    if !DllCall("CreatePipe", "Ptr*", &hRead := 0, "Ptr*", &hWrite := 0, "Ptr", 0, "UInt", 0)
        return "Error: CreatePipe failed"
    
    DllCall("SetHandleInformation", "Ptr", hWrite, "UInt", 1, "UInt", 1)

    siBuf := Buffer(SI_SIZE, 0)
    NumPut("UInt", SI_SIZE, siBuf, 0)
    NumPut("UInt", 0x100, siBuf, ptrSize = 8 ? 60 : 44)
    NumPut("Ptr", hWrite, siBuf, ptrSize = 8 ? 88 : 60) 
    NumPut("Ptr", hWrite, siBuf, ptrSize = 8 ? 96 : 64)

    piBuf := Buffer(PI_SIZE, 0)
    
    if DllCall("CreateProcess", "Ptr", 0, "Str", A_ComSpec " /C " command, 
               "Ptr", 0, "Ptr", 0, "Int", true, "UInt", 0x08000000, 
               "Ptr", 0, "Ptr", 0, "Ptr", siBuf, "Ptr", piBuf) {
        
        DllCall("CloseHandle", "Ptr", hWrite)
        
        result := ""
        memBuf := Buffer(4096)
        
        while DllCall("ReadFile", "Ptr", hRead, "Ptr", memBuf, "UInt", 4096, "UInt*", &bytesRead := 0, "Ptr", 0) && bytesRead > 0 {
            result .= StrGet(memBuf, bytesRead, "CP65001")
        }
        
        DllCall("CloseHandle", "Ptr", NumGet(piBuf, 0, "Ptr"))
        DllCall("CloseHandle", "Ptr", NumGet(piBuf, ptrSize, "Ptr"))
    } else {
        DllCall("CloseHandle", "Ptr", hWrite)
        result := "Error: CreateProcess failed"
    }
    
    DllCall("CloseHandle", "Ptr", hRead)
    return result
}