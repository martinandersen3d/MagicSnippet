# Image Magic must be installed
$sourceFolder = (Get-Location).Path
$destinationFolder = (Get-Location).Path
Get-ChildItem -Path $sourceFolder -Filter *.png | ForEach-Object {
    $pngFile = $_.FullName
    $icoFile = $destinationFolder + '\' + $_.Name.Replace('.png', '.ico')
    & 'C:\Program Files\ImageMagick-7.1.0-Q16-HDRI\magick.exe' convert $pngFile $icoFile
}