$exts=@("wafex")
echo "## setting up file associations"
foreach ($ext in $exts){
    $extfile=$ext+"file"
    $dotext="." + $ext
    cmd /c assoc $dotext=$extfile
    cmd /c "ftype $extfile=""C:\Users\Souvik\Documents\classes\PROJECT\Wacom\WACOM\Wacom_FE\Release\output\PDFE\PDFE.exe"" %1"
    echo ""
}