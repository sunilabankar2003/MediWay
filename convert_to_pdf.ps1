$word = New-Object -ComObject Word.Application
$word.Visible = $false

$inputPath = "A:\Codes\MediWay\FA1_Activity_Details_MediWay.odt"
$outputPath = "A:\Codes\MediWay\FA1_Activity_Details_MediWay.pdf"

try {
    $doc = $word.Documents.Open($inputPath)
    $doc.SaveAs([ref]$outputPath, [ref]17)
    $doc.Close()
}
finally {
    $word.Quit()
}
