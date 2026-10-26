param([string]$InputDocx,[string]$OutputPdf)
$wordRenderer = $null
$wordDocument = $null
try {
  $wordRenderer = New-Object -ComObject Word.Application
  $wordRenderer.Visible = $false
  $wordRenderer.DisplayAlerts = 0
  $wordDocument = $wordRenderer.Documents.Open($InputDocx, $false, $true, $false)
  $wordDocument.Repaginate()
  $wordDocument.ExportAsFixedFormat($OutputPdf, 17)
  Write-Output ('Exported pages: '+$wordDocument.ComputeStatistics(2))
} finally {
  if ($wordDocument) { $wordDocument.Close(0); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($wordDocument) }
  if ($wordRenderer) { $wordRenderer.Quit(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($wordRenderer) }
}
