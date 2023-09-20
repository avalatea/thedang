@set PYTHONIOENCODING=utf-8
@powershell -noprofile -c "cmd /c \"$(thedang %* $(doskey /history)[-2])\"; [Console]::ResetColor();"
