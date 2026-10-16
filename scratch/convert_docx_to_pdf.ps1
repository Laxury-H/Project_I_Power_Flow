$ErrorActionPreference = "Stop"
$docxPath = "c:\Users\Lax\Downloads\Project_I_Power_Flow\report\Project_I_Report_HUST_Vietnamese.docx"
$pdfPath = "c:\Users\Lax\Downloads\Project_I_Power_Flow\report\Project_I_Report_HUST_Vietnamese.pdf"

$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open($docxPath)
    # wdFormatPDF = 17
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close()
    Write-Host "PDF successfully converted to $pdfPath"
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
