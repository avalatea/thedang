if ((Get-Command "dang").CommandType -eq "Function") {
	dang @args;
	[Console]::ResetColor()
	exit
}

"First time use of thedang detected. "

if ((Get-Content $PROFILE -Raw -ErrorAction Ignore) -like "*thedang*") {
} else {
	"  - Adding thedang intialization to user `$PROFILE"
	$script = "`n`$env:PYTHONIOENCODING='utf-8' `niex `"`$(thedang --alias)`"";
	Write-Output $script | Add-Content $PROFILE
}

"  - Adding dang() function to current session..."
$env:PYTHONIOENCODING='utf-8'
iex "$($(thedang --alias).Replace("function dang", "function global:dang"))"

"  - Invoking dang()`n"
dang @args;
[Console]::ResetColor()
